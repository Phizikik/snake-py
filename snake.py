import pygame
from random import randint

# Инициализация Pygame и установка размеров экрана и сетки
pygame.init()

SCR_WIDTH, SCR_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCR_WIDTH // GRID_SIZE
GRID_HEIGHT = SCR_HEIGHT // GRID_SIZE

# Направления движения змейки
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета для различных элементов игры
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (0, 0, 0)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
WHITE = (255, 255, 255)

# Параметры скорости
INITIAL_SPEED = 10
SPEED_INCREMENT = 5
MIN_SPEED = 10
MAX_SPEED = 25

# Создание экрана для отображения игры
scr = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
pygame.display.set_caption('Змейка')

# Установка часов и шрифта для отображения текста на экране
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 25)

# Пустые размеры экрана для дополнительных функций (не используются)
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
screen = pygame.Surface((150, 150))


class GameObject:
    """
    Базовый класс для объектов в игре, таких как змейка и яблоко.
    Используется для наследования и добавления общей функциональности.
    """
    
    position = (0, 0)
    body_color = (0, 0, 0)

    def __int__(self):
        """
        Конструктор по умолчанию
        """
        return 0

    def draw(self):
        """
        Функция для рисования объекта на экране.
        """
        return 0


class Snake(GameObject):
    """
    Класс змейки, описывающий ее поведение, внешний вид и взаимодействие.
    """
    
    position = (0, 0)
    body_color = (0, 0, 0)
    positions = [(0, 0), (0, 0), (0, 0)]
    direction = 'UP'

    def __init__(self):
        """
        Инициализация змейки в центре экрана, настройка начального направления и счета.
        """
        self.positions = [
            (GRID_WIDTH // 2, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2, GRID_HEIGHT // 2 + 1),
            (GRID_WIDTH // 2, GRID_HEIGHT // 2 + 2)
        ]
        self.direction = RIGHT
        self.grow = False
        self.score = 0

    def move(self):
        """
        Двигает змейку в заданном направлении.
        Если происходит столкновение, возвращает False, иначе True.
        """
        current_head = self.positions[0]
        x, y = self.direction
        a = (current_head[0] + x) % GRID_WIDTH
        b = (current_head[1] + y) % GRID_HEIGHT
        new_head = (a, b)

        # Проверка столкновения головы с телом
        if new_head in self.positions:
            return False
        else:
            self.positions.insert(0, new_head)
            if not self.grow:
                self.positions.pop()
            self.grow = False
            return True

    def update_direction(self, direction):
        """
        Меняет направление движения змейки, если оно не противоположно текущему.
        """
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def draw(self):
        """
        Рисует змейку на экране, используя список ее позиций.
        """
        for pos in self.positions:
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE,
                               GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(scr, SNAKE_COLOR, rect)
            pygame.draw.rect(scr, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """
    Класс яблока, описывающий его поведение, позицию и внешний вид.
    """

    def __init__(self):
        """
        Инициализация яблока со случайной начальной позицией на экране.
        """
        a = randint(0, GRID_WIDTH - 1)
        b = randint(0, GRID_HEIGHT - 1)
        self.position = (a, b)

    def draw(self):
        """
        Рисует яблоко на экране в его текущей позиции.
        """
        a = self.position[0] * GRID_SIZE
        b = self.position[1] * GRID_SIZE
        rect = pygame.Rect(a, b, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(scr, APPLE_COLOR, rect)
        pygame.draw.rect(scr, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """
        Перемещает яблоко в новую случайную позицию на экране.
        """
        a = randint(0, GRID_WIDTH - 1)
        b = randint(0, GRID_HEIGHT - 1)
        self.position = (a, b)


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш для управления змейкой и изменением скорости.
    """
    global speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif event.key in (
                pygame.K_UP,
                pygame.K_DOWN,
                pygame.K_LEFT,
                pygame.K_RIGHT
            ):
                direction_map = {
                    pygame.K_UP: UP,
                    pygame.K_DOWN: DOWN,
                    pygame.K_LEFT: LEFT,
                    pygame.K_RIGHT: RIGHT
                }
                snake.update_direction((direction_map[event.key]))
            elif event.key == pygame.K_q:
                speed = max(MIN_SPEED, speed - SPEED_INCREMENT)
            elif event.key == pygame.K_w:
                speed = min(MAX_SPEED, speed + SPEED_INCREMENT)


def game_over_scr(score, high_score):
    """
    Отображает экран окончания игры, позволяет выйти или перезапустить игру.
    """
    while True:
        scr.fill(BOARD_BACKGROUND_COLOR)

        game_over_text = font.render('Вы проиграли!', True, WHITE)
        score_text = font.render(f'Ваш результат: {score}', True, WHITE)
        high_score_text = font.render(f'Рекорд: {high_score}', True, WHITE)
        exit_text = font.render('ESC - выйти', True, WHITE)
        continue_text = font.render('SPACE - продолжить', True, WHITE)

        scr.blit(game_over_text, (SCR_WIDTH // 2 - 50, SCR_HEIGHT // 2 - 50))
        scr.blit(score_text, (SCR_WIDTH // 2 - 70, SCR_HEIGHT // 2 - 28))
        scr.blit(high_score_text, (SCR_WIDTH // 2 - 35, SCR_HEIGHT // 2))
        scr.blit(exit_text, (SCR_WIDTH // 2 - 50, SCR_HEIGHT // 2 + 28))
        scr.blit(continue_text, (SCR_WIDTH // 2 - 90, SCR_HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    return


def main():
    """
    Главная функция игры, инициирует объекты змейки и яблока и запускает основной цикл игры.
    """
    global speed
    speed = INITIAL_SPEED
    snake = Snake()
    apple = Apple()
    high_score = 0

    while True:
        # Управление змейкой
        handle_keys(snake)

        # Проверка столкновений и управление позициями
        if not snake.move():
            if snake.score > high_score:
                high_score = snake.score
            game_over_scr(snake.score, high_score)
            snake = Snake()
            apple.randomize_position()

        # Проверка столкновения змейки с яблоком
        if snake.positions[0] == apple.position:
            snake.grow = True
            snake.score += 1
            apple.randomize_position()

        # Отрисовка элементов игры на экране
        scr.fill(BOARD_BACKGROUND_COLOR)

        pygame.draw.rect(scr, BORDER_COLOR, (0, 0, SCR_WIDTH, SCR_HEIGHT), 2)

        snake.draw()
        apple.draw()

        # Отображение текущего счета и скорости
        score_text = font.render(f'Счет: {snake.score}', True, WHITE)
        scr.blit(score_text, (10, 10))
        speed_text = font.render(f'Скорость: {speed}', True, WHITE)
        scr.blit(speed_text, (10, 30))

        pygame.display.flip()
        clock.tick(speed)


if __name__ == "__main__":
    main()
