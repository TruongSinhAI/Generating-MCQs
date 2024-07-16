from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import requests
import re
import random

from nltk.wsd import lesk
# from pywsd.similarity import max_similarity
# from pywsd.lesk import adapted_lesk
# from nltk.corpus import wordnet as wn


class GenMCQ:
    def __init__(self):
        self.text = ""
        self.sentences = self.tokenize_sentences()

    def setText(self, text):
        self.text = text
        self.sentences = self.tokenize_sentences()
    def get_freq(self, number):
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(self.text.lower())
        filtered_words = [word for word in word_tokens if word.isalnum() and word not in stop_words]
        word_freq = {word: filtered_words.count(word) for word in filtered_words}
        sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [x[0] for x in sorted_word_freq][:number]

    def tokenize_sentences(self):
        sentences = sent_tokenize(self.text)
        sentences = [sentence.strip() for sentence in sentences if len(sentence) > 0]
        return sentences

    def get_sentences_for_keyword(self, keywords):
        keyword_sentences = {}
        for keyword in keywords:
            keyword_sentences[keyword] = [sentence for sentence in self.sentences if keyword in sentence.lower()]
            keyword_sentences[keyword] = sorted(keyword_sentences[keyword], key=len, reverse=True)
        return keyword_sentences

    @staticmethod
    def get_distractors_wordnet(syn, word):
        distractors = []
        word = word.lower()
        if len(word.split()) > 1:
            word = word.replace(" ", "_")
        hypernyms = syn.hypernyms()
        if len(hypernyms) == 0:
            return distractors
        for item in hypernyms[0].hyponyms():
            name = item.lemmas()[0].name()
            if name == word:
                continue
            name = name.replace("_", " ").capitalize()
            if name not in distractors:
                distractors.append(name)
        return distractors

    @staticmethod
    def get_wordsense(sentence, word):
        word = word.lower()
        if len(word.split()) > 1:
            word = word.replace(" ", "_")
        return lesk(sentence, word, 'n')

    @staticmethod
    def get_distractors_conceptnet(word):
        word = word.lower().replace(" ", "_")
        distractor_list = []
        url = f"http://api.conceptnet.io/query?node=/c/en/{word}&rel=/r/PartOf&limit=5"
        obj = requests.get(url).json()
        for edge in obj['edges']:
            link = edge['end']['term']
            url2 = f"http://api.conceptnet.io/query?node={link}&rel=/r/PartOf&limit=10"
            obj2 = requests.get(url2).json()
            for edge in obj2['edges']:
                word2 = edge['start']['label']
                if word2 not in distractor_list and word not in word2.lower():
                    distractor_list.append(word2)
        return distractor_list

    def generate_mcqs(self, num_keywords=10):
        keywords = self.get_freq(num_keywords)
        keyword_sentence_mapping = self.get_sentences_for_keyword(keywords)
        key_distractor_list = {}
        # print(self.text)
        # print(keyword_sentence_mapping)
        for keyword in keyword_sentence_mapping:
            wordsense = self.get_wordsense(keyword_sentence_mapping[keyword][0], keyword)
            if wordsense:
                distractors = self.get_distractors_wordnet(wordsense, keyword)
                if len(distractors) == 0:
                    distractors = self.get_distractors_conceptnet(keyword)
                if distractors:
                    key_distractor_list[keyword] = distractors
            else:
                distractors = self.get_distractors_conceptnet(keyword)
                if distractors:
                    key_distractor_list[keyword] = distractors
        return key_distractor_list, keyword_sentence_mapping

    def display_mcqs(self, key_distractor_list, keyword_sentence_mapping):
        questionList = []
        index = 1
        for keyword, distractors in key_distractor_list.items():
            sentence = keyword_sentence_mapping[keyword][0]
            pattern = re.compile(keyword, re.IGNORECASE)
            output = pattern.sub(" _______ ", sentence)
            # print(f"{index}) {output}")
            choices = [keyword.capitalize()] + distractors
            top4choices = choices[:4]
            random.shuffle(top4choices)
            optionchoices = ['a', 'b', 'c', 'd']
            questionList.append(
                {
                    "questionTitle": output,
                    "questionImage": "",
                    "questionScore": 10,
                    "questionAnswer": []
                }
            )
            for idx, choice in enumerate(top4choices):
                questionList[-1].get("questionAnswer").append(
                    {
                        "title": choice,
                        "status": keyword.capitalize() == choice.capitalize()
                    }
                )
                # print(f"\t{optionchoices[idx]}) {choice}")
            # print(f"Answer: {keyword}\n")
            # print("More options:", choices[4:20], "\n\n")
            index += 1
        return questionList

# if __name__ == '__main__':
#     full_text = """
#     The Egyptians also developed a paperlike material called papyrus from a reed of the same name. If Egypt suffered hard times for a long period, the people blamed the pharaoh for angering the gods. The Nile provided so well for Egyptians that sometimes they had surpluses, or more goods than they needed. It combined the red Crown of Lower Egypt with the white Crown of Upper Egypt. As in many ancient societies, much of the knowledge of Egypt came about as priests studied the world to find ways to please the gods. Egyptians believed that if the pharaoh and his subjects honored the gods, their lives would be happy. Egyptians believed that if a tomb was robbed, the person buried there could not have a happy afterlife. The Nile River fed Egyptian civilization for hundreds of years. During the New Kingdom, pharaohs began building more secret tombs in an area called the Valley of the Kings. Nubia was the Egyptian name for the area of the upper Nile that had the richest gold mines in Africa. About 5,000 years ago, they noticed that a star now called Sirius appeared shortly before the Nile began to flood. Because the pharaoh was thought to be a god, government and religion were not separate in ancient Egypt. The Longest River the Nile is 4,160 miles long—the world’s longest river. The parts of Egypt not near the Nile were a desert.
#     """
#
#     mcq_generator = GenMCQ(full_text)
#     key_distractor_list, keyword_sentence_mapping = mcq_generator.generate_mcqs()
#     print(mcq_generator.display_mcqs(key_distractor_list, keyword_sentence_mapping))
