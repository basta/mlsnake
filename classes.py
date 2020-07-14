import termdraw
bounds = [20,20]
import random
import time
class Field:
    def __init__(self, x, y, t="empty"):
        self.x = x
        self.y = y
        self.type = t
    
    def __str__(self):
        return self.type
    def __repr__(self):
        return self.type


class SnakePart:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dir = "up"
        self.tail = [self]
        self.add_apple = True

    def move(self):
        last_part_x = self.tail[-1].x
        last_part_y = self.tail[-1].y
        if len(self.tail) > 1:
            new_tail = [self] + [SnakePart(-1,-1) for i in range(len(self.tail)-1)]
            #termdraw.f.write(str(len(new_tail)) + " " + str(len(self.tail)))
            for i in range(1, len(self.tail)):
                new_tail[i].x = self.tail[i-1].x
                new_tail[i].y = self.tail[i-1].y
        
            self.tail = new_tail
        if self.dir == "up":
            self.y -= 1
        
        elif self.dir == "down":
            self.y += 1
        
        elif self.dir == "left":
            self.x -= 1
        
        elif self.dir == "right":
            self.x += 1
        
        if self.add_apple:
            self.tail.append(SnakePart(last_part_x, last_part_y))
            self.add_apple = False

        for i in range(len(self.tail)):
            if termdraw.stdscr != None:
                termdraw.stdscr.addstr(5, 22, "Score: " + str(len(self.tail)), termdraw.curses.color_pair(1))
        
        #termdraw.f.write(str(self.x) + " " + str(self.y) + "\n")
        for i in self.tail[1:]:
            if self.x == i.x and self.y == i.y:
                termdraw.f.write("Selfcollide\n")
                if termdraw.stdscr != None:
                    time.sleep(1)
                return False

        if (self.x < 0 or self.x >= bounds[0] or self.y < 0 or self.y >= bounds[1]):
            if termdraw.stdscr != None:
                termdraw.stdscr.addstr(20, 30, str("Kolize"))
            termdraw.f.write("wallcollide\n")
            time.sleep(1)
            return False
        return True

    def draw(self, arr):
        arr[self.x][self.y].type = "head"
        for part in self.tail[1:]:
            arr[part.x][part.y].type = "snake"
            

class Apple:
    def __init__(self):
        self.x = random.randrange(bounds[0])
        self.y = random.randrange(bounds[1])
    
    def consume(self):
        self.x = random.randrange(bounds[0])
        self.y = random.randrange(bounds[1])
    
    def draw(self, arr):
        arr[self.x][self.y].type = "apple"
