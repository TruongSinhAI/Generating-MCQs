import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter

class Summarize:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def preprocess_text(self, text):
        doc = self.nlp(text.lower())
        tokens = [token.text for token in doc if token.text not in STOP_WORDS and token.text not in punctuation]
        return tokens

    def calculate_sentence_scores(self, text):
        doc = self.nlp(text)
        word_frequencies = Counter(self.preprocess_text(text))
        max_frequency = max(word_frequencies.values()) if word_frequencies else 1

        for word in word_frequencies:
            word_frequencies[word] = word_frequencies[word] / max_frequency

        sentence_scores = {}
        for sent in doc.sents:
            score = 0
            for word in sent:
                if word.text.lower() in word_frequencies:
                    score += word_frequencies[word.text.lower()]
            sentence_scores[sent] = score

        return sentence_scores

    def summarize_text(self, text, num_sentences=3):
        sentence_scores = self.calculate_sentence_scores(text)
        if not sentence_scores:
            return ""

        summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
        summary = ' '.join([sent.text for sent in summarized_sentences])
        return summary