from django.db import models
from usecases.registered_usecase_funcs import usecase_func_dict
from usecases.prompts.academic import *
from usecases.prompts.blog import *
from usecases.prompts.brand import *
from usecases.prompts.business import *
from usecases.prompts.copywriting import *
from usecases.prompts.email import *
from usecases.prompts.feedback import *
from usecases.prompts.job import *
from usecases.prompts.marketing import *
from usecases.prompts.newsletter import *
from usecases.prompts.other import *
from usecases.prompts.pressrelease import *
from usecases.prompts.product import *
from usecases.prompts.sales import * 
from usecases.prompts.seo import * 
from usecases.prompts.socialmedia import * 
from usecases.prompts.video import * 
from usecases.prompts.website import * 
from usecases.prompts.youtube import *
from usecases.prompts.podcast import *

from api.utilities.openai.utils import completion
from llm.models import *

from api.utilities.langchain.config import openai_wrapper
from langchain.prompts import PromptTemplate
class UseCaseCategory(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

# Create your models here.

class UseCase(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    function_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    navigateTo = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(UseCaseCategory, on_delete=models.CASCADE, blank=True, null=True)
    # prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return self.title

    def get_usecase_function_by_name(self, function_name):
    # Load the use case URLs and function names from the database or a configuration file
        return  usecase_func_dict.get(function_name)
    #TODO: Add logger
    
    def getPrompt(self, payload):
        function = self.get_usecase_function_by_name(self.navigateTo)
        if function:
            try:
                return function(payload)
            except Exception as e:
                # Handle exceptions that occur during function execution
                print(f"An error occurred while executing the use case: {e}")
                return None
        else:
            raise ValueError(f"No function found for use case: {self.function_name}")
        
    # NEW OPTION  With models  
    # def do_query(self, **variables):
    #     input_vars = self.prompt.as_dict().get("variables")
    #     template = self.prompt.template
    #     prompt = PromptTemplate(input_variables=input_vars, template=template)
    #     res = openai_wrapper.get_response(prompt)
    #     return res
    
    def do_query(self, prompt):
        res = openai_wrapper.get_response(prompt)
        return res
      
    # Previous option  
    def promptExecute(self, payload):
        prompt = self.getPrompt(payload)
        # print(prompt)
        return self.do_query(prompt)
