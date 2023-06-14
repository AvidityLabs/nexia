from api.utilities.openai.utils import completion

def generateCourseTitle(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a captivating and informative title for a course.
    2 - Consider the course content, target audience, and desired outcome.
    3 - Incorporate keywords and phrases that reflect the course topic and benefits.
    4 - Use language that evokes curiosity and captures attention.
    5 - Ensure the title accurately represents the value and uniqueness of the course.
    6 - Output the resulting course title.

    Course Topic: {payload['topic']}
    Target Audience: {payload['audience']}
    Desired Outcome: {payload['outcome']}

    """
    return completion(prompt)


def generateCourseSubtitle(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a compelling and descriptive subtitle for a course.
    2 - Consider the course topic, main benefits, and target audience.
    3 - Use concise language to convey the value and key points of the course.
    4 - Highlight the unique selling points and differentiate it from other courses.
    5 - Output the resulting course subtitle.

    Course Topic: {payload['topic']}
    Main Benefits: {payload['benefits']}
    Target Audience: {payload['audience']}

    """
    return completion(prompt)


def generateCourseDescription(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a compelling and informative course description.
    2 - Highlight the key aspects, learning outcomes, and topics covered in the course.
    3 - Clearly state the target audience and prerequisites, if any.
    4 - Emphasize the unique selling points and benefits of taking the course.
    5 - Use persuasive language to engage potential learners and encourage enrollment.
    6 - Output the resulting course description.

    Course Topic: {payload['topic']}
    Main Benefits: {payload['benefits']}
    Target Audience: {payload['audience']}
    Prerequisites: {payload['prerequisites']}

    """
    return completion(prompt)


def generateCourseLectureTitles(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a list of lecture titles for the course.
    2 - Ensure each lecture title is clear, concise, and reflects the content of the lecture.
    3 - Use descriptive and engaging language to capture the interest of learners.
    4 - Consider organizing the lecture titles in a logical order that flows well.
    5 - Output the resulting list of lecture titles.

    Course Topic: {payload['topic']}
    Number of Lectures: {payload['num_lectures']}

    """
    return completion(prompt)


def generateCourseQuizQuestions(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a set of quiz questions for the course.
    2 - Ensure each question is related to the course content and assesses the learners' understanding.
    3 - Use a variety of question types, such as multiple choice, true/false, or short answer, to keep the quiz engaging.
    4 - Provide clear and concise instructions for each question.
    5 - Include correct answers and relevant explanations.
    6 - Output the resulting set of quiz questions.

    Course Topic: {payload['topic']}
    Number of Questions: {payload['num_questions']}

    """
    return completion(prompt)


def generateCourseExercises(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a set of exercises for the course.
    2 - Ensure each exercise is relevant to the course topic and provides practical application of the concepts learned.
    3 - Include clear instructions and guidelines for each exercise.
    4 - Specify the expected output or solution for each exercise.
    5 - Consider including variations or additional challenges to cater to learners of different skill levels.
    6 - Output the resulting set of course exercises.

    Course Topic: {payload['topic']}
    Number of Exercises: {payload['num_exercises']}

    """
    return completion(prompt)



def generateGrammarCorrection(payload):
    prompt = f"""
    Perform the following actions:\
    1 - Correct the grammar of following text delimited by tripple backticks`\
    2- The language should be in {payload.get('language')}, with a tone that is {payload.get('tone')}\
    3 - Output the result in HTML format\
    
    Text:
    ```{payload.get('text')}```
    """
    return completion(prompt)




def generateKeywordsExtractor(payload):
    prompt = f"""
    Perform the following actions:
    1 - Extract keywords from the provided text delimited by triple backticks. The text should be formatted as follows:
    2 - Specify the desired number of keywords to extract by setting the value of 'num_keywords' variable.
    3 - Consider the context and relevance of the text when selecting the keywords.
    4 - Apply any necessary pre-processing techniques, such as removing stop words or punctuation, to enhance keyword extraction.
    5 - Utilize appropriate natural language processing or machine learning techniques to extract the most relevant keywords.
    6 - Output the extracted keywords as a list.

    Text:
    {payload['text']}
    
    Desired Number of Keywords: {payload['num_keywords']}
    """


def generateParaphraseText(payload):
    prompt = f"""
    Perform the following actions:
    1 - paraphrase the following text delimited by tripple backticks.\
    2 - The paraphrased version should accurately convey the same meaning as the original, but should not simply copy the wording or structure.\
    3- Make sure to properly cite the original text and include all of the key points and supporting details.\
    4 - The text should be written in standard language {payload.get('language')}, in a tone that is {payload.get('tone')}\
    5 - Output the result in HTML format 

    Text:
    ```{payload.get('text')}```
    """
    return completion(payload)



def generateQuestionAnswer(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a consistent question and answer dialogue about the text delimited by tripple backticks.\
    2 - The language for the dialogue is specified in the text delimited by angle brackets\
    3 - The tone is specified in the text delimited by tripple dashes.\

    Text:
    ```{payload.get('topicDescription')}```

    Text:
    <{payload.get('language')}>

    Text:
    ---{payload.get('tone')}---
    
    """
    return completion(prompt)

def generatePresentation(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a compelling presentation based on the provided information.
    2 - Consider the purpose, topic, and target audience of the presentation.
    3 - Structure the presentation with a clear introduction, well-organized content, and a memorable conclusion.
    4 - Use effective visuals, such as images, graphs, or charts, to enhance the presentation and convey information.
    5 - Incorporate persuasive language and storytelling techniques to engage the audience and convey key messages.
    6 - Ensure the presentation is informative, engaging, and aligned with the desired tone and style.
    7 - Output the resulting presentation.

    Presentation Purpose:
    {payload['purpose']}

    Presentation Topic:
    {payload['topic']}

    Target Audience:
    {payload['audience']}
    """
    return completion(prompt)




def generateCourseArticles(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate informative and engaging articles for an online course.
    2 - Ensure the articles are relevant to the course topic and provide valuable insights to the learners.
    3 - Research the subject matter thoroughly to gather accurate information.
    4 - Write articles that are easy to understand, well-structured, and follow a logical flow.
    5 - Incorporate examples, case studies, and real-life scenarios to enhance comprehension.
    6 - Use a tone that is appropriate for the target audience and aligns with the course objectives.
    7 - Output the generated articles.

    Course Topic: {payload['course_topic']}
    Number of Articles: {payload['num_articles']}
    Article Length: {payload['article_length']} words
    """
    return completion(prompt)


def generateSummarizeText(payload):
    prompt = f"""
    Perform the following actions:
    1 - Summarize the given text in the language specified in the text delimited by angle brackets, with a tone that is specified in the text delimited by tripple dashes\
    2 - Identify the main ideas and key points.\
    3 - The summary should be concise and convey the overall message of the text.\
    4 - Include any important details or information that is relevant to the topic.\
    5 - Indicate the text length reduction rate you used while summarizing the text.\
    6 - rovide a title that accurately represents the content of the summarized text.\
    5 - Output the result in HTML format 
    
    Text:
    <{payload.get('language')}>

    Text:
    ---{payload.get('tone')}---
    """
    return completion(prompt)
