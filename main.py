import nltk
import re
from tkinter import *
from evaluation import split_dataset, evaluate_trigram_model
import sys
import customtkinter as ctk 
from AutoFillingGeneral import AutoFilling as generalAF  
import time
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
sys.stdout.reconfigure(encoding='utf-8')

def read_corpus(file_path):
    start = time.time()
    file = open(file_path, 'r', encoding="utf-8")
    corpus_ = file.read()
    file.close()
    print(f"Reading corpus took {time.time() - start:.2f} seconds")
    return corpus_


# Auto Filling Text Class by Trigrams Model
class AutoFilling:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.trigrams = {}

    # Tokenization process for text
    def tokenize(self):
        start = time.time()
        print('Tokenization process running now.')
        self.text = re.sub(r'\s+', ' ', self.text)  # Replace multiple spaces with a single space
        self.text = re.sub(r'[^\w\s]', '', self.text)  # Remove non-alphanumeric characters except spaces
        self.tokens = nltk.word_tokenize(self.text)
        print(f"Tokenization took {time.time() - start:.2f} seconds")

    # Generate all trigrams and count each word after it
    def generate_trigrams(self):
        start = time.time()
        print('Generating trigrams process running now.')
        if len(self.tokens) > 0:
            for i in range(len(self.tokens)-2):  # Take 2 words
                seq_list = self.tokens[i:i+2]
                seq = " ".join(seq_list)

                # Map each 2 words with frequency of the third word
                if seq in self.trigrams:
                    self.trigrams[seq][self.tokens[i + 2]] = self.trigrams[seq].get(self.tokens[i + 2], 0) + 1
                else:
                    self.trigrams[seq] = {}
                    self.trigrams[seq][self.tokens[i + 2]] = 1

        else:
            print('You should tokenize the text first! Tokenization process running now.')
            self.tokenize()
            self.generate_trigrams()
        print(f"Generating trigrams took {time.time() - start:.2f} seconds")

    # Calculate the probability of each trigram
    def calculate_prob(self):
        start = time.time()
        if not self.trigrams:  # Check if trigrams are empty
            print('Trigrams not generated yet, generating now.')
            self.generate_trigrams()
        
        print('Calculating probabilities now.')
        for prev_seq in self.trigrams:
            total_prev_cnt = sum(self.trigrams[prev_seq].values())
            for key in self.trigrams[prev_seq]:
                self.trigrams[prev_seq][key] /= total_prev_cnt
            self.trigrams[prev_seq] = sorted(self.trigrams[prev_seq].items(), key=lambda x: (x[1], x[0]), reverse=True)
        print(f"Calculating probabilities took {time.time() - start:.2f} seconds")

    # Take input and suggest the next word after it
    def suggest_next_trigrams(self, str_input):
        res = []
        str_input = str_input.strip()
        list_input = str_input.split(" ")
        if len(list_input) >= 2:
            last_2_words = (list_input[-2] + " " + list_input[-1])
            if last_2_words in self.trigrams:
                for predicted_word, freq in self.trigrams[last_2_words]:
                    res.append(predicted_word)
                    if len(res) == 10:  # Limit number of suggestions
                        break
        return res


# --------------------------------The Main---------------------------------------

# Reading English dataset
corpus = read_corpus('data/10_million_words.txt')  # this file contains 10 million words from 14441 articles

AutoFillingObj = AutoFilling(corpus)  # Generate Trigrams
AutoFillingObj.tokenize()
AutoFillingObj.generate_trigrams()
AutoFillingObj.calculate_prob()

# Replace this part where you calculate probabilities for the bigram model
AutoFillingObjBi = generalAF(corpus, 2)  # Generate Bigrams
AutoFillingObjBi.tokenize()
AutoFillingObjBi.generate_ngrams()
AutoFillingObjBi.calculate_probabilities()  # Use this method for bigrams


# Reading Arabic dataset (Extra)
corpusAr = read_corpus('data/arabic_cleaned_data.txt')  # this file contains 2 million words from 6499 articles

train_text_ar, test_tokens_ar = split_dataset(corpusAr)


# Train the Trigram model
AutoFillingObjAr = AutoFilling(corpusAr)  # Generate Trigrams
AutoFillingObjAr.tokenize()
AutoFillingObjAr.generate_trigrams()
AutoFillingObjAr.calculate_prob()

# Train the Bigram model
AutoFillingObjArBi = generalAF(corpusAr, 2)  # Generate Bigrams
AutoFillingObjArBi.tokenize()
AutoFillingObjArBi.generate_ngrams()
AutoFillingObjArBi.calculate_probabilities()

# Evaluation of the Arabic Trigram model
precision_ar, mrr_ar = evaluate_trigram_model(AutoFillingObjAr, test_tokens_ar, k=3)

# Output the evaluation metrics for Trigram Model
print(f"Arabic Trigram Evaluation:\nPrecision@3: {precision_ar:.3f} | MRR: {mrr_ar:.3f}")

# --------------------------------GUI------------------------------------------

# Track if input entered and suggest result
def auto_filling_suggest(*args):
    # get input from the entry & delete the list box
    str_input = str_entry.get()
    list_box.delete(0, END)
    try:
        input_str = str_input.strip()
        my_list = []
        # if there is at least one word
        if len(input_str) > 0:

            # check if English text
            if 'a' <= input_str[0] <= "z" or 'A' <= input_str[0] <= 'Z':
                if ' ' not in input_str:  # if one word apply bigrams
                    my_list = AutoFillingObjBi.suggest_next_words(input_str)
                else:  # if multiple words apply trigrams
                    my_list = AutoFillingObj.suggest_next_trigrams(input_str)

            # check if Arabic text
            else:
                if ' ' not in input_str:  # if one word apply bigrams
                    my_list = AutoFillingObjArBi.suggest_next_words(input_str)
                else:  # if multiple words apply trigrams
                    my_list = AutoFillingObjAr.suggest_next_trigrams(input_str)
        else:
            pass

        # show list of suggestions
        for element in my_list:
            element = input_str + " " + element
            list_box.insert(END, element)
            list_box.place(height=9, width=55)
            list_box.listbox_is_showing = True
            list_box.pack(pady=3)
    except KeyError:
        pass


# Select one of the suggestion List
def select_result(event):
    event = event.widget
    text_input.set(event.get(int(event.curselection()[0])))


# these Functions for focus on and out the input entry
def on_enter(e):
    str_entry.configure(border_width=2)


def on_leave(e):
    str_entry.configure(border_width=0)


# Starting of generating GUI with customtkinter
ctk.set_appearance_mode("System")  # Optional: Set dark or light mode
ctk.set_default_color_theme("blue")  # Optional: Set default color theme

AutoFillingWindow = ctk.CTk()  # Using CustomTkinter window
AutoFillingWindow.title("Auto Filling App")
AutoFillingWindow.geometry('650x350')
AutoFillingWindow.resizable(False, False)

# Removed google.png image and label

text_input = StringVar()
str_entry = ctk.CTkEntry(
    AutoFillingWindow,
    font=ctk.CTkFont(family="Arial", size=16),  # Fixed font type
    textvariable=text_input,
    width=300,
    height=40
)
str_entry.pack(pady=40)  # Added more padding since no image above
str_entry.bind("<FocusIn>", on_enter)
str_entry.bind("<FocusOut>", on_leave)

list_box = Listbox(AutoFillingWindow, height=9, width=55, bd=0, font=("Arial", 12))
list_box.configure(bg=AutoFillingWindow["bg"],fg="#f0f0f0", highlightthickness=0, relief="flat") 
list_box.place_forget()
list_box.listbox_is_showing = False

list_box.bind('<<ListboxSelect>>', select_result)
text_input.trace('w', auto_filling_suggest)

AutoFillingWindow.mainloop()