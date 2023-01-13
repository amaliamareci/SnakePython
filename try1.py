import pygame
import random
import sys
import json

#colors 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

SNAKE_BLOCK = 10

with open(sys.argv[1]) as f:
    data = json.load(f)

w = data['width']
h = data['height']

game_display = pygame.display.set_mode((w, h))

pygame.init() 
pygame.display.set_caption('Snake')
 
clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

highest_score = 0

def get_obstacles():
    """ Get obstacles coordinates from the json file and validates them
    :return: obstacles-list of tuples representing the coordinates for obstacles
    """

    obstacles = []
    for ob in data['obstacles']:
        if 10<ob['x']<w-10 and 10<ob['y']<h-10:
            obstacles.append((ob['x'], ob['y']))

    return obstacles

def your_score(score):
    """ Draw score on the screen for every step the player does
    :param score: player's score to be drawn on the screen
    :return: none
    """

    global highest_score
    if score > highest_score:
        highest_score = score
    value = score_font.render("Your Score: " + str(score), True, yellow)
    game_display.blit(value, [0, 0])
 
def message(message, color):
    """ Draw mesagge on the screen in the specified color
    :param message: a text to be drawn on the screen
    :param color: the color for the text
    :return: none
    """

    mesg = font_style.render(message, True, color)
    game_display.blit(mesg, [w / 6, h / 3])

def draw_obstacles(obstacles):
    """ Draw obstacles on the screen 
    :param obstacles: a list of tuples with obstacles coordinates
    :return: none
    """

    for ob in obstacles:
        pygame.draw.rect(game_display, red, [ob[0], ob[1], 10, 10])

def ending_scene():
    """ Ending scene for the game showing the highest 
    score for the player
    :return: none
    """
    
    game_display.fill(black)
    font = pygame.font.Font(None, 25)
    text = font.render("You highest score is " + str(highest_score) + " !!!", True, yellow)
    text_rect = text.get_rect(center=(w/2, h/2))
    game_display.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)
 
def gameLoop(w,h):
    """Used to draw the snake continuously, check if it eats the food, end of the game etc.
    It checks for player keyboard input(the arrow keys) for changing the direction and also
    for the ending screen checks if the players want to continue(keyboard input c) or to quit(keyboard input c).
    :param w: screen's width 
    :param h: screen's height
    :return: none
    """

    obstacles = get_obstacles()
    snake_speed = 10

    game_over = False
    game_close = False
 
    x1 = w / 2
    y1 = h / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_list = []
    snake_length = 1
 
    food_x = round(random.randrange(0, w - SNAKE_BLOCK) / 10.0) * 10.0
    food_y = round(random.randrange(0, h - SNAKE_BLOCK) / 10.0) * 10.0
 
    while not game_over:
 
        while game_close == True:
            game_display.fill(black)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            your_score(snake_length - 1)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        ending_scene()
                        game_over = True
                        game_close = False
                        
                    if event.key == pygame.K_c:
                        gameLoop(w,h)
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0
 
        if x1 >= w or x1 < 0 or y1 >= h or y1 < 0 or ((x1, y1) in obstacles) :
            game_close = True
            continue
        x1 += x1_change
        y1 += y1_change
        game_display.fill(black)
        draw_obstacles(obstacles)
        pygame.draw.rect(game_display, green, [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]
 
        for x in snake_list[:-1]:
            if x == snake_head  :
                game_close = True
 
        for x in snake_list:
            pygame.draw.rect(game_display, white, [x[0], x[1], SNAKE_BLOCK, SNAKE_BLOCK])
        your_score(snake_length - 1)
 
        pygame.display.update()
 
        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, w - SNAKE_BLOCK) / 10.0) * 10.0
            food_y = round(random.randrange(0, h - SNAKE_BLOCK) / 10.0) * 10.0
            while ((food_x, food_y) in obstacles) or food_y< 50:
                food_x = round(random.randrange(0, w - SNAKE_BLOCK) / 10.0) * 10.0
                food_y = round(random.randrange(0, h - SNAKE_BLOCK) / 10.0) * 10.0
            snake_length += 1
            snake_speed += 1
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 
gameLoop(w,h)