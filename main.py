import pygame
import random

# Инициализация pygame
pygame.init()

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 20
FPS = 10

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')


class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = pygame.K_RIGHT

    def move(self):
        head = self.body[0]
        if self.direction == pygame.K_UP:
            new_head = (head[0], head[1] - CELL_SIZE)
        elif self.direction == pygame.K_DOWN:
            new_head = (head[0], head[1] + CELL_SIZE)
        elif self.direction == pygame.K_LEFT:
            new_head = (head[0] - CELL_SIZE, head[1])
        elif self.direction == pygame.K_RIGHT:
            new_head = (head[0] + CELL_SIZE, head[1])
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        tail = self.body[-1]
        if self.direction == pygame.K_UP:
            new_tail = (tail[0], tail[1] + CELL_SIZE)
        elif self.direction == pygame.K_DOWN:
            new_tail = (tail[0], tail[1] - CELL_SIZE)
        elif self.direction == pygame.K_LEFT:
            new_tail = (tail[0] + CELL_SIZE, tail[1])
        elif self.direction == pygame.K_RIGHT:
            new_tail = (tail[0] - CELL_SIZE, tail[1])
        self.body.append(new_tail)

    def check_collision(self):
        head = self.body[0]
        return (
            head[0] < 0 or head[0] >= SCREEN_WIDTH or
            head[1] < 0 or head[1] >= SCREEN_HEIGHT or
            head in self.body[1:]
        )

    def set_direction(self, direction):
        # Избежать движения змейки в противоположном направлении
        if (direction == pygame.K_UP and self.direction != pygame.K_DOWN):
            self.direction = direction
        elif (direction == pygame.K_DOWN and self.direction != pygame.K_UP):
            self.direction = direction
        elif (direction == pygame.K_LEFT and self.direction != pygame.K_RIGHT):
            self.direction = direction
        elif (direction == pygame.K_RIGHT and self.direction != pygame.K_LEFT):
            self.direction = direction
class Food:
    def __init__(self):
        self.position = (random.randint(0, (SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                         random.randint(0, (SCREEN_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

    def respawn(self):
        self.position = (random.randint(0, (SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                         random.randint(0, (SCREEN_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)


def main():
    snake = Snake()
    food = Food()
    clock = pygame.time.Clock()
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                snake.set_direction(event.key)

        snake.move()

        # Проверка на поедание еды
        if snake.body[0] == food.position:
            snake.grow()
            food.respawn()
            score += 1

        # Проверка на столкновение
        if snake.check_collision():
            running = False

        screen.fill(BLACK)

        # Рисование змейки
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

        # Рисование еды
        pygame.draw.rect(screen, RED, pygame.Rect(food.position[0], food.position[1], CELL_SIZE, CELL_SIZE))

        # Отображение счета
        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()