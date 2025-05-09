import nltk
import re
from collections import defaultdict


class AutoFilling:
    def __init__(self, text: str, n: int = 3):
        self.raw_text = text
        self.tokens = []
        self.n = n
        self.ngrams = defaultdict(dict)
        self.MAX_SUGGESTIONS = 10

    def tokenize(self):
        try:
            print('Tokenization process running now.')
            cleaned_text = re.sub(r'\W+', ' ', self.raw_text)  # Remove non-word characters
            self.tokens = nltk.word_tokenize(cleaned_text.lower())
        except Exception as e:
            print(f"Tokenization failed: {e}")

    def generate_ngrams(self):
        if not self.tokens:
            print('Tokens not found. Running tokenization.')
            self.tokenize()
            if not self.tokens:
                raise ValueError("No tokens generated from the input text.")

        print('Generating n-grams.')
        for i in range(len(self.tokens) - self.n + 1):
            prefix = ' '.join(self.tokens[i:i + self.n - 1])
            next_word = self.tokens[i + self.n - 1]
            self.ngrams[prefix][next_word] = self.ngrams[prefix].get(next_word, 0) + 1

    def calculate_probabilities(self):
        if not self.ngrams:
            print('N-grams not found. Generating them first.')
            self.generate_ngrams()

        print('Calculating probabilities.')
        for prefix, next_words in self.ngrams.items():
            total_count = sum(next_words.values())
            if total_count == 0:
                continue
            prob_dist = {word: count / total_count for word, count in next_words.items()}
            # Sort by probability, then alphabetically
            self.ngrams[prefix] = sorted(prob_dist.items(), key=lambda x: (-x[1], x[0]))

    def suggest_next_words(self, input_text: str):
        if not input_text or not isinstance(input_text, str):
            raise ValueError("Input text must be a non-empty string.")

        input_text = input_text.strip().lower()
        tokens = input_text.split()

        if len(tokens) < self.n - 1:
            print(f"Please provide at least {self.n - 1} words for prediction.")
            return []

        prefix = ' '.join(tokens[-(self.n - 1):])
        suggestions = self.ngrams.get(prefix, [])

        if not suggestions:
            print(f"No suggestions found for prefix: '{prefix}'")
            return []

        return [word for word, _ in suggestions[:self.MAX_SUGGESTIONS]]
