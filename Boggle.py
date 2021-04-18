import random
'''
In order to watch how the code works behind the scenes, set debug to True
'''
debug = False

def load_words():

    '''
    Loads uppered words with length >= 3 from words_alpha.txt into a set and returns it.
    '''

    with open('english-words-master\english-words-master\words_alpha.txt') as word_file:
        valid_words = set()
        for word in word_file.read().split():
            if len(word) >= 3:
                valid_words.add(word.upper())

        # valid_words = set(word_file.read().split())

    if debug: print("Words loaded: {}".format('FATE' in valid_words))

    return valid_words

def randomize_board():

    '''
    Simulates rolling the standard "Boggle" dice into random slots on a grid and returns this as a 2D list for the game board.
    '''

    die = [
        ['R', 'I', 'F', 'O', 'B', 'X'],
        ['I', 'F', 'E', 'H', 'E', 'Y'],
        ['D', 'E', 'N', 'O', 'W', 'S'],
        ['U', 'T', 'O', 'K', 'N', 'D'],
        ['H', 'M', 'S', 'R', 'A', 'O'],
        ['L', 'U', 'P', 'E', 'T', 'S'],
        ['A', 'C', 'I', 'T', 'O', 'A'],
        ['Y', 'L', 'G', 'K', 'U', 'E'],
        ['Q', 'B', 'M', 'J', 'O', 'A'],
        ['E', 'H', 'I', 'S', 'P', 'N'],
        ['V', 'E', 'T', 'I', 'G', 'N'],
        ['B', 'A', 'L', 'I', 'Y', 'T'],
        ['E', 'Z', 'A', 'V', 'N', 'D'],
        ['R', 'A', 'L', 'E', 'S', 'C'],
        ['U', 'W', 'I', 'L', 'R', 'G'],
        ['P', 'A', 'C', 'E', 'M', 'D'],
    ]

    board = []

    die_indices = [i for i in range(16)]
    random.shuffle(die_indices)

    for index in die_indices:
        board.append(random.choice(die[index]))

    board = [board[0:4], board[4:8], board[8:12], board[12:]]

    if debug:
        print("Board Generated:")
        for row in board:
            print(row)

    return board

def search_word(word, board, words):

    '''
    Verifies if the word is in the set of real words and attainable through the game board.
    '''

    letters = board[0]+board[1]+board[2]+board[3]

    if len(word) < 3:
        if debug: print("{} is too short.".format(word))
        return False

    if word not in words:
        if debug: print("{} is not a word.".format(word))
        return False

    if word[0] not in letters:
        if debug: print("{}'s first letter {} is not on the board.".format(word, word[0]))
        return False

    stack = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == word[0]:
                stack.append((i,j,0,[(i,j)]))
    if debug: print("Initial stack: {}".format(stack))

    while stack:
        if debug: print("Current stack: {}".format(stack))
        current = stack.pop()
        i, j, k, visited = current[0], current[1], current[2], current[3]

        directions = [(0,-1), (-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1)]

        if k == len(word)-1:
            if debug: print("Found {} by {}".format(word, visited))
            return True

        for direction in directions:
            x, y = i+direction[0], j+direction[1]
            if 0 <= x < 4 and 0 <= y < 4:
                if board[x][y] == word[k+1] and (x,y) not in visited:
                    stack.append((x, y, k+1, visited+[(x, y)]))

    if debug: print("{} not on board".format(word))
    return False

def print_board(board):

    '''
    Prints game board.
    '''

    for row in board:
        print(row)

def end_game(entered_words):

    '''
    Shows results of game.
    '''

    entered_words.sort()
    entered_words.sort(key=len, reverse=True)
    points = 0
    for word in entered_words:
        points += 200 * 2 **(len(word)-3)
    print("-----")
    print("End game.")
    print("Total points: {}".format(points))
    print("Number of words: {}".format(len(entered_words)))
    print("-----")
    for word in entered_words:
        print("{}: {}".format(word, 200*2**(len(word)-3)))

def play_game(board, words):

    '''
    Runs "Boggle".
    '''

    entered_words = []

    print_board(board)

    current = input("Enter a word you see, otherwise 0 to exit: ")
    while current != '0':
        current = current.upper()
        if current in entered_words:
            print("{} Already Entered!".format(current))
        elif search_word(current, board, words) and current not in entered_words:
            print("{} Valid!".format(current))
            entered_words.append(current)
        else:
            print("{} Invalid!".format(current))
        print("-----")
        print_board(board)
        current = input("Enter a word you see, otherwise 0 to exit: ")

    end_game(entered_words)

if debug:
    seed = input("Enter random seed: ")
    random.seed(seed)

play_game(randomize_board(), load_words())
if debug: print("Seed used: {}".format(seed))
