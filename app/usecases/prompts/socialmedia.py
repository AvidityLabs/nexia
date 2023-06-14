from api.utilities.openai.utils import completion

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