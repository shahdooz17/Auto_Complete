# Auto Filling Bilingual Autocomplete App

This project implements a bilingual (Arabic and English) autocomplete system that provides suggestions based on user input. The system uses a combination of Natural Language Processing (NLP) models to predict the next word(s) in a given input. The application is built with `CustomTkinter` for the GUI and uses algorithms like n-grams and a fine-tuned BERT model for Arabic autocomplete.

## Project Structure

```bash
autocomplete_app/
├── data/
│   ├── extract.py                # Extracts the first column from CSV and saves it to a text file
│   └── arabic_data_cleaned.txt   # Cleaned Arabic data used for generating autocomplete suggestions
├── AutoFillingGeneral.py         # Core model and logic
├── main.py                       # Main script to run the app `
├── evaluate.py                       # Main script to run the app `
```

How to Run the Project
----------------------

1.  **Install Dependencies:**

    Install all necessary Python dependencies:


    `pip install -r requirements.txt`

2.  **Prepare the Data:**

    Run `data/extract.py` to process the input dataset and extract the first column. It saves the cleaned Arabic data into `arabic_data_cleaned.txt`. Ensure that the correct CSV file path is set in the script.

3.  **Run the App:**


    `python main.py`

    This will launch the application. Start typing to receive autocomplete suggestions.

Data
----

The project uses two primary datasets for Arabic and English:

-   **Arabic Data**:

    -   Cleaned and stored in `data/arabic_data_cleaned.txt`.

    -   Sourced from Kaggle: [Arabic Classification Dataset](https://www.kaggle.com/datasets/saurabhshahane/arabic-classification).

-   **English Data**:

    -   Sourced from: [English Corpora](https://www.english-corpora.org/).

NLP Models
----------

### N-Grams

Used for predicting the next word(s):

-   **Bigram**: For single-word inputs.

-   **Trigram**: For multiple-word inputs.

Both Arabic and English n-gram models are trained on their respective datasets.

### GPT 2 (Arabic)

We fine-tuned a pre-trained Arabic gpt 2 model from Hugging Face to generate context-aware suggestions:

🔗 [asafaya/bert-base-arabic on Hugging Face](https://huggingface.co/akhooli/gpt2-small-arabic-poetry)

GUI
---

Built using `CustomTkinter`, offering:

-   A text input field.

-   A dynamic suggestion box with word predictions.

-   Keyboard navigation (arrow keys + Enter).

-   Auto-detection of Arabic vs. English input.

Features
--------

-   Bilingual autocomplete (Arabic and English).

-   Combines n-grams and GPT-2 for prediction.

-   Clean and responsive GUI.

-   Easy navigation and word selection.

Requirements
------------

-   `customtkinter`

-   `tkinter`

-   `numpy`

-   `pandas`

-   `nltk`

-   `scikit-learn`

Presentation
------------

📊 View the detailed project presentation:\
[Canva Slide Deck](https://www.canva.com/design/DAGm6Q3ODIA/bszklmxk92H-Fcu-0VWkYQ/edit?utm_content=DAGm6Q3ODIA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)