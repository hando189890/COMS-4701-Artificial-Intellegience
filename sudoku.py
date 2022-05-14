#!/usr/bin/env python
#coding:utf-8

#Homework Assginment 3
#Dongbing Han/dh3071
#2021.11.2

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import time
from statistics import mean, stdev


ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def changeMatrix(board):
    matrix = []
    for row in ROW:
        new = []
        for col in COL:
            tempindex = row + col
            temp = board[tempindex]
            new.append(temp)
        matrix.append(new)
    return matrix

def findEmpties(matrix):
    empties = set()
    for row in range(9):
        for col in range(9):
            if matrix[row][col] == 0:
                empties.add((row, col))
    return empties

def isValid(matrix, row, col, num):
    for j in range(9):
        if (matrix[row][j] == num):
            return False
    for i in range(9):
        if (matrix[i][col] == num):
            return False

    temprow = row - row % 3
    tempcol = col - col % 3

    for m in range(temprow, temprow + 3):
        for n in range(tempcol, tempcol + 3):
            if (matrix[m][n] == num):
                return False

    return True

def convertBack(matrix):
    tempboard = {ROW[r] + COL[c]: matrix[r][c]
             for r in range(9) for c in range(9)}

    return tempboard


def findDomain(matrix, row, col):
    """get domain for a specific position"""
    domain = []
    for value in range(1, 10):
        if isValid(matrix, row, col, value):
           domain.append(value)
    return domain


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    matrix = changeMatrix(board)
    btHelper(matrix)
    tempboard = convertBack(matrix)
    return tempboard


def btHelper(matrix):
    empties = findEmpties(matrix)
    if len(empties) == 0:
        return matrix

    currow = 0
    curcol = 0
    domainlength = 10
    for empty in empties:
        minrow, mincol = empty
        curdomain = findDomain(matrix, minrow, mincol)
        if len(curdomain) < domainlength:
            currow = minrow
            curcol = mincol
            domainlength = len(curdomain)

    row = currow
    col = curcol


    for num in range(1, 10):
        if not isValid(matrix, row, col, num):
            continue
        if isValid(matrix, row, col, num):
           matrix[row][col] = num
        if btHelper(matrix):
            return matrix
        matrix[row][col] = 0
    return None


if __name__ == '__main__':
    # if len(sys.argv) > 1:

    #     # Running sudoku solver with one board $python3 sudoku.py <input_string>.
    #     print(sys.argv[1])
    #     # Parse boards to dict representation, scanning board L to R, Up to Down
    #     board = {ROW[r] + COL[c]: int(sys.argv[1][9 * r + c])
    #              for r in range(9) for c in range(9)}

    #     # start = time.time()
    #     solved_board = backtracking(board)
    #     # end = time.time()
    #     # rm = end - start
    #     # Write board to file
    #     out_filename = 'output.txt'
    #     outfile = open(out_filename, "w")
    #     outfile.write(board_to_string(solved_board))
    #     outfile.write('\n')

    #     # print('board run time %.3f second(s)' % rm)


    # else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        # timeList = []
        # total = 0
        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):
            start = time.time()
            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = {ROW[r] + COL[c]: int(line[9 * r + c])
                     for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            print_board(board)

            # Solve with backtracking
            solved_board = backtracking(board)

            # Print solved board. TODO: Comment this out when timing runs.
            print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')
            # end = time.time()
            # rm = end - start
            # print('board run time %.3f second(s)' % rm)
            # print("\n")
            # timeList.append(rm)
            # total = total + rm

        # maxT = max(timeList)
        # minT = min(timeList)
        # meanT = mean(timeList)
        # stdevT = stdev(timeList)
        # print('max %.3f second(s)' % maxT)
        # print('min %.3f second(s)' % minT)
        # print('mean %.3f second(s)' % meanT)
        # print('stdev %.3f second(s)' % stdevT)
        # print('total %.3f second(s)' % total)

        print("Finishing all boards in file.")