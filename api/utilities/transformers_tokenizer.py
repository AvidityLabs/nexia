from transformers import AutoTokenizer


def calculate_tokens(text):
    # Instantiate a tokenizer for a specific pre-trained model
    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
    # Use the tokenizer to tokenize the input string
    tokens = tokenizer.tokenize(text)

    # Get the number of tokens in the input string
    num_tokens = len(tokens)
    return num_tokens
