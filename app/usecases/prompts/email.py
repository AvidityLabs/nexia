

import os
import json
from langchain.llms import OpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from api.utilities.openai.utils import completion
 
from dotenv import load_dotenv
load_dotenv()
 

os.environ['OPENAI_API_KEY'] = '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'


llm = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], model_name='gpt-3.5-turbo', temperature=0)


def generateEmail(payload: any):
    # Define the PromptTemplate
    
    # Define a template string
    template_string = """
    Perform the following actions:
    1. Generate an email based on the text that is delimited by triple backticks into a style that is {style}. text: ```{text}```\
    2. Output the result must be in HTML format excluding backticks.
    """
    
    
    # Create a prompt template using above template string
    prompt_template = ChatPromptTemplate.from_template(template_string)
    
    
    customer_style = f"{payload.get('language')} in a {payload.get('tone')} tone"
    

    # customer_message will generate the prompt and it will be passed into the llm to get a response. 
    customer_messages = prompt_template.format_messages(
                        style=customer_style,
                        text=payload.get('email_content'))

    # Call the LLM to translate to the style of the customer message. 
    response = llm(customer_messages)


    return response
    # email_prompt_template = PromptTemplate(
    #     input_variables=["subject", "recipient", "content", "tone", "format", "language"],
    #     template="Generate an email with the following details:\n"
    #             "- Subject: {subject}\n"
    #             "- Recipient: {recipient}\n"
    #             "- Content: {content}\n"
    #             "- Tone: {tone}\n"
    #             "- Format: {format}\n"
    #             "- Language: {language}\n"
    # )


    # prompt = email_prompt_template.from_template(email_prompt_template)

    # chat_prompt = ChatPromptTemplate.from_messages([
    # ("system", "You are a world-class email generation model."),
    # ("human", prompt)
    # ])

    
    # chain = LLMChain(
    #     prompt=chat_prompt,
    #     llm=llm  # You should define gpt_turbo or your language model here
    # )


    # print(chain)

def generateEmailSubjectLine(payload):
    pass


def generateEmailBody(payload):
    # recipient [customers/prospects/subscribers]
    prompt = f"""
    Instruction: Generate Email Body\

    Objective: Create an engaging and persuasive email body to effectively communicate the following context provided in the text delimited by tripple backticks.\
                Context:
                ```{payload.get('purpose')}```
    Guidelines:
    1 - Recipient and Target Audience: The email is intended for the audience described in the following text delimited by angle brackects\
        Audience:
        <{payload.get('audience')}>
    2 - Email Purpose: Clearly state the purpose of the email, whether it's to provide information, promote a product/service, share an update, or encourage a specific action.\
    3 - Key Message: Identify the primary message or value proposition that should be communicated prominently in the email.\
    4 - Tone and Style: The tone/style should be as mentioned in the following text delimited by tripple backticks Tone:```{payload.get('tone')}``` to resonate with the target audience.\
    5 - Personalization: If applicable, personalize the email by including the recipient's name or other relevant details to establish a connection.\
    6 - Structure and Format: Determine the structure and format of the email, including sections such as introduction, main body, call to action, and closing.\
    7 - Length and Conciseness: Ensure the email is concise and to the point, with a recommended length of 100 words.\
    8 - Call to Action: Clearly define the desired action you want the recipient to take and make it prominent in the email.\
    9 - Additional Information: Include any additional details, specifications, or requirements relevant to the email content.
    8 - Proofreading: Review the generated email body for grammar, spelling, and clarity before finalizing\
    9 - Output the result in HTML format 
    """
    return completion(prompt)



def generateEmailToneAdjustment(payload):
    prompt = f"""
    Perform the following actions
    Modify the tone of the given email to better align with the desired communication style. Please follow these guidelines:\
    Guidelines:
    Desired Tone: The tone/style should match the desired specification described in the following text delimited by tripple backticks Tone```{payload.get('tone')}```.\
    Email Content: Provide the original email content as a reference for the tone adjustment.
    Key Points: The email should be preserved or emphasized during the tone adjustment.
    Output: Output the result in HTML format 
    """
    return completion(prompt)