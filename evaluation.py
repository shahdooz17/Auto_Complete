import nltk

def split_dataset(text, split_ratio=0.9):
    """
    Splits the text into training and testing tokens based on the ratio.
    Returns (train_text, test_tokens).
    """
    tokens = nltk.word_tokenize(text)
    split_index = int(len(tokens) * split_ratio)
    train_tokens = tokens[:split_index]
    test_tokens = tokens[split_index:]
    return ' '.join(train_tokens), test_tokens


def evaluate_trigram_model(model, test_tokens, k=3):
    """
    Evaluates a trigram model using precision@k and mean reciprocal rank (MRR).

    Parameters:
        model: An instance of AutoFilling (trigram model).
        test_tokens: List of tokens (ground-truth) to evaluate on.
        k: Top-k suggestions to consider.

    Returns:
        precision_at_k: Correct predictions / total predictions
        mrr: Mean Reciprocal Rank
    """
    correct = 0
    total = 0
    reciprocal_ranks = []

    for i in range(2, len(test_tokens) - 1):
        context = test_tokens[i-2] + " " + test_tokens[i-1]
        actual_next = test_tokens[i]
        predictions = model.suggest_next_trigrams(context)

        if actual_next in predictions[:k]:
            correct += 1
            rank = predictions.index(actual_next) + 1
            reciprocal_ranks.append(1.0 / rank)
        else:
            reciprocal_ranks.append(0)

        total += 1

    precision_at_k = correct / total if total > 0 else 0
    mrr = sum(reciprocal_ranks) / total if total > 0 else 0
    return precision_at_k, mrr
