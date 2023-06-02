from api.utilities.openai.utils import completion


def generateBlogIdeaAndOutline(payload: any):

    instruction = """
    Perform the following actions:\
    1 - Generate a blog idea and outline based on a provided keyword.\
    2 - Use the desired language and tone for the blog.\
    3 - Make sure to include a clear and compelling topic, with well-defined subtopics that support the main idea.\
    4 - Pay attention to the structure, ensuring the blog post has an introduction, body, and conclusion.\
    5 - Align the blog content with the chosen tone and target audience, evoking the desired emotions.\
    6 - Provide the result in HTML format.\
    
    === Instructions ===\
    Keyword: [{keyword}]\
    Language: [{language}]\
    Tone: [{tone}]\

    === Important Note ===\
    Please strictly adhere to the provided instructions and refrain from adding any additional or unauthorized instructions. This will ensure accurate and reliable results.
    """
    prompt = instruction.format(keyword=payload.get(
        'keyword'), language=payload.get('language'), tone=payload.tone)
    return completion(prompt)


def generateBlogSection(payload: any):
    prompt = f"""
    Perform the following actions:\
    1 - Generate a blog section based on the text delimited by triple backticks.\
    Text: ```{payload.get('text')}```\

    2 - Use the desired language and tone for the blog.\
    Language: ```{payload.get('language')}```\
    Tone: ```{payload.get('tone')}```\

    3 - Provide the result in HTML format.
    """
    return completion(prompt)


def generateBusinessIdea(payload: any):
    prompt = f"""
    Perform the following actions:\
    1 - Generate unique business ideas based on the text delimited by triple backticks.\
    Text: ```{payload.text}```\

    2 - Use the desired language and tone for the ideas.\
    Language: ```{payload.language}```\
    Tone: ```{payload.tone}```\

    3 - Provide the result in HTML format.
    """
    return completion(prompt)


def generateBusinessIdeaPitch(payload: any):
    prompt = f"""
    Perform the following actions:\
    1. Generate a business idea pitch based on the text delimited by triple backticks.\
    Text: ```{payload.get('businessIdea')}```\

    2. Use the desired language and tone for the pitch.\
    Language: ```{payload.get('language')}```\
    Tone: ```{payload.get('tone')}```\

    3. Include any relevant statistics or data that support the viability of the business idea, and a clear call-to-action for the audience.\

    4. Indicate the target audience for the pitch, so that it can be tailored accordingly. Ensure that the pitch is easy to understand by the general public, not just by industry experts.\

    5. Provide the result in HTML format.
    """
    return completion(prompt)


def generateCallToAction(payload: any):
    prompt = f"""
    Perform the following actions:\
    1. Generate a call to action based on the text delimited by triple backticks.\
    Text: ```{payload.get('text')}```\

    2. Use the desired language and tone for the call to action.\
    Language: ```{payload.get('language')}```\
    Tone: ```{payload.get('tone')}```\

    3. Write the call to action in a clear and compelling manner using persuasive language and techniques to encourage the reader to take action.\

    4. Provide the result in HTML format.
    """
    return completion(prompt)


def generateCopywritingFrameworkAIDA(payload: any):
    prompt = f"""
    Perform the following actions:\
    1 - Generate a copywriting framework using AIDA (Attention, Interest, Desire, Action) for a product or brand, described in the following text delimited by triple backticks.\
    Description: ```{payload.get('description')}```\

    2 - Use the desired language and tone for the copywriting framework.\
    Language: ```{payload.get('language')}```\
    Tone: ```{payload.get('tone')}```\

    3 - Ensure that the generated copy grabs the attention of the audience, creates interest in the product or brand, builds desire for the product or brand, and creates a sense of urgency to take action.\

    4 - Provide the result in HTML format.
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


def generateEmail(payload: any):
    prompt = f"""
    Perform the following actions:\
    1 - Generate an email based on the information provided in the text delimited by triple backticks.\
    Text: ```{payload.get('text')}```

    Language: ```{payload.get('language')}```\
    Tone: ```{payload.get('tone')}```

    Provide the result in HTML format.
    """
    return completion(prompt)


def generateYoutubeVideoDescription(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a YouTube video description based on the following text delimited by triple backticks in ```{payload.get('language')}``` language, with a tone that is ```{payload.get('tone')}```.\

    2 - Include a brief summary of the video content, highlighting the key points and main takeaways.\

    3 - Include relevant keywords and hashtags to optimize the video for search engines.\

    4 - Use persuasive language to encourage viewers to watch the video and to subscribe to your channel.\

    5 - Include a call-to-action, such as asking viewers to leave a comment or to check out a related video or website.\

    6 - Output the result in HTML format.

    Text:
    ```{payload.get('videoTitle')}```
    """
    return completion(prompt)


def generateYoutubeChannelDescription(payload):
    prompt = f"""
    Perform the following actions:\
    1 - Generate a YouTube channel description for a channel based on the following text delimited by tripple backticks in {prompt.language} language with a tone that is {prompt.tone}.\
    2 - Include a detailed and clear overview of the channel, including the type of content, target audience, and unique selling points.\
    3 - Include a call-to-action, encouraging viewers to subscribe to the channel.\
    4 - Use appropriate keywords to optimize the channel description for search engines and make sure to align the tone with the channel's purpose and target audience.\
    5 - Output the result in HTML format.

    Text:
    ```{payload.channelDescription}```       
    """


def generateTestimonialAndReview(payload):
    prompt = f"""
    Perform the following actions:\
    1 - Generate a testimonial or review for a product or service described in the text delimited by tripple backticks with a review title of ```{payload.reviewTitle}```.\
    2 - The testimonial or review should be in ```{payload.language}``` language, with a tone that is ```{payload.tone}```.\
    3 - Make sure to include specific details and examples about the product or service being reviewed.\
    4 - Highlight the key benefits and features of the product or service that you found useful.\
    5 - Use persuasive language to encourage others to try the product or service.\
    6 - Include overall rating and recommendation for the product or service.\
    7 - Output the result in HTML format.

    Text:
    ```{payload.productName}```
    """
    return completion(prompt)


def generateTagLineAndHeadline(payload):
    prompt = f"""
    Perform the following actions:\
    1 - Generate a tagline and headline based on the following key points described in the text delimited by tripple backticks.
    2 - The language should be in ```{payload.language}```, with a tone that is ```{payload.tone}```.\
    3 - Make sure to include key words and phrases that accurately reflect the brand or product being promoted.\
    4 - Also, make sure that the tagline and headline are concise and easily understandable by the target audience.\
    5 - Use persuasive language to create a sense of urgency and inspire the audience to take action.\
    6 - Ensure that the tagline and headline are unique and memorable in order to make a lasting impression.\
    7 - Output the result in HTML format.
    
    Text:
    ```{payload.keyPoints}```
    """
    return completion(prompt)


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


def generateEmailSubjectLine(payload):
    pass


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


def generateReplyToReviewsAndMessages(payload):
    pass


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


def generatePostAndCaptionIdea(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a post and caption idea based on the provided information.
    2 - Use the following text delimited by triple backticks to describe the content of the post:
    ```{payload['postContent']}```
    3 - Consider the target audience and the platform where the post will be shared.
    4 - Create an engaging and attention-grabbing caption that complements the post content.
    5 - Use hashtags or keywords relevant to the post to increase visibility.
    6 - Ensure the caption is concise, compelling, and aligned with the desired tone.
    7 - Output the generated post and caption idea.

    Information:
    Platform: {payload['platform']}
    Target Audience: {payload['targetAudience']}
    """
    return completion(prompt)


def generateProductDescription(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a compelling product description that effectively showcases the features and benefits of the product.
    2 - Describe the product in detail, highlighting its key functionalities, specifications, and unique selling points.
    3 - Clearly communicate how the product solves a problem or fulfills a need for the target audience.
    4 - Emphasize the advantages and benefits that set the product apart from competitors.
    5 - Use persuasive language to engage and captivate potential customers.
    6 - Consider the target market and tailor the description to resonate with their interests and preferences.
    7 - Output the generated product description in a clear and concise format.

    Product Name: {payload['product_name']}
    Product Category: {payload['product_category']}
    Target Audience: {payload['target_audience']}
    Product Description: {payload['product_description']}
    """
    return completion(prompt)


def generateProductDescriptionWithBulletPoints(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a product description with bullet points based on the provided information.
    2 - Use the following text delimited by triple backticks to describe the product:
    ```{payload['productDescription']}```
    3 - Include key features, benefits, and specifications of the product.
    4 - Format the description using bullet points to make it clear and easy to read.
    5 - Ensure the description highlights the unique selling points and value proposition of the product.
    6 - Output the generated product description in HTML format.

    Information:
    Product Name: {payload['productName']}
    Product Category: {payload['productCategory']}
    Price: {payload['price']}
    """
    return completion(prompt)


def generateSeoMetaTitle(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate an SEO meta title based on the provided information.
    2 - Use the following text delimited by triple backticks to describe the content or topic for which the SEO meta title is needed:
    ```{payload['content']}```
    3 - Consider the target audience and the purpose of the content when crafting the meta title.
    4 - Ensure the meta title is concise, compelling, and accurately reflects the content's topic or main idea.
    5 - Incorporate relevant keywords or phrases to improve search engine visibility.
    6 - Optimize the meta title length to fit within the recommended character limit for search engines.
    7 - Output the generated SEO meta title.

    Information:
    Target Audience: {payload['targetAudience']}
    Content Type: {payload['contentType']}
    """
    return completion(prompt)


def generateBrandName(payload):
    # [Specify the desired brand image, e.g., modern, sophisticated, playful]
    # [Describe the purpose or mission of the brand
    prompt = f"""
    Perform the following actions:\
    1 - Generate a brand name that reflects the desired brand image and purpose. Consider the target audience and desired tone and style.\
    2 - The output should be a brand name that resonates with customers and effectively represents the brand's identity.\
    3 - Utilize creativity and uniqueness to craft a memorable and distinctive brand name.\
    4 - Consider any specific keywords or themes that should be incorporated into the brand name.\
    5 - Output the result in HTML format\

    Instructions:\

    Desired Brand Image: The specified brand image is described in the following text delimited by tripple backticks Brand Image:```{payload.get('brandImage')}```\
    Brand Purpose: The purpose or mission of the brand is described in the following text delimited by tripple backticks Purpose:```{payload.get('purpose')}```\
    Target Audience: The target audience for the brand is described in the following text delimited by tripple backticks Audience:```{payload.get('audience')}```\
    Tone and Style: The desired tone and style of the brand name is described in the following text delimited by tripple backticks Audience:```{payload.get('tone')}```\
    Language: The language of the brand name is described in the following text delimited by tripple backticks Audience:```{payload.get('language')}```\
    Generate a compelling brand name that aligns with the provided instructions. The brand name should effectively represent the desired brand image, purpose, target audience, and tone. Ensure it is unique, memorable, and capable of resonating with customers.
    """
    return completion(prompt)


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


def generateSocialMediaAd(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate an engaging social media ad that grabs attention and drives clicks.
    2 - Describe the product, service, or offer in a compelling and concise way.
    3 - Highlight the key features, benefits, or promotions to entice the audience.
    4 - Use eye-catching visuals, such as images or videos, to enhance the ad's appeal.
    5 - Include a clear call-to-action that directs users to take the desired action (e.g., visit a website, make a purchase).
    6 - Tailor the ad to the specific social media platform and its audience.
    7 - Output the generated social media ad in the appropriate format for the chosen platform (e.g., image file, video file).

    Product, Service, or Offer: {payload['product']}
    Key Features or Benefits: {payload['features']}
    Desired Action: {payload['action']}
    Platform: {payload['platform']}
    """
    return completion(prompt)


def generateLandingPageCopy(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate compelling copy for a landing page that captures the attention of visitors.
    2 - Describe the product, service, or offer in a concise and persuasive manner.
    3 - Highlight the unique value proposition and key benefits of the offering.
    4 - Create a sense of urgency or exclusivity to encourage immediate action.
    5 - Use customer testimonials or social proof to build trust and credibility.
    6 - Incorporate persuasive language and call-to-action statements to guide visitors to take the desired action.
    7 - Ensure the copy is aligned with the target audience and matches the overall tone and branding.
    8 - Output the generated landing page copy in HTML format.

    Product, Service, or Offer: {payload['product']}
    Target Audience: {payload['audience']}
    Desired Action: {payload['action']}
    Key Benefits: {payload['benefits']}
    """

    return completion(prompt)


def generateFacebookAd(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a Facebook ad for a product or service based on the provided information.
    2 - The ad should be attention-grabbing, compelling, and optimized for the Facebook platform.
    3 - Consider the target audience demographics, their interests, and pain points when crafting the ad.
    4 - Use persuasive language, eye-catching visuals, and a clear value proposition to capture the audience's attention and generate interest.
    5 - Highlight the key features, benefits, and unique selling points of the product or service to create a desire for it.
    6 - Include a strong call-to-action that prompts the audience to take the desired action, such as visiting a website or making a purchase.
    7 - Make use of appropriate ad formats, such as images, videos, or carousels, to convey the message effectively.
    8 - Output the resulting Facebook ad in HTML format.

    Product or Service Description:
    {payload['description']}

    Target Audience:
    {payload['audience']}

    Desired Tone:
    {payload['tone']}
    """
    return completion(prompt)


def generateInstagramCaption(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate an engaging Instagram caption for a post based on the provided information.
    2 - The caption should be creative, attention-grabbing, and aligned with the content of the post.
    3 - Consider the target audience, the purpose of the post, and the desired tone when crafting the caption.
    4 - Use a combination of compelling words, emojis, hashtags, and mentions to enhance the caption's appeal.
    5 - Reflect the personality of the brand or individual behind the post while maintaining authenticity.
    6 - Include a clear call-to-action that encourages the audience to engage with the post, such as liking, commenting, or sharing.
    7 - Make sure the caption is concise and easily readable within the character limit of an Instagram caption.
    8 - Output the resulting Instagram caption.

    Post Content:
    {payload['content']}

    Target Audience:
    {payload['audience']}

    Desired Tone:
    {payload['tone']}
    """
    return completion(prompt)


def generatePodcastIdea(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a unique and captivating podcast idea based on the provided information.
    2 - Consider the target audience, niche, and overall theme of the podcast when brainstorming the idea.
    3 - Incorporate relevant keywords, trends, or current topics to make the podcast idea timely and appealing.
    4 - Highlight the main purpose or value proposition of the podcast, such as education, entertainment, or inspiring stories.
    5 - Ensure that the podcast idea is specific, concise, and easily understandable for potential listeners.
    6 - Include potential episode topics or segments that can be covered in the podcast to give a clearer picture of the content.
    7 - Output the resulting podcast idea.

    Podcast Niche:
    {payload['niche']}

    Target Audience:
    {payload['audience']}

    Main Theme:
    {payload['theme']}
    """
    return completion(prompt)


def generatedcastTitle(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a catchy and engaging podcast title based on the provided information.
    2 - Consider the podcast niche, target audience, and main theme when creating the title.
    3 - Use attention-grabbing words, intriguing phrases, or wordplay to make the title memorable and enticing.
    4 - Ensure that the title accurately represents the content and tone of the podcast.
    5 - Keep the title concise and easy to understand, avoiding overly complex or confusing wording.
    6 - Output the resulting podcast title.

    Podcast Niche:
    {payload['niche']}

    Target Audience:
    {payload['audience']}

    Main Theme:
    {payload['theme']}
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


def generatePressRelease(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a compelling press release based on the provided information.
    2 - Consider the news or announcement that needs to be conveyed.
    3 - Begin the press release with a strong headline and a concise introductory paragraph that grabs attention.
    4 - Provide relevant details, such as the who, what, when, where, and why of the news or announcement.
    5 - Include quotes from key individuals or stakeholders to add credibility and human interest.
    6 - Highlight the key benefits, features, or impact of the news or announcement.
    7 - Ensure the press release follows proper press release formatting and style.
    8 - Proofread and edit the press release for clarity, accuracy, and professionalism.
    9 - Output the resulting press release in HTML format.

    Press Release Title:
    {payload['title']}

    Press Release Content:
    {payload['content']}

    Language: {payload['language']}
    Tone: {payload['tone']}
    """
    return completion(prompt)


def generateVideoScript(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a video script.\
    2 - The video script should align with the following guidelines:"\
    3- Please cover the following main points in the video script in the text delimited by tripple backticks:\
       
       Key Points:\
       ```{payload.get('keyPoints')}```\
    4 - The video script should have a tone as described in the text delimited by angle brackets, appealing to target audience in the text delimited by tripple dashes."\
        
        Tone:\
        <{payload.get('tone')}>\

        Audience:\
        ---{payload.get('audience')}---\

    5 - The key messages to convey in the video script are in the following text delimited by XML tags. At the end, please include a call to action encouraging viewers to subscribe."\

        Message:
        <tag>{payload.get('message')}</tag>

    6 - The video script should be approximately have a duration mentioned in the following text delimited by backticks and formatted in a formated style, including scene descriptions, dialogue, and narration."\

        Duration:
        ```{payload.get('duration')}```

    7 - You are encouraged to provide a creative, engaging, and coherent video script that captures the viewers' attention and effectively conveys the desired messages."\
    8 - Output the result in HTML format 

    """
    return completion(prompt)


def generateWebsiteCopy(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate persuasive website copy based on the provided information.
    2 - Consider the purpose and target audience of the website.
    3 - Begin with a compelling headline that grabs attention and conveys the main message.
    4 - Clearly articulate the unique value proposition and key benefits of the product, service, or brand.
    5 - Organize the copy into sections, highlighting different features, solutions, or offerings.
    6 - Use persuasive language, storytelling, and customer testimonials to build trust and credibility.
    7 - Incorporate relevant keywords for search engine optimization (SEO).
    8 - Create a sense of urgency or exclusivity by emphasizing limited-time offers or unique selling points.
    9 - Ensure the copy is concise, easy to read, and scannable.
    10 - Proofread and edit the copy for grammar, spelling, and coherence.
    11 - Output the resulting website copy in HTML format.

    Website Purpose: {payload['purpose']}
    Target Audience: {payload['audience']}
    Main Message: {payload['message']}
    Key Features/Benefits:
    {payload['features']}

    Language: {payload['language']}
    Tone: {payload['tone']}
    """
    return completion(prompt)


def generateNewsletterIdea(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a newsletter idea based on the provided information.
    2 - Consider the target audience and purpose of the newsletter.
    3 - Identify a relevant and engaging topic that would interest the subscribers.
    4 - Outline the key sections or topics to include in the newsletter.
    5 - Provide valuable content, such as industry insights, tips, news, or updates.
    6 - Incorporate visuals, such as images or infographics, to enhance the newsletter's appeal.
    7 - Include a call-to-action to encourage reader engagement or conversion.
    8 - Personalize the newsletter by addressing the subscribers by name, if applicable.
    9 - Ensure the tone and language align with the brand and audience.
    10 - Format the newsletter in a visually appealing and easy-to-read manner.
    11 - Proofread and edit the content for clarity, grammar, and coherence.
    12 - Output the resulting newsletter idea in a suitable format.

    Target Audience: {payload['audience']}
    Newsletter Purpose: {payload['purpose']}
    Key Topics/Ideas:
    - Idea 1: {payload['topic1']}
    - Idea 2: {payload['topic2']}
    - Idea 3: {payload['topic3']}

    Language: {payload['language']}
    Tone: {payload['tone']}
    """
    return completion(prompt)


def generateNewsletterTitle(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a catchy and attention-grabbing title for a newsletter.
    2 - Consider the target audience, purpose, and content of the newsletter.
    3 - Create a title that reflects the main theme or topic of the newsletter.
    4 - Use language and words that evoke curiosity, interest, or excitement.
    5 - Keep the title concise, clear, and easy to understand.
    6 - Make sure the title aligns with the brand and the tone of the newsletter.
    7 - Output the resulting newsletter title.

    Target Audience: {payload['audience']}
    Newsletter Purpose: {payload['purpose']}
    Key Topics/Ideas: {payload['topics']}

    Language: {payload['language']}
    Tone: {payload['tone']}
    """
    return completion(prompt)


def generateGenerateSalesCopy(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate compelling and persuasive sales copy for a product or service.
    2 - Consider the target audience, product features, and unique selling points.
    3 - Highlight the benefits and value proposition of the product/service.
    4 - Use persuasive language and techniques to create a sense of urgency and desire.
    5 - Craft a strong call-to-action that encourages the reader to take immediate action.
    6 - Ensure the sales copy aligns with the brand and desired tone.
    7 - Output the resulting sales copy.

    Product/Service: {payload['product']}
    Target Audience: {payload['audience']}
    Unique Selling Points: {payload['usp']}
    Key Features: {payload['features']}

    Language: {payload['language']}
    Tone: {payload['tone']}
    """
    return completion(prompt)


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


def generateSocialMediaPost(payload):
    # posttype such as a text-based post, image-based post, or a combination.
    # objective  such as promoting a product, sharing a news update, or encouraging user engagement.
    # target audience on demographics, interests, and preferences.
    prompt = f"""
    Instruction: Generate Social Media Post\

    Using the available information, generate a creative and engaging social media post that aligns with the desired goals and target audience. Please follow these guidelines:\
    
    Platform: The social media platform for which the post is intended is described in the text delimited by tripple backtics Platform:```{payload.get('platform')}```.\
    Post Type: The type is described in the text delimited by tripple backticks ```{payload.get('postType')}```\
    Objective: The main objective of the post is described in the following text delimited by tripple backticks Objective:```{payload.get('objective')}\
    Target Audience: The target audience is described in the following text delimited by tripple backticks Audience:```{payload.get('audience')}``\
    Tone and Style: The desired tone and style of the post is described in the following text delimited by tripple backticks ```{payload.get('tone')}```\
    Key Message: The main message or key points that need to be conveyed in the post are described in the following text delimted by tripple backticks Key Message```{payload.get('keyMessage')}```.\
    Call to Action: Specify the desired action you want the audience to take (e.g., visit a website, like/comment/share the post).
    Output: Output the result in HTML format 
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


def generateYouTubeIdea(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a YouTube video idea based on the provided information.
    2 - The video should be in the {payload['language']} language with a {payload['tone']} tone.
    3 - Consider the target audience and their interests when generating the idea.
    4 - Ensure the idea is engaging, informative, and aligned with the channel's theme.
    5 - Output the generated video idea in HTML format.

    Information:
    Channel Name: {payload['channelName']}
    Channel Theme: {payload['channelTheme']}
    Previous Video Topics: {payload['previousVideoTopics']}
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


# TODO prompt = f"""
# Perform the following actions:
# 1 - Generate configuration files and deployment scripts for automating CI/CD pipelines.
# 2 - Based on the provided project requirements, define the required stages and steps in the CI/CD pipeline.
# 3 - Specify the desired tools and technologies for CI/CD, such as Jenkins, GitLab CI/CD, or AWS CodePipeline.
# 4 - Include steps for building, testing, and deploying the application or software.
# 5 - Configure integration with version control systems, artifact repositories, and deployment environments.
# 6 - Ensure scalability, security, and best practices in the CI/CD pipeline configuration.
# 7 - Output the generated configuration files and deployment scripts.

# Project Requirements:
# {payload['requirements']}

# CI/CD Tools and Technologies: {payload['tools']}

# Additional Notes or Requirements: {payload['notes']}
# """
