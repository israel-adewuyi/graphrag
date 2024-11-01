import tiktoken

def get_token_count(text: str) -> int:
    # Load the encoding for a specific model
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    # Tokenize the text
    tokens = encoding.encode(text)

    return len(tokens)