#!/usr/bin/python3
import pprint
import copy
import numpy as np

# special character that means that this space has not been used.  Encode it because
# numpy uses the byte literal rather than the unicode.
empty_letter = '0'.encode()


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

    def print_board(self):
        pp = pprint.PrettyPrinter(indent=4, depth=2)
        pp.pprint(self.board)

    def find_empty_spot(self):
        """find a blank on the board"""
        for row in range(self.size):
            for col in range(self.size):
                if self.board(row, col) == empty_letter:
                    return row, col

    def shuffle(self, aboard):
        # Ravel returns a flattened _view_ of the 2d array, whereas flatten() produces a new flattened array
        b = aboard.ravel()
        np.random.shuffle(b)
        b = b.reshape(self.size, self.size)
        return b

    def find_word(self, word, used_locations=[]):

        print("In find_word. Looking for: {}.  Used: {}".format(word, used_locations))

        # If got to end of word, we are done
        if len(word) == 0:
            return True

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

    def rearrange_and_find(self, word):
        self.board = self.shuffle(self.board)
        self.print_board()
        return self.find_word(word)

    def add_word(self, word):
        """Given a new word, try to add it to the existing board"""

        # Make sure that all the letters are on the board
        e = (self.board.flatten())
        existing_letters = np.delete(e, np.where(e == empty_letter))
        room = np.size(self.board) - len(existing_letters)

        # If there is room, then just add it
        if room >= len(word):
            for letter in word.split():
                row, col = self.find_empty_spot()
                self.board[row][col] = letter.encode()

            found = False
            while not found:
                found = self.rearrange_and_find(word)

        print("amount room {}".format(room))
        return


def test_delete():
    x = np.array([3, 54, 6, 7, 4, 23, 5, 6, 2, 1, 3])
    y = np.delete(x, np.where(x == 3))
    print("{} {}".format(x, y))


def main():
    boggle = Boggle()

    # Add words one at a time
    words = ["spring", "summer"]
    for word in words:
        boggle.add_word(word)

    boggle.print_board()


if __name__ == "__main__":
    # test_delete()
    main()
