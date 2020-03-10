from unittest import TestCase
from boggle import Boggle
import numpy as np


class TestBoggle(TestCase):

    def test_find_word_simple(self):
        size = 4
        b = Boggle(size)
        board = b.create_empty_board(size)
        for row in range(size):
            for col in range(size):
                board[row][col] = 'A'.encode()

        result = b.find_word('AAA')
        print("Result is: {}".format(result))

        result = b.find_word('XYZ')
        print("Result is: {}".format(result))

    def test_find_word_slightly_complex(self):
        size = 4
        b = Boggle(size)
        board = b.create_empty_board(size)
        for row in range(size):
            for col in range(size):
                board[row][col] = 'A'.encode()
        board[1][0] = 'B'.encode()
        board[1][1] = 'M'.encode()
        board[1][2] = 'C'.encode()
        board[1][3] = 'K'.encode()

        b.print_board()
        result = b.find_word('BMCK')
        print("Result is: {}".format(result))

        result = b.find_word('KCMB')
        print("Result is: {}".format(result))

        result = b.find_word('KBCM')
        print("Result is: {}".format(result))

    def test_find_word_complex(self):
        size = 6
        b = Boggle(size)
        board = b.create_empty_board(size)
        for row in range(size):
            for col in range(size):
                board[row][col] = 'X'.encode()
        board[0][0] = 'X'.encode()
        board[0][1] = 'B'.encode()
        board[0][2] = 'E'.encode()
        board[0][3] = 'D'.encode()

        board[1][0] = 'E'.encode()
        board[1][1] = 'O'.encode()
        board[1][2] = 'R'.encode()
        board[1][3] = 'C'.encode()

        board[2][0] = 'M'.encode()
        board[2][1] = 'W'.encode()
        board[2][2] = 'R'.encode()
        board[2][3] = 'E'.encode()

        board[3][0] = 'S'.encode()
        board[3][1] = 'C'.encode()
        board[3][2] = 'A'.encode()
        board[3][3] = 'Q'.encode()

        b.print_board()
        result = b.find_word('SCARECROW')
        print("Result is: {}".format(result))


def test_delete():
    """Testing out some things in numpy"""
    x = np.array([3, 54, 6, 7, 4, 23, 5, 6, 2, 1, 3])
    y = np.delete(x, np.where(x == 3))
    print("{} {}".format(x, y))
