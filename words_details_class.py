class WordDetails:
    """A WordDetails class, holds details about a word.

    :ivar word: The word.
    :ivar row_num: The number of row that the word appeared.
    :ivar word_place: What is the number of the current word in the sentence.
    :ivar start_row_position: The Place of the cursor at the beginning of the current line in the file.
    :ivar file_path: The path to the file where the current word has been found.
    """
    def __init__(self, word: str, row_num: int, word_place: int, start_row_position: int,
                 file_path: str, full_row: str):
        self.word = word
        self.row_num = row_num
        self.word_place = word_place
        self.start_row_position = start_row_position
        self.file_path = file_path
        self.next = None
        self.full_row = full_row

    """
    A function that returns a pointer to the next element in the sentence
    """
    def set_next(self, next_word: "WordDetails"):
        self.next = next_word

    @property
    def word(self):
        return self.__word

    @word.setter
    def word(self, new_word: str):
        self.__word = new_word

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path: str):
        self.__file_path = file_path

    @property
    def start_row_position(self):
        return self.__start_row_position

    @start_row_position.setter
    def start_row_position(self, start_row_position: int):
        self.__start_row_position = start_row_position

    @property
    def full_row(self):
        return self.__full_row

    @full_row.setter
    def full_row(self, full_row: int):
        self.__full_row = full_row
