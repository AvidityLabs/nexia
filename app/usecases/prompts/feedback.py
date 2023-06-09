from api.utilities.openai.utils import completion

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


def generateReplyToReviewsAndMessages(payload):
    pass
