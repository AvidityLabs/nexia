from api.utilities.openai.utils import completion

def generateJobDescription(payload):
    prompt = f"""
    Perform the following actions:\
    1 - Generate a job description for a role described in the text delimited by tripple backticks.\
    2 - The language should be in {payload.get('language')}, with a tone that is {payload.get('tone')}.
    3 - Make sure to include a detailed and clear overview of the role, including the responsibilities, qualifications, and requirements for the position.\
    4 - Also, include information about the company culture and benefits to give an idea about the working environment to the potential candidates.\
    5 - Use appropriate keywords to optimize the job description for search engines and include a clear call-to-action to apply for the role.\
    6 - Output the result in HTML format 

    Text:
    ```{payload.get('jobRole')}```
    """
    return completion(prompt)


def generateCoverLetter(payload: any):
    prompt = f"""
    Perform the following actions:\
    1 - Generate a personalized and detailed cover letter for a job role described in the text delimited by angle brackets.\
    Job Role: <{payload.get('jobRole')}>

    2 - The highlighted skills, qualifications, and achievements that match the requirements of the position are described in the text delimited by triple backticks.\
    Skills: ```{payload.get('jobSkills')}```\

    3 - Use desired language and tone for the cover letter.\
    Language: ```{payload.get('language')}```\
    Tone: ```{payload.get('tone')}```\

    4 - Tailor the letter to the specific job, highlighting the relevant skills and experience.\

    5 - Show enthusiasm for the company and position, and express why you would be a great fit for the ```{payload.get('jobRole')}``` role.\

    6 - End the letter with a call-to-action, encouraging the hiring manager to contact you for an interview.\

    7 - Provide the result in HTML format.
    """
    return completion(prompt)



def generateInterviewQuestions(payload):
    prompt = f"""
    Perform the following actions:\
    1 - Generate a set of interview questions for an interviewee with the bio described in the text delimited by tripple backticks.\
    2 - Base the interview in the context of the text delimited by angle brackets\
    3 - The interview questions should be in {payload.get('language')}, with a tone that is {payload.get('tone')}.\
    4 - Make sure to include a mix of open-ended and closed-ended questions, and to tailor the questions to the specific interviewee and context.\
    5 - Also, include behavioral based questions to understand the interviewee's past experience and how they handle different situations.\
    6 - Lastly, include a few creative and unique questions to understand the interviewee's thinking process and personality.\
    7 - Output the result in HTML format \
    
    Text:
    ```{payload.get('bio')}```

    Text:
    <{payload.get('context')}>
    """
    return completion(prompt)
