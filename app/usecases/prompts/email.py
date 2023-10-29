from langchain.prompts.chat import ChatPromptTemplate
from api.utilities.openai.utils import completion
from api.utilities.langchain.config import openai_wrapper




def generateEmail(payload: any):
    # Define the PromptTemplate
    template_string = """
    You are a help assistant that generates an email and the text style that is translated into {language} in a {tone} and is formatted into HTML format. Based on the text: ```{text}```
    """

    human_template = "{text}"

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", template_string),
        ("human", human_template),
    ])

    formatted_messages = chat_prompt.format_messages(
        language=payload.get('language'),
        tone=payload.get('tone'),
        text=payload.get('email_content')
    )
    

    return formatted_messages


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