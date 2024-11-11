# import pandas as pd

# data = pd.read_csv("C:/Users/kappiah/Desktop/Labs/Autocorrect Tool/ngram_frequency_by_letter.csv")

# average_frequencies = data.groupby("ngram")["frequency"].mean()

# letter_frequencies = average_frequencies.to_dict()



import string

words_by_letter = {letter:[] for letter in string.ascii_lowercase}
names_by_letter = {letter:[] for letter in string.ascii_uppercase}

with open("en_US-large.txt", "r") as file:
    for line in file:
        word = line.strip()
        if word:
            if word[0].isupper():
                first_letter = word[0]
                if first_letter in names_by_letter:
                    names_by_letter[first_letter].append(word)
            else:
                first_letter = word[0]
                if first_letter in words_by_letter:
                    words_by_letter[first_letter].append(word)

for letter, word_list in words_by_letter.items():
    with open(f"{letter}_words.txt", "w") as file:
        file.write('\n'.join(sorted(word_list)))

# for letter, name_list in names_by_letter.items():
#     with open(f"{letter}_names.txt", "w") as file:
#         file.write('\n'.join(sorted(name_list)))



from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load pre-trained model and tokenizer
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def get_word_probability(word):
    # Add context to make the language model more accurate
    input_text = f"The word '{word}' appears frequently in"
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model(**inputs, labels=inputs["input_ids"])
    loss = outputs.loss
    word_probability = torch.exp(-loss).item()
    return word_probability

# Test the function with a few words
words = ["example", "data", "frequency", "analysis"]
word_probs = {word: get_word_probability(word) for word in words}

print("Word Probabilities:", word_probs)
