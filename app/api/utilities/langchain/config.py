import os
from langchain.llms import OpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.output_parsers.json import SimpleJsonOutputParser
from api.utilities.openai.utils import completion
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
# from tiktoken import Tokenizer  # Import Tokenizer for counting tokens

load_dotenv()

os.environ['OPENAI_API_KEY'] = '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'


#OpenAI Config
class OpenAIWrapper:
    def __init__(self, model_name, model_kwargs=None):
        self.llm = ChatOpenAI(**model_kwargs)

    def get_response(self, prompt):
        try:
            with get_openai_callback() as cb:
                res = self.llm(prompt)
                token_usage = {
                    "total_tokens": cb.total_tokens,
                    "prompt_tokens": cb.prompt_tokens,
                    "completion_tokens": cb.completion_tokens,
                    "total_cost": cb.total_cost
                }
            return {
                "res": res.to_json(),
                "token_usage": token_usage
            }
        except Exception as e:
            return {
                "error": str(e),
                "res": None,
                "token_usage": None
            }

# Usage
model_name = "gpt-3.5-turbo"
model_kwargs = {
    "api_key": os.getenv('OPENAI_API_KEY')
}

openai_wrapper = OpenAIWrapper(model_name, model_kwargs)



