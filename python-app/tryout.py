import nltk
nltk.download('punkt')
import re
from nltk.tokenize import RegexpTokenizer

def split_text_by_dividers(text, dividers):
    # Create a regular expression pattern to match the dividers
    divider_pattern = '|'.join(map(re.escape, dividers))
    
    # Use the RegexpTokenizer to split the text based on the dividers
    tokenizer = RegexpTokenizer(f'[^{divider_pattern}]+|[{divider_pattern}]')
    tokens = tokenizer.tokenize(text)
    
    # Remove any empty strings from the list of tokens
    tokens = [token.strip() for token in tokens if token.strip()]
    
    return tokens

# Example usage
text = "This is, a test - sentence! With: various? dividers."

# Define a list of dividers you want to use
dividers = [',', '-', '!', ':', '?']

tokens = split_text_by_dividers(text, dividers)
print(tokens)
