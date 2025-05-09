# Auto Filling Bilingual Autocomplete App

This project implements a bilingual (Arabic and English) autocomplete system that provides suggestions based on user input. The system uses a combination of Natural Language Processing (NLP) models to predict the next word(s) in a given input. The application is built with `CustomTkinter` for the GUI and uses various algorithms like n-grams and BERT-based models to generate the suggestions.

## Project Structure

```autocomplete_app/
├── data/
│ ├── extract.py # Extracts the first column from CSV and saves it to a text file
│ └── arabic_data_cleaned.txt # Cleaned Arabic data used for generating autocomplete suggestions
├── AutoFillingGeneral.py/
├── main.py # Main script to run the app
```

## How to Run the Project

1. **Install Dependencies:**
   
   First, install all necessary Python dependencies:


## How to Run the Project

1. **Install Dependencies:**
   
   First, install all necessary Python dependencies:

2. **Prepare the Data:**

    The data/extract.py script processes the input dataset and extracts the first column. It saves the cleaned Arabic data into arabic_data_cleaned.txt. Ensure that the appropriate CSV file path is provided in the script before running.

3. **Run the App:**

    After the data is prepared, you can run the project using the following command:

    ```python main.py```
This will launch the application, and you can start typing to receive autocomplete suggestions

Data
----

The project uses two primary datasets for Arabic and English data:

-   **Arabic Data**:

    -   The data for Arabic text is cleaned and stored in the `data/arabic_data_cleaned.txt` file.

    -   The dataset is derived from Kaggle's [Arabic Text Classification Dataset](https://www.kaggle.com/datasets/saurabhshahane/arabic-classification).

-   **English Data**:

    -   The English dataset used for generating autocomplete suggestions is obtained from [English Corpus](https://www.english-corpora.org/).

NLP Models
----------

### N-Grams

N-grams are used for predicting the next word(s) in a sequence. The following models are used in the project:

-   **Bigrams**: Used when there is only one word in the input.

-   **Trigrams**: Used when there are multiple words in the input.

These models are trained on the provided datasets (Arabic and English) to suggest the most likely next words.


GUI
---

The app uses the `CustomTkinter` library to provide a modern and user-friendly interface. It consists of:

-   An input field where the user can type text.

-   A listbox that shows the suggested next words based on the input.

-   Arrow keys to navigate through the suggestions and `Enter` to select a suggestion.

The GUI is responsive and changes based on the input type (Arabic or English).

Features
--------

-   Bilingual (Arabic and English) autocomplete.

-   Suggests the next word(s) based on n-gram models or BERT for Arabic.

-   Uses n-grams for both English and Arabic text input.

-   Modern GUI built with `CustomTkinter`.

-   Arrow key navigation for suggestions.

Requirements
------------

-   `customtkinter`

-   `tkinter`



-   `numpy`

-   `pandas`

-   `nltk`

-   `scikit-learn`