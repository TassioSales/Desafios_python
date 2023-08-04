import pygame
import chess
import random

# Inicializa o Pygame
pygame.init()

# Define as dimensões da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Cria a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define o título da janela
pygame.display.set_caption("Jogo de Xadrez")

# Define o tamanho do tabuleiro
board_size = 8

# Define o tamanho de cada célula do tabuleiro
cell_size = SCREEN_WIDTH // board_size

# Define as cores das células do tabuleiro
LIGHT_COLOR = (232, 235, 239)
DARK_COLOR = (125, 135, 150)

# Carrega as imagens das peças
PIECES = {
    'r': pygame.image.load("imagens_xadrez/wrook.png"),
    'n': pygame.image.load("imagens_xadrez/wknight.png"),
    'b': pygame.image.load("imagens_xadrez/wbishop.png"),
    'q': pygame.image.load("imagens_xadrez/wqueen.png"),
    'k': pygame.image.load("imagens_xadrez/wking.png"),
    'p': pygame.image.load("imagens_xadrez/wpawn.png"),
    'R': pygame.image.load("imagens_xadrez/brook.png"),
    'N': pygame.image.load("imagens_xadrez/bknight.png"),
    'B': pygame.image.load("imagens_xadrez/bbishop.png"),
    'Q': pygame.image.load("imagens_xadrez/bqueen.png"),
    'K': pygame.image.load("imagens_xadrez/bking.png"),
    'P': pygame.image.load("imagens_xadrez/bpawn.png")
}

# Cria um tabuleiro de xadrez
board = chess.Board()
move_history = []


# Função para obter a posição da célula clicada
def get_clicked_square(pos):
    col = pos[0] // cell_size
    row = board_size - (pos[1] // cell_size) - 1
    return chess.square(col, row)


# Função para desenhar o tabuleiro
def draw_board():
    for row in range(board_size):
        for col in range(board_size):
            x = col * cell_size
            y = row * cell_size
            color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))


# Função para desenhar as peças no tabuleiro
def draw_pieces():
    for row in range(board_size):
        for col in range(board_size):
            x = col * cell_size
            y = row * cell_size
            piece = board.piece_at(chess.square(col, board_size - row - 1))
            if piece:
                image = PIECES[piece.symbol()]
                screen.blit(image, (x, y))


# Função para desenhar movimentos válidos
def draw_valid_moves(valid_moves):
    for move in valid_moves:
        pygame.draw.circle(screen, (0, 255, 0),
                           (move % 8 * cell_size + cell_size // 2, (7 - move // 8) * cell_size + cell_size // 2),
                           cell_size // 4)


# Função para verificar se o jogo terminou (xeque-mate, empate)
def is_game_over():
    return board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material()


# Função para verificar se a posição está em xeque
def is_check():
    return board.is_check()


# Função para escolher o melhor movimento usando o algoritmo Minimax com poda alfa-beta
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)

    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


# Função de avaliação simples para a posição do tabuleiro
def evaluate_board(board):
    evaluation = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue
        value = piece_value(piece)
        if piece.color == chess.WHITE:
            evaluation += value
        else:
            evaluation -= value
    return evaluation


# Função para obter o valor da peça
def piece_value(piece):
    if piece.piece_type == chess.PAWN:
        return 1
    elif piece.piece_type == chess.KNIGHT:
        return 3
    elif piece.piece_type == chess.BISHOP:
        return 3
    elif piece.piece_type == chess.ROOK:
        return 5
    elif piece.piece_type == chess.QUEEN:
        return 9
    elif piece.piece_type == chess.KING:
        return 0


# Função para escolher o melhor movimento para a IA
def get_best_move(board):
    legal_moves = list(board.legal_moves)
    best_move = None
    best_eval = float('-inf')
    for move in legal_moves:
        board.push(move)
        eval = minimax(board, 2, float('-inf'), float('inf'), False)
        board.pop()
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move


# Função para exibir o menu de seleção de modo de jogo
def show_menu():
    font = pygame.font.Font(None, 36)
    text = "Escolha o modo de jogo:"
    text_ai = "1 - Jogar contra a Máquina"
    text_human = "2 - Jogar contra Humano"
    rendered_text = font.render(text, True, (255, 255, 255))
    rendered_text_ai = font.render(text_ai, True, (255, 255, 255))
    rendered_text_human = font.render(text_human, True, (255, 255, 255))
    screen.blit(rendered_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100))
    screen.blit(rendered_text_ai, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
    screen.blit(rendered_text_human, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return True
                elif event.key == pygame.K_2:
                    return False


# Função para desfazer a última jogada
def undo_move():
    if len(move_history) > 0:
        move = move_history.pop()
        board.pop()
        if len(move_history) > 0:
            move = move_history.pop()
            board.pop()


# Loop principal do jogo
selected_square = None
valid_moves = []

# Mostra o menu de seleção de modo de jogo
playing_against_ai = show_menu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            square = get_clicked_square(pos)
            piece = board.piece_at(square)

            if is_game_over():
                board.reset()

            if playing_against_ai and board.turn == chess.WHITE:
                pass
            elif selected_square is None and piece is not None and piece.color == board.turn:
                selected_square = square
                valid_moves = [move.to_square for move in board.legal_moves if move.from_square == square]
            elif selected_square is not None and square in valid_moves:
                move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    move_history.append(move)
                    board.push(move)
                selected_square = None
                valid_moves = []
            else:
                selected_square = None
                valid_moves = []

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                undo_move()

    if playing_against_ai and board.turn == chess.WHITE and not is_game_over():
        ai_move = get_best_move(board)
        move_history.append(ai_move)
        board.push(ai_move)

    screen.fill((0, 0, 0))
    draw_board()
    draw_pieces()
    draw_valid_moves(valid_moves)

    if is_check():
        font = pygame.font.Font(None, 24)
        text = "Xeque!"
        rendered_text = font.render(text, True, (255, 0, 0))
        screen.blit(rendered_text, (10, SCREEN_HEIGHT - 30))

    if is_game_over():
        font = pygame.font.Font(None, 36)
        text = "Fim de jogo: "
        if board.is_checkmate():
            text += "Xeque-mate!"
        elif board.is_stalemate():
            text += "Empate por afogamento!"
        elif board.is_insufficient_material():
            text += "Empate por material insuficiente!"
        text += " Clique para reiniciar."
        rendered_text = font.render(text, True, (255, 255, 255))
        screen.blit(rendered_text, (10, SCREEN_HEIGHT - 50))
        pygame.time.wait(1000)

    pygame.display.flip()
