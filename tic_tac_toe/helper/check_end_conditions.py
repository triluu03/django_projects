import numpy as np

def checkEndGame(details, row, col):
    """
    Check the ending condition of the game
    params:
        details: 2D array of the board
        row: row of the last move
        col: column of the last move
    return:
        True if the game is ended, False otherwise
    """
    # Check in the same row:
    if check_in_array(details[row, :], col):
        return True
    # Check in the same column:
    if check_in_array(details[:, col], row):
        return True
    # Check in the diagonal:
    if check_in_diagonal(details, row, col):
        return True
    return False

def check_in_array(array, index, n = 5):
    """
    Check if there are n same elements consecutively in an extracted array
    params:
        array: numpy array or list
        index: index of the considered start point
        n: number of same elements
    return:
        boolean value
    """
    num = 1
    for i in range(index+1, len(array)):
        if array[i] == array[i-1]:
            num += 1
            if num == n:
                return True
        else:
            break
    for i in range(index-1, -1, -1):
        if array[i] == array[i+1]:
            num += 1
            if num == n:
                return True
        else:
            break
    return False

def check_in_diagonal(matrix, row, col, n = 5):
    """
    Check if there are n same elements in a diagonal of a matrix
    params:
        matrix: 2D numpy array
        row: row of the start point to consider
        col: column of the start point to consider
        n: number of same elements
    return:
        boolean value
    """
    first_direction = 1
    for i in range(1, len(matrix)):
        if row + i < len(matrix) and col + i < len(matrix):
            if matrix[row+i, col+i] == matrix[row, col]:
                first_direction += 1
                if first_direction == n:
                    return True
            else:
                break
    for i in range(1, len(matrix)):
        if row - i > -1 and col-i > -1:
            if matrix[row-i, col-i] == matrix[row, col]:
                first_direction += 1
                if first_direction == n:
                    return True
            else:
                break

    second_direction = 1
    for i in range(1, len(matrix)):
        if row - i > -1 and col + i < len(matrix):
            if matrix[row-i, col+i] == matrix[row, col]:
                second_direction += 1
                if second_direction == n:
                    return True
            else:
                break
    for i in range(1, len(matrix)):
        if row + i < len(matrix) and col-i > -1:
            if matrix[row+i, col-i] == matrix[row, col]:
                second_direction += 1
                if second_direction == n:
                    return True
            else:
                break
    
    return False
    