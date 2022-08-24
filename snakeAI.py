import threading
import time
import numpy as np
from tkinter import *
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Game:
    class Snake:
        def __init__(self, outer_instance):
            self.body_size = BODY_PARTS
            self.coordinates = []
            self.squares = []
            for i in range(0, BODY_PARTS):
                self.coordinates.append([0, 0])

            for x, y in self.coordinates:
                square = outer_instance.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR,
                                                                tags="snake")
                self.squares.append(square)

    class Apple:
        def __init__(self, outer_instance):
            x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
            self.coordinates = [x, y]
            outer_instance.canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags="food")

    def next_turn(self, action):
        self.change_direction(action)

        x, y = self.snake.coordinates[0]
        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE

        self.snake.coordinates.insert(0, (x, y))
        square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
        self.snake.squares.insert(0, square)

        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.reward += 10
            self.score += 1
            self.label.config(text="score:{}".format(self.score))
            self.canvas.delete("food")
            food = self.Apple(self)

        else:
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        if self.check_collisions(self.snake):
            self.reward -= 10
            self.isDone = True
        else:
            self.timer += 1
            self.window.after(SPEED, self.next_turn, action)

        print("i reached immortality")
        return self.reward, self.isDone, self.score


    def change_direction(self, action):
        new_direction = ''
        new_dir = ['right', 'down', 'left', 'up']
        index = new_dir.index(self.direction)
        if np.array_equal(action, [1, 0, 0]):
            new_direction = self.direction
        elif np.array_equal(action, [0, 1, 0]):
            index = (index + 1) % 4
            new_direction = new_dir[index]
        else:
            index = (index - 1) % 4
            new_direction = new_dir[index]

        if new_direction == 'left':
            if self.direction != 'right':
                self.direction = new_direction

        if new_direction == 'right':
            if self.direction != 'left':
                self.direction = new_direction

        if new_direction == 'up':
            if self.direction != 'down':
                self.direction = new_direction

        if new_direction == 'down':
            if self.direction != 'up':
                self.direction = new_direction



    def check_collisions(self,snake):
        x, y = snake.coordinates[0]
        if x < 0 or x >= GAME_WIDTH:
            return True

        if y < 0 or y >= GAME_HEIGHT:
            return True

        for snakeSegment in snake.coordinates[1:]:
            if x == snakeSegment[0] and y == snakeSegment[1]:
                return True

        return False

    def is_collision(self,snake,x,y):
        if x < 0 or x >= GAME_WIDTH:
            return True

        if y < 0 or y >= GAME_HEIGHT:
            return True

        for snakeSegment in snake.coordinates[1:]:
            if x == snakeSegment[0] and y == snakeSegment[1]:
                return True

        return False

    def reset(self):
        self.canvas.delete(ALL)

        self.isDone = False
        self.reward = 0
        self.timer = 0
        self.score = 0
        self.direction = 'down'
        self.label.config(text="score:{}".format(self.score))
        self.window.update()

        self.snake = self.Snake(self)
        self.food = self.Apple(self)
        self.action = [1, 0, 0]
        self.next_turn(self.action)

    def set_action(self , action):
        self.action = action;

    def thread_game(self):
        self.isDone = False
        self.reward = 0
        self.timer = 0
        self.window = Tk()
        self.window.title("Snake game")
        self.window.resizable(False, False)
        self.score = 0
        self.direction = 'down'
        self.label = Label(self.window, text="Score:{}".format(self.score), font=('consolas', 40))
        self.label.pack()
        self.canvas = Canvas(self.window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()
        self.window.update()
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.snake = self.Snake(self)
        self.food = self.Apple(self)
        self.action = [1, 0, 0]
        self.next_turn(self.action)
        self.start_game();

    def __init__(self):
        self.action = None
        self.food = None
        self.snake = None
        self.canvas = None
        self.label = None
        self.direction = None
        self.score = None
        self.window = None
        self.timer = None
        self.reward = None
        self.isDone = None
        threading.Thread(target=self.thread_game , args=()).start()




    def start_game(self):
        self.window.mainloop()