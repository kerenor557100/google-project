from auto_complete_class import AutoCompleteData
from os import walk
from prefix_trie import Trie
import re
from string import ascii_lowercase
from typing import List
from words_details_class import WordDetails
"""
A dictionary that keeps the details we need for each word
"""
WORDS_DETAILS_DICT = {}
PREFIX_TREE = Trie()
SUFFIX_TREE = Trie()


def reverse(s):
    """
    :param s:The word obtained from the dictionary
    :return:Returns the word only in reverse
    """
    string = ""
    for i in s:
        string = i + string
    return string


def create_data_dictionary(files_list: List[str]) -> dict[str, List[WordDetails]]:
    """ Receive a list of files and return a dictionary.
    The dictionary's keys are all the words inside the files, and the value is a list that includes details about
    the word (an object named WordDetails that gives us information about the place that the word found).

    :param files_list: A list includes paths to files.
    :return: Dictionary with words as keys and List[WordDetails] as value.
    """
    words_dict = {}
    for file_path in files_list:
        try:
            with open(file_path, encoding='UTF8') as file:
                pos = 0
                for row_number, row in enumerate(file.readlines()):
                    words_list = [word.lower() for word in re.findall(r"[^\w']*([\w']+)[^\w']*", row)]
                    p2prev_word = None
                    for word_place, word in enumerate(words_list):
                        new_word = WordDetails(word, row_number, word_place, pos, file_path, row)
                        if word in words_dict.keys():
                            words_dict[word].append(new_word)
                        else:
                            words_dict[word] = [new_word, ]
                        if p2prev_word:
                            p2prev_word.set_next(new_word)
                        p2prev_word = new_word
                    pos = file.tell()
        except OSError as err:
            print(f"File: {file_path}, Error: {err}")
    return words_dict


def initialize_data(files_list: List[str]) -> dict[str, List[WordDetails]]:
    """
     Initialize data and return data structure.
    :param files_list: List of files' paths.
    :return: Dictionary as a data structure for all the files.
    """
    words = create_data_dictionary(files_list)
    keys = words.keys()
    PREFIX_TREE.form_trie(list(keys))
    revers_keys = [reverse(word) for word in list(keys)]
    SUFFIX_TREE.form_trie(revers_keys)
    return words


def make_list_of_files() -> List[str]:
    """
    The function passes the file we gave it
    :return:list of file paths
    """
    dir_path = r"..\archive"
    # dir_path = r"..\t"
    res = []
    for (dir_path, dir_names, files_names) in walk(dir_path):
        res.extend([dir_path + "\\" + file_name for file_name in files_names])
    return res


def check_user_words(words_list: List[str], score: int) -> List[AutoCompleteData]:
    """ Receive a list of words and check if there is a sentence inside the data structure that
     matches the received list. Return maximum five results.

    :param words_list:The list of words we are looking for in the data structure
    :param score:Determines the score of the received sentence
    :return:Returns a maximum of five results matching the received sentence
    """
    word_result = []
    all_exists_words = WORDS_DETAILS_DICT.get(words_list[0])
    if not all_exists_words:
        return []
    for obj in all_exists_words:
        if len(words_list) >= 2:
            current_word = obj.next
            for word in words_list[1:]:
                if not current_word or current_word.word != word:
                    break
                current_word = current_word.next
            else:
                word_result.append(AutoCompleteData(obj, words_list, score))
                if len(word_result) == 5:
                    break
        else:
            word_result.append(AutoCompleteData(obj, words_list, score))
        if len(word_result) == 5:
            break

    return word_result


def calculate_optional_results(substring: str, score: int) -> List[AutoCompleteData]:
    """Receives the user's string after corrections if necessary,
    and receives the score of this sentence and returns a list of all relevant sentences
    :param substring:user's string after corrections if necessary
    :param score:score of this sentence
    :return:list of all relevant sentences
    """
    words_list = [word.lower() for word in re.findall(r"[^\w']*([\w']+)[^\w']*", substring)]
    word_result = []
    word_result += check_user_words(words_list, score)
    # if len(word_result) < 5:
    #     first_word_op = [reverse(word) for word in SUFFIX_TREE.get_all_words_matching_prefix(reverse(words_list[0]))]
    #     last_word_op = PREFIX_TREE.get_all_words_matching_prefix(words_list[-1])
    #     if len(words_list) == 1:
    #         for word in first_word_op:
    #             word_result += check_user_words([word], score)
    #             if len(word_result) >= 5:
    #                 return word_result
    #         for word in last_word_op:
    #             word_result += check_user_words([word], score)
    #             if len(word_result) >= 5:
    #                 return word_result
    #     else:
    #         for start_word in first_word_op:
    #             for end_word in last_word_op:
    #                 word_result += check_user_words([start_word] + words_list[1:len(words_list) - 1] +
    #                                                 [end_word], score)
    #                 if len(word_result) >= 5:
    #                     return word_result

    return word_result


def get_best_k_completions(prefix: str) -> List[AutoCompleteData]:
    """ Receive the user's string and return the top 5 rows at the texts that could complete the sentence.
    The string could be with one mistake, and it should be a substring of a sentence.
    :param prefix: Part of a sentence that the user insert.
    :return: Best 5 results.
    """
    prefix_length = len(prefix)
    score = prefix_length * 2
    best_word_result = calculate_optional_results(prefix, score)

    if len(best_word_result) >= 5:
        return best_word_result[:5]
    # switch

    results_after_mistakes = []
    minus_score = 5
    for i in range(0, prefix_length)[::-1]:
        current_letter = prefix[i]
        if current_letter == ' ':
            continue
        for letter in ascii_lowercase:
            if letter == current_letter:
                continue
            if len(results_after_mistakes) >= 5:
                break
            current_string = (prefix[:i] if i != 0 else "") + letter + (prefix[i+1:] if i != prefix_length-1 else "")
            results_after_mistakes += calculate_optional_results(current_string, score - minus_score)
            minus_score = minus_score - 1 if minus_score != 1 else minus_score

    best_word_result = best_word_result + results_after_mistakes
    best_word_result.sort(reverse=True)
    results_after_mistakes = []
    # add
    minus_score = 10
    for i in range(1, prefix_length)[::-1]:
        for letter in ascii_lowercase:
            if len(results_after_mistakes) >= 5:
                break
            current_string = prefix[:i] + letter + prefix[i:]
            results_after_mistakes += calculate_optional_results(current_string, score - minus_score)
            minus_score = minus_score - 2 if minus_score != 2 else minus_score

    # sub
    minus_score = 10
    for i in range(prefix_length)[::-1]:
        if len(results_after_mistakes) >= 5:
            break
        current_string = (prefix[:i] if i != 0 else "") + (prefix[i + 1:] if i != prefix_length-1 else "")
        results_after_mistakes += calculate_optional_results(current_string, score - minus_score)
        minus_score = minus_score - 2 if minus_score != 2 else minus_score

    best_word_result = best_word_result + results_after_mistakes
    best_word_result.sort(reverse=True)

    return best_word_result[:5]


if __name__ == '__main__':
    WORDS_DETAILS_DICT = initialize_data(make_list_of_files())
    while True:
        prefix = input("Please enter a prefix: ")
        result = get_best_k_completions(prefix)
        for item in result:
            print(item)
