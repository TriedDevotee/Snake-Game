import random
import tkinter as tk
import sounddevice as sd
import numpy as np

direction = "RIGHT"
nextDirection = "RIGHT"

maxLength = 4
numFruit = 0

CELLSIZE = 40

score = 0

snakeHead = [120, 120]

def get_volume():
    duration = 0.05
    sampleRate = 44100


def set_up_body():
    partCoords = [[120, 120]]

    return partCoords

def draw_body_parts(partCoords):

    global CELLSIZE
    
    SNAKECOLOR = "lime"

    for coords in partCoords:
        pulse = get_pulse_test()

        offset = pulse / 2

        startX = coords[0] - offset
        startY = coords[1] - offset

        endX = startX + CELLSIZE + offset 
        endY = startY + CELLSIZE + offset

        canvas.create_rectangle(startX - 2, startY - 2, endX + 2, endY + 2, fill="black", outline="black")
        canvas.create_rectangle(startX, startY, endX, endY, fill=SNAKECOLOR, outline="black")

    return

def get_pulse_test():
    return random.randint(1, 150) / 10

def add_new_part(direction, partCoords):

    global CELLSIZE

    prevX = partCoords[-1][0]
    prevY = partCoords[-1][1]

    if direction == "UP":
        partCoords.append([prevX, prevY - CELLSIZE])
    elif direction == "RIGHT":
        partCoords.append([prevX + CELLSIZE, prevY])
    elif direction == "DOWN":
        partCoords.append([prevX, prevY + CELLSIZE])
    else:
        partCoords.append([prevX - CELLSIZE, prevY])

    if len(partCoords) > maxLength:
        partCoords.pop(0)

    return partCoords

def update_direction(event):
    global nextDirection
    global direction

    OPPOSITE = {
        "UP" : "DOWN",
        "DOWN" : "UP",
        "LEFT" : "RIGHT",
        "RIGHT" :"LEFT"  
    }

    newDirection = event.keysym.upper()

    if newDirection in OPPOSITE and OPPOSITE[newDirection] != direction:
        nextDirection = newDirection

def spawn_fruit(fruit):
    global numFruit
    global CELLSIZE

    while numFruit < MAXFRUIT:
        fruit.append([random.randint(0, 800 // CELLSIZE - 1) * CELLSIZE, random.randint(0, 800 // CELLSIZE - 1) * CELLSIZE])

        numFruit += 1

    return fruit

def update_fruit(fruit, snakeHead):
    global numFruit
    global maxLength
    global score
    
    fruitToPop = []

    for i in range(len(fruit)):
        if fruit[i][0] == snakeHead[0] and fruit[i][1] == snakeHead[1]:
            fruitToPop.append(i)
    
    for index in reversed(fruitToPop):
        fruit.pop(index)
        numFruit -= 1
        maxLength += 1

        score += 1

    return

def draw_fruit(fruit):

    global CELLSIZE

    FRUITCOLOR = "red"

    for fruits in fruit:
        canvas.create_rectangle(fruits[0], fruits[1], fruits[0] + CELLSIZE, fruits[1] + CELLSIZE, fill=FRUITCOLOR)
    
    return

def check_for_death(partCoords):
    global snakeHead

    if snakeHead[0] < 0 or snakeHead[0] >= 800 or snakeHead[1] < 0 or snakeHead[1] >= 800:
        quit()

    
    for chunk in partCoords[:-1]:
        if snakeHead[0] == chunk[0] and snakeHead[1] == chunk[1]:
            quit()

def draw_score():
    global score

    canvas.create_text(
        50, 50,
        anchor="nw",
        text=f"Score: {score}",
        fill="white",
        font=("Comic Sans MS", 24, "bold")
    )

def draw_grid_lines():
    numRows = WIDTH // CELLSIZE
    numColumns = HEIGHT // CELLSIZE

    for i in range(numColumns + 1):
        canvas.create_line(i * CELLSIZE, 0, i * CELLSIZE, HEIGHT, fill="dimgray")

    for i in range(numRows + 1):
        canvas.create_line(0, i * CELLSIZE, WIDTH, i * CELLSIZE, fill="dimgray")


def game_loop():

    global snakeHead, direction

    canvas.delete("all")

    direction = nextDirection

    draw_grid_lines()

    add_new_part(direction, partCoords)
    draw_body_parts(partCoords)

    snakeHead = partCoords[-1]

    update_fruit(fruit, snakeHead)
    draw_fruit(fruit)
    spawn_fruit(fruit)

    draw_score()

    check_for_death(partCoords)

    root.after(200, game_loop)



root = tk.Tk()

HEIGHT = 800
WIDTH = 800

MAXFRUIT = 1

root.bind("<KeyPress>", update_direction)

root.title("Snake")

partCoords = set_up_body()

fruit = []
fruit = spawn_fruit(fruit)

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="Black")
canvas.pack()

game_loop()

root.mainloop()
    