from api.utilities.openai.utils import completion

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