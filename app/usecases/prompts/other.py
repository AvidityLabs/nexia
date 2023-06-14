from api.utilities.openai.utils import completion

def generateStoryPlots(payload):
    prompt = f"""
    Perform the following actions:\
    1 - Generate a story based on the idea described in the text delimited by tripple backticks.\
    2 - The language should be in ```{payload.get('language')}```, with a tone that is ```{payload.get('tone')}```.\
    3 - Make sure to include a clear and compelling plot, with well-developed characters and a satisfying resolution.\
    4 - Also, pay attention to the pacing, ensuring that the story maintains a balance of tension and release.\
    5 - Use descriptive language to create vivid imagery and bring the story to life.\
    6 - Ensure that the story aligns with the chosen tone and evokes the desired emotions in the audience.\
    7 - Output the result in HTML format.
    
    Text:
    ```{payload.get('storyIdea')}```
    """
    return completion(prompt)


def generateSongLyrics(payload):
    prompt = f"""
    Perform the following actions:\
    1 - Generate song lyrics based on the idea described in the text delimited by tripple backticks.\
    2 - The song lyric should be in ```{payload.get('language')}``` language, with a tone that is ```{payload.get('tone')}```.\
    3 - Make sure to include a clear and compelling narrative, with well-crafted verses, chorus, and a memorable hook.\
    4 - Also, pay attention to the rhyme scheme and meter, ensuring that the lyrics flow smoothly and are easy to sing along.\
    5 - Use descriptive language and imagery to bring the song idea to life and to create an emotional connection with the audience.\
    6 - Make sure that the lyrics align with the chosen tone and evoke the desired emotions.\
    7 - Output the result in HTML format.

    Text:
    ```{payload.get('songIdea')}```
    """
    return completion(payload)


def generateSmsAndNotifications(payload):
    prompt = f"""
    Perform the folowing actions:\
    1 - Generate SMS and push notifications based on the following text delimited by tripple backticks.\
    2 - The language should be in {payload.get('language')}, with a tone that is {payload.get('tone')}.\
    3 - Make sure to include a clear and concise message that is relevant to the user and the current context in the text delimited by tripple backticks.\
    4 - Also, pay attention to the timing and frequency of the SMS and notifications, ensuring that they are not too frequent or disruptive.\
    5 - Use persuasive language and images to grab the user's attention and create a sense of urgency.\
    6 - Additionally, make sure to consider the character limit of SMS and to provide a clear call-to-action to encourage the user to take action.\
    7 - Make sure that the SMS and notifications align with the user's preferences and opt-in status.\
    8 - Output the result in HTML format.
    
    Text:
    ```{payload.get('context')}```
    """
    return completion(prompt)






def generateProfileBio(payload):
    # purpose Personal Profile Bio, Business Profile Bio, Freelancer Profile Bio, Artist Profile Bio
    prompt = f"""
    Perform the folowing actions:\
    1 - Generate Profile Bio\
    2 - Using the provided information, create a captivating and concise profile bio that effectively showcases the individual or entity. Please follow these guidelines:\
    Guidlines:\
    Name or Entity: The specified name or entity for which the profile bio is being generated is described in the following text delimited by tripple backticks Name:```{payload.get('name')}```\
    Purpose: The purpose or main activities of the individual or entity to provide context for the profile bio are described in the following text delimited by tripple backticks Purpose:```{payload.get('purpose')}```\
    Background: Highlight relevant background information such as achievements, qualifications, expertise, or unique selling points. Which are described in the following text delimited by tripple backticks Background:```{payload.get('background')}```\
    Tone and Style: The Tone and Style: should be in the following text delimited by tripple backticks Tone:```{payload.get('tone')}```\
    Language: The language should be as described in the following text delimited by tripple backticks Language:```{payload.get('languge')}```\
    Key Attributes: The key attributes, skills, or qualities that make the individual or entity stand out and are worth mentioning in the profile bio.\
    Call to Action (if applicable): If there is a desired action or next step for the audience to take, include a compelling call to action.\
    3 - Output the result in HTML format 
    """
    return completion(prompt)

























































"""_summary_
Yes, an AI writing tool can be used to analyze an essay and provide a percentage or score based on certain criteria. Here's how it can be done:

Readability Analysis: The AI tool can assess the readability of the essay by considering factors like sentence length, vocabulary complexity, and overall readability scores (e.g., Flesch-Kincaid or Gunning Fog index). It can assign a readability percentage or grade level indicating the essay's readability.

Grammar and Spelling Check: The AI tool can analyze the essay for grammar and spelling errors. It can highlight the mistakes and provide suggestions for corrections. The percentage can indicate the accuracy of the essay in terms of grammar and spelling.

Plagiarism Detection: The AI tool can compare the essay against a database of existing texts to identify any instances of plagiarism. It can provide a percentage indicating the similarity between the essay and other sources.

Coherence and Cohesion Analysis: The AI tool can assess how well the essay flows and whether the ideas are logically connected. It can analyze the use of transitional phrases, sentence structure, and paragraph coherence. The percentage can reflect the essay's coherence and cohesion.

Content Analysis: The AI tool can evaluate the essay's content based on predefined criteria. For example, it can assess the relevance of the content, the depth of analysis, the clarity of arguments, or the incorporation of supporting evidence. The percentage can indicate the overall quality of the essay's content.

Structure and Organization Assessment: The AI tool can analyze the essay's structure, including the introduction, body paragraphs, and conclusion. It can assess the essay's adherence to a proper essay structure and provide feedback on improving the organization. The percentage can reflect the essay's structural coherence.
"""


def automatedEssayAnalysis(payload):
    prompt = f"""
    Perform the following actions:
    1 - Analyze an essay based on the provided text.
    2 - Use natural language processing techniques to evaluate the essay's structure, coherence, grammar, and vocabulary.
    3 - Identify the essay's main ideas, supporting arguments, and conclusion.
    4 - Evaluate the essay's clarity, logical flow, and use of evidence.
    5 - Provide constructive feedback on areas of improvement, such as organization, sentence structure, and word choice.
    6 - Output the automated analysis of the essay.

    Essay Text:
    {payload['essay_text']}
    """
    return completion(prompt)


def plagiarismDetection(payload):
    prompt = f"""
    Perform the following actions:
    1 - Detect plagiarism in a given document.
    2 - Use advanced algorithms and techniques to compare the document against a database of sources.
    3 - Identify and highlight any instances of text that closely match existing sources.
    4 - Calculate similarity scores or percentages to indicate the level of potential plagiarism.
    5 - Provide a detailed report with the identified plagiarized sections and the corresponding sources.
    6 - Output the plagiarism detection results.

    Document Text:
    {payload['document_text']}
    """
    return completion(prompt)




def generateAdCopy(payload):
    prompt = f"""
    Instruction: Generate Ad Copy for product mentioned in the text delimited by tripple bacticks:
                
                Product/Service:
                ```{payload.get('product')}```

    Objective: Create compelling ad copy to promote Product/Service in the text delimited by backticks and the desired outcome is mentioned in the text delimited by tripple backticks.\
                
                Product/Service:
                ```{payload.get('product')}```  
                
                Desired Outcome:
                ```{payload.get('desiredOutcome')}```         

    Guidelines:
    1. Target Audience is mentioned in the following text delimited by tripple backticks: Audience:```{payload.get('audience')}```.\
    2. Key Selling Points are mentioned in the following text delimited by tripple backticks:\
       - Highlight, Showcase & Emphasize ```{payload.get('keySellingPoints')}\
    3. Tone and Style: should be in the following text delimited by tripple backticks Tone:```{payload.get('tone')}``` that resonates with the target audience.\
    4. Keywords or Phrases: Include the following text delimited by backticks ```{payload.get('keywords')}``` to optimize visibility and impact.\
    5. Length and Format: Concise ad copy, approximately 100 words, suitable for platform/channel mentioned in the following text delimited by tripple backticks. Platform:```{payload.get('platform')}```.\
    6. Compelling Content: Craft attention-grabbing, persuasive copy that encourages the target audience to desired action.
    7. Output the result in HTML format \

    Generate creative and effective ad copy that aligns with the provided guidelines.
    """

    return completion(prompt)





def generateCitation(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a citation for a source based on the provided information.
    2 - Ensure the citation follows the appropriate citation style (e.g., APA, MLA, Chicago).
    3 - Include the necessary details such as author(s), title, publication date, and source information.
    4 - Verify the accuracy of the information and format the citation accordingly.
    5 - Output the generated citation.

    Source Information:
    Title: {payload['title']}
    Author(s): {payload['authors']}
    Publication Date: {payload['publication_date']}
    Source: {payload['source']}
    Citation Style: {payload['citation_style']}
    """
    return completion(prompt)








def generateGoogleSearchAd(payload):
    prompt = f"""
    Perform the following actions:
    Generate a compelling Google Search Ad for our online advertising campaign. We need an ad that grabs attention, drives clicks, and delivers our message effectively keeping it concise and compelling.\

    1. Provide a brief description of the product or service we are advertising the product/service is described in the following text delimited by tripple backticks Product/Service: ```{payload.get('product')}```.\
    2. The target audience are described in the following text delimited by tripple backticks Audience:```{payload.get('audience')}.\
    3. The primary goal of our ad campaign is described in the following text delimted by tripple backticks Goal:```{payload.get('goal')}```\
    4. Highlight a key feature or benefit of our product/service that sets us apart from competitors. The key selling point is described in the following text delimited by tripple backticks Selling Point: ```{payload.get('keySellingPoints')}```\
    5. Craft a strong call to action that encourages users to take the desired action, such as "Shop Now," "Learn More," or "Get a Quote."\
    6. Identify relevant keywords or key phrases related to our product/service that will help the ad appear in relevant search results.\
    7. Specify the maximum budget allocated for this ad campaign.
    8: Output the result in HTML format 
    """
    return completion(prompt)





def generateCode(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate code snippets or templates based on specific requirements or programming patterns.
    2 - Specify the programming language and any specific requirements or patterns you need.
    3 - Provide the necessary details such as input/output specifications, algorithmic logic, or desired code structure.
    4 - Output the generated code snippets or templates.

    Programming Language: {payload['language']}
    Requirements or Patterns: {payload['requirements']}
    Additional Details: {payload['details']}
    """
    return completion(prompt)


def generateCodeDocumentation(payload):
    prompt = f"""
    Perform the following actions:
    1 - Provide automated suggestions for code comments, function and class descriptions, and inline documentation.
    2 - Specify the programming language and the code segment that needs documentation.
    3 - Include any specific requirements or guidelines for the code documentation.
    4 - Output the automated suggestions for code documentation.

    Programming Language: {payload['language']}
    Code Segment: {payload['code_segment']}
    Specific Requirements or Guidelines: {payload['requirements']}
    """
    return completion(prompt)


def generateErrorMessageEnhancement(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate clear and informative error messages or debugging suggestions.
    2 - Specify the programming language or framework used.
    3 - Provide the relevant code snippet or error message that needs enhancement.
    4 - Output the enhanced error message or debugging suggestion.

    Programming Language or Framework: {payload['language']}
    Code Snippet or Error Message: {payload['code_snippet']}
    """
    return completion(prompt)


def generateCodeRefactor(payload):
    prompt = f"""
    Perform the following actions:
    1 - Analyze the provided codebase for refactoring or optimization.
    2 - Specify the programming language or framework used.
    3 - Provide the codebase or specific code snippet that needs analysis.
    4 - Output suggestions for code refactoring or optimization to improve performance and maintainability.

    Programming Language or Framework: {payload['language']}
    Codebase or Code Snippet: {payload['codebase']}
    """
    return completion(prompt)


def generateTechnicalWriting(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate technical writing on the topic of {payload['topic']}.
    2 - Specify the desired length or word count for the writing.
    3 - Provide any specific requirements, guidelines, or key points to be covered in the writing.
    4 - Output the generated technical writing.

    Topic: {payload['topic']}
    Desired Length: {payload['length']}
    Requirements/Guidelines: {payload['requirements']}
    """
    return completion(prompt)


def summarizeCode(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a summary of code based on the provided snippet.
    2 - Specify the desired level of detail and length for the code summary.
    3 - Provide any specific requirements or areas of focus for the summary.
    4 - Output the generated code summary.

    Code Snippet:
    {payload['code_snippet']}
    
    Level of Detail: {payload['detail_level']}
    Desired Length: {payload['length']}
    Requirements/Focus Areas: {payload['requirements']}
    """
    return completion(prompt)


def generateAPIDocumentation(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate API documentation based on the provided API endpoints and specifications.
    2 - Specify the desired format and style for the documentation (e.g., Markdown, HTML, Swagger).
    3 - Include relevant details such as endpoint descriptions, request and response parameters, authentication requirements, and examples.
    4 - Ensure the documentation is clear, comprehensive, and easily understandable for developers.
    5 - Output the generated API documentation.

    API Endpoints and Specifications:
    {payload['endpoints']}

    Desired Format: {payload['format']}
    Style Guidelines: {payload['style']}

    Additional Notes or Requirements: {payload['notes']}
    """
    return completion(prompt)


def projectPlanEstimationGenerator(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a project plan and estimation based on the provided project requirements and scope.
    2 - Specify the desired format for the project plan (e.g., Gantt chart, Kanban board).
    3 - Include key project phases, tasks, milestones, and deliverables.
    4 - Estimate the effort, resources, and timeline required for each task.
    5 - Identify dependencies, risks, and potential mitigation strategies.
    6 - Ensure the project plan is realistic, achievable, and aligned with the client's expectations.
    7 - Output the generated project plan and estimation.

    Project Requirements and Scope:
    {payload['requirements']}

    Desired Format: {payload['format']}

    Additional Notes or Requirements: {payload['notes']}
    """
    return completion(prompt)