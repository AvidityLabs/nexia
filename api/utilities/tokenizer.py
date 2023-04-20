"""_summary_
    Read the input string
Tokenize the string into words
Create an empty list called "sentence"
For each word in the list of words:
a. If the word is a punctuation mark, ignore it
b. If the word is a verb, capitalize it and add "the" before it
c. If the word is a noun, add "a" or "an" before it depending on the first letter of the noun
d. Otherwise, add the word to the "sentence" list
Join the words in the "sentence" list with spaces to create the final sentence
Add a period at the end of the sentence
    """

import re

def arrange_sentence(sentence):
    # Split the input string into a list of words using whitespace as the delimiter.
    words = re.findall(r'\b\w+\b', sentence)
    
    # Create an empty list to hold the words that will make up the sentence.
    sentence_words = []
    
    # Loop through each word in the list.
    for i, word in enumerate(words):
        # Check if the word is the first word in the sentence.
        if i == 0:
            sentence_words.append(word.capitalize())
        else:
            sentence_words.append(word.lower())
            
            # If the word is not the last word in the sentence.
            if i < len(words) - 1:
                # Check if the next word is a punctuation mark.
                if re.match(r'[^\w\s]', words[i+1]):
                    sentence_words.append(words[i+1])
                else:
                    sentence_words.append(' ')
            # If the word is the last word in the sentence.
            else:
                sentence_words.append('.')
                
    # Join the list of sentence words into a single string to create the readable sentence.
    readable_sentence = ''.join(sentence_words)
    
    # Find the first verb in the original sentence.
    first_verb = re.findall(r'\b\w+(?:ing|ed|s)?\b', sentence)[0]
    
    # Generate a sentence as an instruction.
    if first_verb.endswith('ing') or first_verb.endswith('s'):
        instruction = 'Please ' + readable_sentence.replace(first_verb, '______')
    else:
        instruction = 'Please rewrite ' + readable_sentence.replace(first_verb, '______')
        
    return readable_sentence, instruction


sentence = "the quick BROWN fox jumps OVER the lazy DOG. It's a beautiful day!"
readable, instruction = arrange_sentence(sentence)

print(readable)    # The quick brown fox jumps over the lazy dog. It's a beautiful day.
print

