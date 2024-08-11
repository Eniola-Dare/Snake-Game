import pygame
from random import choice
from sys import exit


pygame.init()

WIDTH = HEIGHT = 700
BG_COLOR = 0,0,0
BLOCKS = 20
BLOCK_SIZE = WIDTH//BLOCKS
GRID = [(i,j) for i in range(BLOCKS) for j in range(BLOCKS)]
SPEED = 150
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SNAKE")
clock = pygame.time.Clock()
font_64 = pygame.font.Font("Font.ttf", 64)
font_32 = pygame.font.Font("Font.ttf", 32)


def quit_game():
    pygame.quit()
    exit()

def new_food_position(body):
    if len(body) == len(GRID):
        return  None
    empty_space = [coordinate for coordinate in GRID if coordinate not in body]
    return choice(empty_space)

def position_from_coordinate(coordinate):
    return coordinate[0]*BLOCK_SIZE, coordinate[1]*BLOCK_SIZE

class Snake:
    def __init__(self, coordinate=(BLOCKS//2,BLOCKS//2)):
        self.direction = 0,-1
        self.body = [coordinate]
        self.color = 0,255,0
        self.head_color = 0,200,0
        
    def move(self):
        new_head = self.body[-1][0]+self.direction[0], self.body[-1][1]+self.direction[1]
        self.body.append(new_head)
        del self.body[0]

    def set_direction(self, new_x, new_y):
        if new_x == self.direction[0]*-1 or new_y == self.direction[1]*-1:
            return
        self.direction = new_x, new_y
    
    def draw(self):
        for index, square in enumerate(self.body):
            x, y = position_from_coordinate(square)
            pygame.draw.rect(screen, self.head_color if index==len(self.body)-1 else self.color ,pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))

    def grow(self):
        self.body.append(self.body[-1])

    def eat(self, food):
        if self.body[-1] == food:
            self.grow()
            return True
        return False
        
    def outside(self):
        x, y = position_from_coordinate(self.body[-1])
        return not (WIDTH>x>=0 and HEIGHT>y>=0)

    def eaten_self(self):
        return self.body[-1] in self.body[:-2]


def after_game_window(text):
    text_surface = font_64.render(text, True, (225,225,225))
    text_rect = text_surface.get_rect()
    text_rect.center = WIDTH//2, HEIGHT//2

    press_any_key = font_32.render("PRESS ANY KEY TO CONTINUE", True, (225,225,225))
    press_any_key_rect = press_any_key.get_rect()
    press_any_key_rect.center = WIDTH//2, HEIGHT//2 + 100
    
    screen.fill(BG_COLOR)
    while True:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               quit_game()
            if event.type == pygame.KEYDOWN:
                return

        screen.fill(BG_COLOR)
        
        screen.blit(text_surface, text_rect)
        screen.blit(press_any_key, press_any_key_rect)
        
        pygame.display.update()

def main():
    play = False

    snake_surface = font_64.render("SNAKE", True, (225,225,225))
    snake_surface_rect = snake_surface.get_rect()
    snake_surface_rect.center = WIDTH//2, HEIGHT//2
    
    press_any_key = font_32.render("PRESS ANY KEY TO PLAY", True, (225,225,225))
    press_any_key_rect = press_any_key.get_rect()
    press_any_key_rect.center = WIDTH//2, HEIGHT//2 + 100
    while True:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               quit_game()
            if event.type == pygame.KEYDOWN:
                play = True

        if play:
            won = game_window()
            play = False
            if won:
                after_game_window("YOU WON :)")
            else:
                after_game_window("GAME OVER")

        screen.fill(BG_COLOR)
        
        screen.blit(snake_surface, snake_surface_rect)
        screen.blit(press_any_key, press_any_key_rect)
        
        pygame.display.update()

def game_window():
    snake = Snake()
    move = pygame.USEREVENT
    pygame.time.set_timer(move, SPEED)
    food = new_food_position(snake.body)

    score_surface = font_32.render("Score: 1", True, (225,225,225))
    
    run = True
    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == move:
                snake.move()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            snake.set_direction(0,1)
        if keys[pygame.K_UP]:
            snake.set_direction(0,-1)
        if keys[pygame.K_RIGHT]:
            snake.set_direction(1,0)
        if keys[pygame.K_LEFT]:
            snake.set_direction(-1,0)

        if snake.outside() or snake.eaten_self():
            return False
        if snake.eat(food):
            score_surface = font_32.render("Score: "+str(len(snake.body)), True, (225,225,225))
            food = new_food_position(snake.body)
            if not food:
                return True
        
        screen.fill(BG_COLOR)

        pygame.draw.rect(screen, (255, 0, 0) ,pygame.Rect(*position_from_coordinate(food), BLOCK_SIZE, BLOCK_SIZE))
        snake.draw()
        screen.blit(score_surface, (10,10))
        
        pygame.display.update()


if __name__ == "__main__":
    main()
