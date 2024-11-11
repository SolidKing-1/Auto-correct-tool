import nltk
import string
from nltk.corpus import words
from script import letter_frequencies


# Downloading a corpus of English Words from NLTK library
# nltk.download('words')

vocabulary = set(words.words()) # Create a set to speed up "look-up" operations when we check if a word is spelled correctly
# print(vocabulary)
# print(f"Vocabulary size: {len(vocabulary)}")

#  Tokenization
def tokenize(text):
    tokens = text.split()
    tokens = [token.strip(".,!?:;") for token in tokens]
    return tokens

def detect_errors(tokens, vocabulary):
    errors = [token for token in tokens if token.lower() not in vocabulary]
    return errors

def generate_edits(word):
    letters = string.ascii_lowercase
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

    deletes = [L + R[1:] for L, R in splits if R]

    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]

    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]

    inserts = [L + c + R for L, R in splits for c in letters]

    return set(deletes + transposes + replaces + inserts)

def calculate_letter_score(word):
    score = sum(letter_frequencies.get(char, 0) for char in word.lower())
    return score

def levenshtein_distance(word1, word2):
    dp = [[0] * (len(word2) + 1) for _ in range(len(word1) + 1)]

    for i in range(len(word1) + 1):
        dp[i][0] = i
    for j in range(len(word2) + 1):
        dp[0][j] = j

    for i in range(1, len(word1) + 1):
        for j in range(1, len(word2) + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[-1][-1]

def get_suggestions(word, vocabulary):
    edits = generate_edits(word)

    valid_suggestions = [edit for edit in edits if edit in vocabulary]

    if not valid_suggestions:
        return word

    suggestions_with_scores = []
    for suggestion in valid_suggestions:
        letter_score = calculate_letter_score(suggestion)
        lev_distance = levenshtein_distance(word, suggestion)
        combined_score = (letter_score * 0.7) - (lev_distance * 0.3)
        suggestions_with_scores.append((suggestion, combined_score))

    ranked_suggestions = sorted(suggestions_with_scores, key=lambda x: x[1], reverse=True)
    
    return [suggestion for suggestion, score in ranked_suggestions]


def autocorrect(text, vocabulary):
    tokens = tokenize(text)

    errors = detect_errors(tokens, vocabulary)

    corrected_tokens = [
        get_suggestions(word, vocabulary)[0] if word in errors else word for word in tokens
    ]

    corrected_text = " ".join(corrected_tokens)
    return corrected_text


input_text = "Hellu"
corrected_text = autocorrect(input_text, vocabulary)
print("Corrected Text:", corrected_text)

# tokens = tokenize(input_text)
# errors = detect_errors(tokens, vocabulary)

# print("Tokens:",tokens)
# print("Errors:", errors)
# print("Generated edits for exmple:", generate_edits("ic"))
# print("suggestions for exmple:", get_suggestions("ic", vocabulary))