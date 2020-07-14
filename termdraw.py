import curses
import time

stdscr = None #Setup standardscreen



f = open("error.log", "a+")


def start():
    global stdscr
    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    stdscr.nodelay(True)
    stdscr.keypad(True)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK) #APPLE 1 RED
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) #SNAKE 2 GREEN
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK) #NOTHING 3 BLACK
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK) #WALL 4 WHITE
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK) #HEAD 5 WHITE

def end():
    if stdscr is not None:    
        curses.nocbreak()
        curses.echo()
        curses.endwin()

def draw_box():
    for i in range(0, 22):
        #f.write(str(stdscr.getyx()))
        stdscr.move(0, i)
        stdscr.addstr("█")
        stdscr.move(i, 0)
        stdscr.addstr("█")
        stdscr.move(i, 21)
        stdscr.addstr("█")
        stdscr.move(21, i)
        stdscr.addstr("█")

def refresh():
    stdscr.refresh()

def read_input():
    inp = stdscr.getch()
    return inp


def draw_screen(arr):
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            if arr[x][y] == "apple":
                stdscr.addstr(y+1,x+1, "█", curses.color_pair(1))
            if arr[x][y] == "snake":
                stdscr.addstr(y+1, x+1, "█", curses.color_pair(2))
            if arr[x][y] == "empty":
                stdscr.addstr(y+1, x+1, "█", curses.color_pair(3))
            if arr[x][y] == "head":
                stdscr.addstr(y+1, x+1, "█", curses.color_pair(5))
