NOT_SQUARE = 'Matrix must be square'
ZERO_DETERMINANT = 'Determinant can\'t be 0'
NO_DIAGONAL_DOMINANCE = 'WAR: The matrix was not reduced to diagonal dominance'

RESULT = 'Result'
EPOCHS = 'Epochs'
ERROR = 'Error'
B_MAE = 'MAE with vector b (residual criterion)'

GREETING = '''Hello, you have launched a solver for a system of
linear algebraic equations using the method of simple iterations
Select an action:'''
MATRIX_COND_OPTION = 'Find out the conditions for the matrix'
ENTER_MATRIX_OPTION = 'Enter the matrix'
ABOUT_ME_OPTION = 'About the author'

EXIT = 'exit'

ENTER_RULE_OPTION = 'Input rules'

ENTER_RULE = '''These rules apply to input from the keyboard and from a file.
First, enter epsilon in the first line. On the next one, enter the number of columns (rows).
And from the next line, enter the matrix of coefficients separated by spaces, with breaks between lines. There should be an empty line at the end of the file'''

MATRIX_COND = '''You must enter a square matrix consisting of floating point numbers.
Enter numbers separated by spaces. When entering through a file, there must be an empty line at the end.
The matrix must be square, with a non-zero determinant and reducible to diagonal dominance'''

ENTER_MATRIX_TYPE_MSG = 'Select input type'
FILE_MATRIX = 'file'
CONSOLE_MATRIX = 'console'
RANDOM_MATRIX = 'random'

ABOUT_ME = 'The program was made by Artyom Zaytsev, a 2nd year ITMO student majoring in system and application software engineering.'

WRONG_ACTION = 'Enter the numbers corresponding to the selected action'
BACK_RESPOND_MSG = 'Back'

ENTER_FILE_NAME = 'Enter full file name: '
INVALID_PATH = 'Invalid path'
INVALID_FILE = 'Can\'t read matrix from the file'

DIM_MAX = 100

MATRIX_DIM = f'Enter the height (width) of the matrix. Max is {DIM_MAX}: '
ENTER_EPSILON = 'Enter the epsilon: '

DIM_INPUT_ERROR = 'Please, input digit x. 1 <= x <= ' + str(DIM_MAX)

PARSE_ERROR = 'Can\'t parse your string. Please check it and try again.'


def get_solae_error(n: int):
    return f'For a given matrix, this method does not converge (over {n} steps the error coefficient did not decrease)'


ZERO_DIAGONAL = 'There is a zero on main diagonal'

YOU_ENTERED = 'You entered:'
