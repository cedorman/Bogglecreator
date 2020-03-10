#!/usr/bin/python3
import pprint
import copy
import random
import numpy as np

# special character that means that this space has not been used.  Encode it because
# numpy uses the byte literal rather than the unicode.
empty_letter = '0'.encode()

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Boggle:

    def __init__(self, size):
        self.size = size
        self.create_empty_board(self.size)
        self.current_words = []

    def create_empty_board(self, size):
        # In vanilla python:
        # board = [['0'] * size] * size
        self.size = size
        self.board = np.chararray((size, size))
        self.board[:] = empty_letter
        return self.board

    def print_board(self, board_to_print=None):
        for row in range(self.size):
            strarray = []
            for col in range(self.size):
                if board_to_print is None:
                    strarray.append(self.board[row][col].decode())
                else:
                    strarray.append(board_to_print[row][col].decode())
            output = ', '.join(strarray)
            print("\t{}".format(output))

    def find_empty_spot(self, aboard=None):
        """find a blank on the board"""
        vals = np.argwhere(self.board == empty_letter)
        if len(vals) > 0:
            np.random.shuffle(vals)
            return vals[0][0], vals[0][1]

        return -1, -1

    def shuffle_board(self, aboard):
        # Ravel returns a flattened _view_ of the 2d array, whereas flatten() produces a new flattened array
        b = aboard.ravel()
        np.random.shuffle(b)
        b = b.reshape(self.size, self.size)
        return b

    def fill_remaining_random(self):
        """If there are spaces with nothing in them, add random letters"""
        vals = np.argwhere(self.board == empty_letter)
        for val in vals:
            self.board[val[0]][val[1]] = ''.join(random.sample(letters, 1))

    def find_word(self, word, used_locations=[]):

        # print("In find_word. Looking for: {}.  Used: {}".format(word, used_locations))

        # If got to end of word, we are done
        if len(word) == 0:
            return True, used_locations

        first_letter = word[0].encode()

        if len(used_locations) == 0:
            for loc, x in np.ndenumerate(self.board):
                row = loc[0]
                col = loc[1]
                board_letter = self.board[row][col]
                if board_letter == first_letter:
                    possible_locations = [(row, col)]
                    return self.find_word(word[1:], possible_locations)
        else:
            indices = []
            last_row = used_locations[-1][0]
            last_col = used_locations[-1][1]
            indices.append((last_row - 1, last_col))
            indices.append((last_row + 1, last_col))
            indices.append((last_row, last_col - 1))
            indices.append((last_row, last_col + 1))

        for loc in indices:
            row = loc[0]
            col = loc[1]

            # remove those off board or already used
            if row < 0 or row >= self.size or col < 0 or col >= self.size:
                continue

            if loc in used_locations:
                continue

            if self.board[row][col] == first_letter:
                possible_locations = copy.deepcopy(used_locations)
                possible_locations.append((row, col))
                return self.find_word(word[1:], possible_locations)

        return False

    def add_word_sequentially(self, word, working_board, used_locations=[]):
        if len(word) == 0:
            return True, working_board

        first_letter = word[0].encode()

        current_working_board = copy.deepcopy(working_board)

        # print("in add_word_seq {}".format(word))
        # self.print_board(current_working_board)

        if len(used_locations) == 0:
            row, col = self.find_empty_spot(current_working_board)
            current_working_board[row][col] = first_letter
            possible_locations = [(row, col)]
            return self.add_word_sequentially(word[1:], current_working_board, possible_locations)

        # Places we can put the next letter
        indices = []
        last_row = used_locations[-1][0]
        last_col = used_locations[-1][1]
        indices.append((last_row - 1, last_col))
        indices.append((last_row + 1, last_col))
        indices.append((last_row, last_col - 1))
        indices.append((last_row, last_col + 1))
        random.shuffle(indices)

        for loc in indices:
            row = loc[0]
            col = loc[1]

            # remove those off board or already used
            if row < 0 or row >= self.size or col < 0 or col >= self.size:
                continue

            # if loc in used_locations or not current_working_board[row][col] == empty_letter:
            if not current_working_board[row][col] == empty_letter:
                continue

            possible_locations = copy.deepcopy(used_locations)
            possible_locations.append((row, col))
            current_working_board[row][col] = first_letter
            result, deep_working_board = self.add_word_sequentially(word[1:], current_working_board,
                                                                    possible_locations)
            if result:
                return True, deep_working_board

        return False, None

    def add_word(self, word):
        """Given a new word, try to add it to the existing board"""

        # Make sure that all the letters are on the board
        e = (self.board.flatten())
        existing_letters = np.delete(e, np.where(e == empty_letter))
        room = np.size(self.board) - len(existing_letters)

        # If there is room, then add it
        if room >= len(word):
            result, new_board = self.add_word_sequentially(word, self.board)
            if result:
                print("Added {} to board".format(word))
                self.board = new_board
                return True
            else:
                print("Unable to add word to board")
                return False

        print("Not enough room to add word")
        return False

    def add_words(self, words):
        """Try to add the words, keeping track of the most that can be added"""
        best = 0
        for trial in range(100):
            self.create_empty_board(self.size)
            added = 0
            for word in words:
                result = self.add_word(word)
                if result:
                    added += 1

            # If successful, return with board
            if added == len(words):
                print("Required {} attempts".format(str(trial + 1)))
                self.fill_remaining_random()
                self.print_board()
                return

            if added > best:
                best_board = copy.deepcopy(self.board)
                best = added

        # Unsuccessful, print best one
        print("Unable to add all the words.  got {}".format(best))
        self.board = best_board
        self.fill_remaining_random()
        self.print_board()


def main():
    boggle = Boggle(8)
    words = ["SPRING", "COPY", "WATCH", "DOG", "AIRPLANE"]
    boggle.add_words(words)


if __name__ == "__main__":
    # test_delete()
    np.random.seed(13)
    random.seed(1324)
    main()
