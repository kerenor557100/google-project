
from dataclasses import dataclass
import re
from typing import List
from words_details_class import WordDetails


@dataclass
class AutoCompleteData:
    """
    Save inside a data structure the details about each match.
    """

    def __init__(self, word_detail: WordDetails, substring_list: List[str], score: int):
        """
        that function does:
        Saving the information typed by the user, and giving a grade on the answers we gave him.

        :param word_detail: the detail about the words.
        :param substring_list:  a list of substrings.
        :param score: the score of the results that the user recieves.
        """

        self.completed_sentence = word_detail.full_row
        pattern = "("
        for index, word in enumerate(substring_list):
            pattern += r"[^\w']*" + word
        pattern += ")"
        match = re.search(pattern, self.completed_sentence.lower())
        if match:
            self.offset = self.completed_sentence.lower().index(match.group(1))
        self.source_text = word_detail.file_path
        self.score = score

    def __str__(self):
        """

        :param self: autoCompleteData
        :return: data about the sentence and the source.
        """
        return f"Sentence = {self.completed_sentence}\nOffset = {self.offset}\n " \
               f"Source = {self.source_text}\nScore = {self.score}\n\n"

    def __lt__(self, other: "AutoCompleteData") -> bool:
        """ To compare two objects by their score
        :param other: The second AutoCompleteData object
        :return: True if current score < other score.
        """
        return self.score < other.score
