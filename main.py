import pygame
import sys

# Ініціалізація гри
pygame.init()
size = width, height = 300, 300
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic Tac Toe")

# Ініціалізація поля гри
def create_board():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    return board

# Відмалювання поля гри на екрані
def draw_board(board):
    for row in range(3):
        for col in range(3):
            pygame.draw.rect(screen, (255, 255, 255), (col * 100, row * 100, 100, 100), 2)
            if board[row][col] == 'X':
                pygame.draw.line(screen, (255, 0, 0), (col * 100 + 10, row * 100 + 10), (col * 100 + 90, row * 100 + 90), 2)
                pygame.draw.line(screen, (255, 0, 0), (col * 100 + 90, row * 100 + 10), (col * 100 + 10, row * 100 + 90), 2)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, (0, 0, 255), (col * 100 + 50, row * 100 + 50), 40, 2)

# Перевірка переможця
def check_winner(board):
    lines = [
        [[0, 0], [0, 1], [0, 2]],
        [[1, 0], [1, 1], [1, 2]],
        [[2, 0], [2, 1], [2, 2]],
        [[0, 0], [1, 0], [2, 0]],
        [[0, 1], [1, 1], [2, 1]],
        [[0, 2], [1, 2], [2, 2]],
        [[0, 0], [1, 1], [2, 2]],
        [[0, 2], [1, 1], [2, 0]]
    ]

    for line in lines:
        symbols = [board[row][col] for row, col in line]
        if symbols.count('X') == 3:
            return 'X'
        elif symbols.count('O') == 3:
            return 'O'

    if all(board[row][col] != ' ' for row in range(3) for col in range(3)):
        return 'tie'

    return None

# Клас вузла дерева прийняття рішень
class Node:
    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.children = []
        self.score = None

    def add_child(self, node):
        self.children.append(node)

# Побудова дерева прийняття рішень
def build_decision_tree(board, player):
    root = Node(board, player)

    # Рекурсивна побудова дерева
    def build_tree(node):
        # Отримання всіх можливих ходів
        possible_moves = get_possible_moves(node.board)

        # Для кожного можливого ходу
        for move in possible_moves:
            # Створення нового вузла з оновленою дошкою
            new_board = update_board(node.board, move, node.player)
            new_player = get_next_player(node.player)
            child = Node(new_board, new_player)
            node.add_child(child)

            # Рекурсивний виклик для дочірнього вузла
            build_tree(child)

    build_tree(root)
    return root

# Обхід дерева прийняття рішень для пошуку найкращого ходу
def find_best_move_with_decision_tree(board, player):
    root = build_decision_tree(board, player)

    # Рекурсивний обхід дерева
    def traverse(node):
        if not node.children:
            # Досягнуто листка - обчислення оцінки
            node.score = evaluate_board(node.board, player)
        else:
            # Рекурсивний виклик для дочірніх вузлів
            for child in node.children:
                traverse(child)

            if node.player == player:
                # Вибір максимальної оцінки для гравця
                node.score = max(child.score for child in node.children)
            else:
                # Вибір мінімальної оцінки для супротивника
                node.score = min(child.score for child in node.children)

    traverse(root)

    # Вибір найкращого ходу
    best_score = float('-inf')
    best_move = None
    for child in root.children:
        if child.score > best_score:
            best_score = child.score
            best_move = get_move_from_boards(board, child.board)

    return best_move

# Оцінка стану дошки
def evaluate_board(board, player):
    winner = check_winner(board)
    if winner == player:
        return 1
    elif winner == get_next_player(player):
        return -1
    else:
        return 0

# Отримання можливих ходів
def get_possible_moves(board):
    moves = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                moves.append((row, col))
    return moves

# Оновлення дошки після ходу
def update_board(board, move, player):
    row, col = move
    new_board = [row[:] for row in board]
    new_board[row][col] = player
    return new_board

# Отримання наступного гравця
def get_next_player(player):
    return 'O' if player == 'X' else 'X'

# Отримання ходу з дошки
def get_move_from_boards(board1, board2):
    for row in range(3):
        for col in range(3):
            if board1[row][col] != board2[row][col]:
                return row, col

# Основний цикл гри
def main():
    board = create_board()
    current_player = 'X'

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and current_player == 'X':
                pos = pygame.mouse.get_pos()
                col = pos[0] // 100
                row = pos[1] // 100
                if board[row][col] == ' ':
                    board[row][col] = current_player
                    current_player = get_next_player(current_player)

        draw_board(board)
        pygame.display.flip()

        winner = check_winner(board)
        if winner is not None:
            print("Winner:", winner)
            break

        if current_player == 'O':
            move = find_best_move_with_decision_tree(board, current_player)
            if move is not None:
                row, col = move
                board[row][col] = current_player
                current_player = get_next_player(current_player)

# Запуск гри
if __name__ == '__main__':
    main()
