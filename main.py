import termdraw
import time
import curses
import random
import traceback
from classes import *
import ml
import plotit

field_map = []
selfcollides = []

last_time = time.time()
last_dir = "up"
timer= 1

total_ml_time = 0

snake = Snake(10, 10)
apple = Apple()
results = open("results.txt", "w+")
def draw_fields(fields):
    ret = []
    
    for x in range(len(fields)):
        ret.append([])
        for y in range(len(fields[x])):
            field = fields[x][y]
            ret[x].append("")
        
            if field.type == "apple":
                ret[x][y] = "apple"
            elif field.type == "snake":
                ret[x][y] = "snake"
            elif field.type == "head":
                ret[x][y] = "head"
            else:
                ret[x][y] = "empty"

    return ret

def clean_fields(fields):
    for x in fields:
        for y in x:
            y.type = "empty"
    return fields

def mainloop():
    global timer
    global last_time
    global last_dir
    global total_ml_time
    timer += time.time() - last_time
    last_time = time.time()
    #termdraw.f.write(termdraw.read_input())
    inp = ""
    if termdraw.stdscr != None:
        inp = termdraw.read_input()
    if inp == curses.KEY_UP and last_dir != "down":
        snake.dir = "up"
    elif inp == curses.KEY_RIGHT and last_dir != "left":
        snake.dir = "right"
    elif inp == curses.KEY_DOWN and last_dir != "up":
        snake.dir = "down"
    elif inp == curses.KEY_LEFT and last_dir != "right":
        snake.dir = "left"

    if apple.x == snake.x and snake.y == apple.y:
        #termdraw.stdscr.addstr(10, 39, "Consumed")
        apple.consume()
        snake.add_apple = True
        ml.eaten(snake)
    else:
        pass
        #termdraw.stdscr.addstr(10, 39, "         ")
    
    #termdraw.stdscr.addstr(10, 40, str(timer))
    
    if timer > 0.015 or termdraw.stdscr == None:
        time1 = time.time()
        snake.dir = ml.ml(snake, apple)
        total_ml_time += time.time()-time1
        last_dir = snake.dir
        #termdraw.f.write(snake.dir + "\n")
        if len(snake.tail) > 2:
            pass
            # print([[i.x, i.y] for i in snake.tail], snake.dir, list(ml.current_state.poss_dir.values()))
        if not snake.move():
            #ml.statelist.save()
            return False
        else:
            timer = 0
            return True
        #termdraw.f.write(str(field_map))
    return True        
generations = 0

if __name__ == "__main__":
    for x in range(bounds[0]):
        field_map.append([])
        for y in range(bounds[1]):
            field_map[x].append(Field(x, y))

    try:
        graphical = False
        if graphical:
            termdraw.start()
            termdraw.draw_box()
            snake.draw(field_map)
        while True:
            if not mainloop(): 
                termdraw.f.write(str("Delka hada: " + str(len(snake.tail))+"\n"))
                #ml.statelist.save()
                if generations % 20 == 0:
                    ml.o = open("out.log", "w+")
                    print("Generations: " ,generations)
                
                if not graphical:
                    print(str(len(snake.tail)), file=results)
                    print(len(snake.tail), len(ml.statelist.states))
                    print("Total time taken by ML: ", total_ml_time)
                total_ml_time = 0
                ml.collided(snake)
                #termdraw.f.write(str(ml.statelist.states))
                snake = Snake(10, 10)
                ml.moves = []
                ml.turns = 0
                apple.consume()
                
                if generations > 500:
                    graphical = True
                    termdraw.start()
                    termdraw.draw_box()
                    snake.draw(field_map)

                if generations > 150:
                    ml.statelist.save()
                    results.close()
                    plotit.draw(open("results.txt","r"))
                    break
                else:
                    generations += 1


            if graphical:
                field_map = clean_fields(field_map)
                apple.draw(field_map)
                snake.draw(field_map)
                termdraw.draw_screen(draw_fields(field_map))
                termdraw.refresh()
    finally:
        termdraw.end()