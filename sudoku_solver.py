__author__ = 'purdyk'

import copy
import sys

if len(sys.argv) > 1:
    start = sys.argv[1]
else:
    start = "800003700040605000203790000630000050000000000090000071000067504000801090004500003"

history = []
guesses = 0


def construct_board():
    board = [[]] * 9
    for i in range(0, 9):
        board[i] = [[]] * 9
        for j in range(0, 9):
            item = int(start[9 * i + j])
            if item == 0:
                res = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            else:
                res = [item]

            board[i][j] = res

    return board


def remove_if_unique(available, options):
    if len(options) == 1:
        num = options[0]
        if num in available:
            available.remove(options[0])
        else:
            print "Found a duplicate"
            return None
    return available


def safe_remove(list, toremove):
    for each in toremove:
        if each in list:
            list.remove(each)


def available_row(board, rownum):
    available = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    unavailable_elsewhere = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    for i in range(0, 9):
        cell = board[rownum][i]
        available = remove_if_unique(available, cell)
        safe_remove(unavailable_elsewhere, cell)

        if not available:
            break

    if len(unavailable_elsewhere) == 1:
        return unavailable_elsewhere

    return available


def available_col(board, colnum):
    available = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    unavailable_elsewhere = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    for i in range(0, 9):
        cell = board[i][colnum]
        available = remove_if_unique(available, cell)
        safe_remove(unavailable_elsewhere, cell)

        if not available:
            break

    if len(unavailable_elsewhere) == 1:
        return unavailable_elsewhere

    return available


def available_square(board, rownum, colnum):
    available = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    unavailable_elsewhere = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    squarenum = 3 * (rownum / 3) + (colnum / 3)
    startrow = 3 * (squarenum / 3)
    startcol = 3 * (squarenum % 3)

    for i in range(0, 9):

        offrow = (i / 3)
        offcol = (i % 3)

        r = startrow + offrow
        c = startcol + offcol

        # print "Searching {}x{}".format(r, c)
        cell = board[r][c]
        available = remove_if_unique(available, cell)
        safe_remove(unavailable_elsewhere, cell)

        if not available:
            break

    if len(unavailable_elsewhere) == 1:
        return unavailable_elsewhere

    return available


def all_available(board, row, column):
    na = available_row(board, row)
    if not na:
        print "Nothing from AR"
        return None
    ar = set(na)

    na = available_col(board, column)
    if not na:
        print "Nothing from AC"
        return None
    ac = set(na)

    na = available_square(board, row, column)
    if not na:
        print "Nothing from AS"
        return None
    aq = set(na)

    arc = ar.intersection(ac)
    aa = arc.intersection(aq)

    return list(aa)


def reduce_board(board):
    changed = 0

    for row in range(0, 9):
        for col in range(0, 9):

            old = board[row][col]

            if len(old) > 1:
                new = all_available(board, row, col)

                if new is None:
                    # print "Nothing available items for cell"
                    return -1

                if len(new) == 0:
                    # print "Board is fucked"
                    return -1

                if len(old) != len(new):
                    board[row][col] = new
                    changed = 1

    return changed


def print_board(board):
    for row in range(0, 9):
        for col in range(0, 9):
            cell = board[row][col]
            if len(cell) == 1:
                print cell[0],
            else:
                print "?",
            print " ",
        print ""
        print ""


def unsolved_cells(board):
    unsolved = 0
    for row in range(0, 9):
        for col in range(0, 9):
            cell = board[row][col]
            if len(cell) != 1:
                unsolved += 1
    return unsolved


def choose_cell(board):
    best = 10
    bestrc = None

    for row in range(0, 9):
        for col in range(0, 9):
            cell = board[row][col]
            if 1 < len(cell) < best:
                best = len(cell)
                bestrc = (row, col)
                if best == 2:
                    return bestrc
    return bestrc


def iter_reduce(board):

    status2 = reduce_board(board)
    while status2 == 1:
        # print "Reducing..."
        status2 = reduce_board(board)

    return status2


def guess_board(board):
    # print "Guessing..."
    # guesses += 1

    rc = choose_cell(board)
    newb = board

    row, col = rc
    cell = newb[row][col]

    future = copy.deepcopy(newb)
    future[row][col] = cell[1:]
    history.append(future)

    newb[row][col] = cell[0:1]

    return newb


b = construct_board()

print "{} unsolved cells".format(unsolved_cells(b))
print_board(b)
status = iter_reduce(b)

while unsolved_cells(b) > 0:
    b = guess_board(b)
    guesses += 1

    status = iter_reduce(b)

    while status == -1:
        b = history.pop()
        guesses += 1
        status = iter_reduce(b)

print "Solved in {} guesses".format(guesses)

print_board(b)
