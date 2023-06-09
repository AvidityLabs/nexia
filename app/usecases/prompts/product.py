from api.utilities.openai.utils import completion

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