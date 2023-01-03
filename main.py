from collections import defaultdict
import json
HOR_LEN  = 38
VERT_LEN = 39

SOLUTIONS_TO_SHOW = 5
GAME_COLUMNS = 10

LETTER_POINTS = {
    'Α':  1, 'Β':  8, 'Γ':  4, 'Δ':  4, 'Ε':  1, 'Ζ': 10,
    'Η':  1, 'Θ': 10, 'Ι':  1, 'Κ':  2, 'Λ':  3, 'Μ':  3,
    'Ν':  1, 'Ξ': 10, 'Ο':  1, 'Π':  2, 'Ρ':  2, 'Σ':  1,
    'Τ':  1, 'Υ':  2, 'Φ':  8, 'Χ':  8, 'Ψ':  8, 'Ω':  3
}
LETTER_POINTS = defaultdict(int, **LETTER_POINTS)

MULTIPLIERS = (0, 1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

def expected_word_points(word):
    return sum(map(LETTER_POINTS.__getitem__, word)) * MULTIPLIERS[len(word)]


class TrieNode:
    nodes = 0

    def __init__(self, parent, word=None):
        self.terminal_word = word
        self.terminal_points = 0
        self.parent = parent
        self.edges = {}
        TrieNode.nodes += 1


    def set_terminal(self, word):
        self.terminal_word = word
        self.terminal_points = expected_word_points(word)


    def get_child(self, edge):
        if edge not in self.edges:
            self.edges[edge] = TrieNode(self)

        return self.edges[edge]


    def push_word(self, word, word_index=0):
        if word_index == len(word):
            return

        next_char = word[word_index]
        next_node = self.get_child(next_char)

        if word_index == len(word)-1:
            next_node.set_terminal(word)
            return

        next_node.push_word(word, word_index+1)


    def search_word(self, word, word_index=0):
        if word_index == len(word):
            if self.terminal_word == word:
                return (self.terminal_word, self.terminal_points)
            else:
                return None

        next_char = word[word_index]
        if not next_char in self.edges:
            return None

        return self.get_child(next_char).search_word(word, word_index+1)


root = TrieNode(None)
with open("wordlist.txt", 'r') as f:
    for line in f:
        root.push_word(line.strip())

print(TrieNode.nodes)
# print(root.search_word("ΦΤΗΝΟΣ"))

# parse json game state
with open("sample_game_state.json", 'r') as f:
    game_state = json.load(f)


board = [[] for _ in range(GAME_COLUMNS)]
for letter in game_state["game_board"]:
    board[letter["x"]].append(letter)

for column in board:
    column.sort(key=lambda letter: letter["y"])


def print_game_board(board):
    for row in range(GAME_COLUMNS, 0, -1):
        for column in range(GAME_COLUMNS):
            if len(board[column]) >= row:
                letter = board[column][-row]["letter"]
            else:
                letter = ' '

            print(letter, ' ', end='')
        print()


def search_words(board, unique_only=True):
    moves = []
    current_state = [0 for _ in range(GAME_COLUMNS)]
    solutions = []
    current_word = []

    word_iterator = root
    points = 0
    bonus_multiplier = 0
    def board_dfs():
        nonlocal word_iterator, points, bonus_multiplier
        for column, depth in enumerate(current_state):
            next_letter = board[column][depth]["letter"]
            if next_letter not in word_iterator.edges:
                continue

            letter_points = LETTER_POINTS[next_letter]
            extra_multiplier = 0
            bonus = board[column][depth]["bonus"]
            if bonus.endswith("Γ"):
                letter_points *= int(bonus[0])
            elif bonus.endswith("Λ"):
                extra_multiplier = int(bonus[0])

            moves.append(column)
            current_word.append(next_letter)
            current_state[column] += 1
            points += letter_points
            bonus_multiplier += extra_multiplier

            word_iterator = word_iterator.get_child(next_letter)

            # TODO: calculate points while searching
            if word_iterator.terminal_word is not None:
                word_points = points * (1+bonus_multiplier) * MULTIPLIERS[len(word_iterator.terminal_word)]
                solutions.append((word_iterator.terminal_word,
                                 word_points,
                                 moves.copy()))

            board_dfs()

            moves.pop()
            current_word.pop()
            current_state[column] -= 1
            word_iterator = word_iterator.parent
            points -= letter_points
            bonus_multiplier -= extra_multiplier


    # call dfs
    board_dfs()

    solutions.sort(key=lambda s: s[1], reverse=True)

    if unique_only:
        unique_words = set()
        clean_solutions = []
        for solution in solutions:
            if solution[0] not in unique_words:
                clean_solutions.append(solution)
                unique_words.add(solution[0])

        solutions = clean_solutions

    return solutions


print_game_board(board)
solutions = search_words(board)

print(f"Found {len(solutions)} possible words")
print("Best solutions:")

for solution in solutions[:min(SOLUTIONS_TO_SHOW, len(solutions))]:
    print("{:15s} {:3d} points {}".format(solution[0],
                                          solution[1],
                                          '->'.join(map(str, solution[2])
                                          )))

