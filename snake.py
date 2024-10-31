import pygame
from random import randint

# Инициализация библиотеки Pygame
pygame.init()

# Установка параметров экрана и сетки
SCR_WIDTH, SCR_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCR_WIDTH // GRID_SIZE
GRID_HEIGHT = SCR_HEIGHT // GRID_SIZE

# Задание направлений для движения змейки
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Определение цветов для элементов игры
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (0, 0, 0)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
WHITE = (255, 255, 255)

# Установка начальной скорости и границ увеличения скорости
INITIAL_SPEED = 10
SPEED_INCREMENT = 5
MIN_SPEED = 10
MAX_SPEED = 25

# Создание основного окна игры
scr = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
pygame.display.set_caption('Змейка')

# Инициализация таймера и шрифта
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 25)

# Экран для отображения
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
screen = pygame.Surface((150, 150))

# Базовый класс для игровых объектов
class GameObject:
    """
    Базовый класс GameObject. Содержит свойства позиции и цвета объекта.
    """
    position = (0, 0)
    body_color = (0, 0, 0)

    def __int__(self):
        """
        Фейковый метод инициализации.
        """
        return 0

    def draw():
        """
        Фейковый метод отрисовки.
        """
        return 0

# Класс для змейки
class Snake(GameObject):
    """
    Класс Snake для управления змейкой в игре.
    """
    position = (0, 0)
    body_color = (0, 0, 0)
    positions = [(0, 0), (0, 0), (0, 0)]
    direction = 'UP'

    def __init__(self):
        """
        Инициализация змейки с начальной позицией, направлением, флагом роста и счетом.
        """
        self.positions = [
            (GRID_WIDTH // 2, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2, GRID_HEIGHT // 2 + 1),
            (GRID_WIDTH // 2, GRID_HEIGHT // 2 + 2)
        ]
        self.direction = RIGHT
        self.grow = False
        self.score = 0

    def get_head_position():
        """
        Возвращает текущую позицию головы змейки.
        """
        return 0

    def reset():
        """
        Сбрасывает состояние змейки при начале новой игры.
        """
        return 0

    def move(self):
        """
        Двигает змейку в текущем направлении, проверяет столкновение с телом змейки.
        Возвращает False при столкновении, иначе True.
        """
        current_head = self.positions[0]
        x, y = self.direction
        a = (current_head[0] + x) % GRID_WIDTH
        b = (current_head[1] + y) % GRID_HEIGHT
        new_head = (a, b)

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
        Обновляет направление движения змейки.
        Параметры: direction - кортеж (dx, dy) нового направления.
        """
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def draw(self):
        """
        Отрисовывает змейку на экране.
        """
        for pos in self.positions:
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE,
                               GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(scr, SNAKE_COLOR, rect)
            pygame.draw.rect(scr, BORDER_COLOR, rect, 1)

# Класс для яблока
class Apple(GameObject):
    """
    Класс Apple для управления яблоком в игре.
    """

    position = (0, 0)
    body_color = (0, 0, 0)

    def __init__(self):
        """
        Устанавливает начальную позицию яблока случайным образом на игровом поле.
        """
        a = randint(0, GRID_WIDTH - 1)
        b = randint(0, GRID_HEIGHT - 1)
        self.position = (a, b)

    def draw(self):
        """
        Отрисовывает яблоко на экране.
        """
        a = self.position[0] * GRID_SIZE
        b = self.position[1] * GRID_SIZE
        rect = pygame.Rect(a, b, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(scr, APPLE_COLOR, rect)
        pygame.draw.rect(scr, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """
        Изменяет позицию яблока на случайную.
        """
        a = randint(0, GRID_WIDTH - 1)
        b = randint(0, GRID_HEIGHT - 1)
        self.position = (a, b)

# Управление движением змейки
def handle_keys(snake):
    """
    Управляет событиями нажатия клавиш для движения змейки и изменения скорости.
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

# Экран после завершения игры
def game_over_scr(score, high_score):
    """
    Отображает экран завершения игры с результатами и рекордом.
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

# Главная функция игры
def main():
    """
    Главная функция, запускающая игру. Управляет циклом игры, объектами и отрисовкой.
    """
    global speed
    speed = INITIAL_SPEED
    snake = Snake()
    apple = Apple()
    high_score = 0

    while True:
        handle_keys(snake)

        # Перемещение змейки, проверка столкновений
        if not snake.move():
            if snake.score > high_score:
                high_score = snake.score
            game_over_scr(snake.score, high_score)
            snake = Snake()
            apple.randomize_position()

        # Проверка на поедание яблока
        if snake.positions[0] == apple.position:
            snake.grow = True
            snake.score += 1
            apple.randomize_position()

        # Очистка экрана и отрисовка игровых объектов
        scr.fill(BOARD_BACKGROUND_COLOR)
        pygame.draw.rect(scr, BORDER_COLOR, (0, 0, SCR_WIDTH, SCR_HEIGHT), 2)
        snake.draw()
        apple.draw()

        # Отображение текущего счета и скорости
        score_text = font.render(f'Счет: {snake.score}', True, WHITE)
        scr.blit(score_text, (10, 10))
        speed_text = font.render(f'Скорость: {speed}', True, WHITE)
        scr.blit(speed_text, (10, 30))

        # Обновление экрана и ограничение кадров
        pygame.display.flip()
        clock.tick(speed)

# Запуск основной функции, если скрипт выполняется напрямую
if __name__ == "__main__":
    main()
