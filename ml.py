import typing
import random
import math
from classes import *

statesave_filename = "state.txt"

o = open("out.log", "w+")

current_state = None

degrees_per_state = 360/8

class Move:
    def __init__(self, state, dir):
        self.dir = dir
        self.state: State = state

    def reward(self, custom_val = 0.2):
        # Here, modify the reward mechanism
        self.state.dir_weights[self.dir] += custom_val

    def punish(self, custom_val=0.1):
        if self.dir != "" and self.state.dir_weights[self.dir] > 0:
            self.state.dir_weights[self.dir] -= random.uniform(0, custom_val * 2)
        for i in self.state.dir_weights:
            if i != self.dir and "" != i:
                self.state.dir_weights[i] += custom_val


class State:
    def __init__(self, id, apple_dir, dir_weights = None):
        self.id = id
        self.apple_dir : float = apple_dir
        
        if dir_weights is None:
            dir_weights = {}
            for i in ["up", "left", "right", "down"]:
                dir_weights[i] = 0.2 + random.uniform(-0.2, 0.2)

        self.dir_weights : typing.Dict[str, float] = dir_weights

    
    def __cmp__(self, other):
        return (self.apple_dir > other.apple_dir)
    
    def similiarity_to(self, other) -> float:
        #print("Similiarity is: ", 1 - abs((self.apple_dir - other.apple_dir) / (math.pi*2)), self.apple_dir, other.apple_dir, file=o)
        return 1 - abs((self.apple_dir - other.apple_dir) / (math.pi*2))

    def coeff_with(self, other) -> float:
        coeff = 0
        coeff += self.similiarity_to(other) * 1 #Here, maybe increase the weight of similiarity
        #coeff += other.best_weight()[1] * 0 #Here, maybe modify the weight of state's weight
        
        return coeff

    def best_weight(self, poss_dir):
        best_weight = -1
        best_dir = ""

        for i in self.dir_weights:
            if self.dir_weights[i] > best_weight and poss_dir[i]:
                best_weight = self.dir_weights[i]
                best_dir = i 
        return [best_dir, best_weight]
    
    def __str__(self):
        return str(self.apple_dir) + str(self.dir_weights)

class StateList:
    def __init__(self):
        self.states : typing.List[State] = []
    
    def load(self):
        f = open(statesave_filename, "r")
        line = f.readline()
        while line != "":
            line = line.split()
            self.states.append(State(int(line[0]), float(line[1]), {"up": bool(line[2]), "left": bool(line[3]), "right": bool(line[4]), "down": bool(line[5])}))
        f.close()

    def save(self):
        #self.states = sorted(self.states)        o = open(statesave_filename, "w+")
        s = open(statesave_filename, "w+")
        for i, state in enumerate(self.states):
            state.id = i
            for ii in ["up", "left", "right", "down"]:
                s.write(str(state.dir_weights[ii]))
            s.write("\n")
    
    def create(self):
        for i in range(int(360/degrees_per_state)):
            self.states.append(State(i, i*degrees_per_state))

    def __iter__(self):
        return iter(self.states)
    

    def __str__(self):
        return str([str(i)+"\n" for i in self.states])


statelist = StateList()
statelist.create()
moves : typing.List[Move] = []

def find_best_state(state: State, statearr: StateList):
    return statearr.states[int(math.degrees(state.apple_dir)/degrees_per_state)-1]

turns = 0
def eaten(snake):
    global moves, turns
    [i.reward(custom_val=len(snake.tail)/10-0.2) for i in moves[-100:]] #Here, modify the amount of rewarded moves
    moves = []
    o.writelines(["jablko snězeno"])
    turns = 0

def collided(snake):
    global moves, turns
    [i.punish(custom_val=0.4) for i in moves[-100:]] #Here, modify the amount of rewarded moves
    moves = []
    turns = 0

    
def ml(snake : Snake, apple : Apple):
    global moves, turns, current_state
    turns += 1
    poss_dir = {"up": True, "left": True, "right": True, "down" : True}
    for i in snake.tail[1:]:
        if i.x == snake.x + 1 and i.y == snake.y:
            poss_dir["right"] = False
        if i.x == snake.x - 1 and i.y == snake.y:
            poss_dir["left"] = False
        if i.y == snake.y + 1 and i.x == snake.x:
            poss_dir["down"] = False
        if i.y == snake.y - 1 and i.x == snake.x:
            poss_dir["up"] = False

    if snake.x + 1 == bounds[0]:
        poss_dir["right"] = False
    if snake.x-1 == -1:
        poss_dir["left"] = False
    if snake.y+1 == bounds[1]:
        poss_dir["down"] = False
    if snake.y-1 == -1:
        poss_dir["up"] = False

    apple_dir = math.atan2(apple.x - snake.x, apple.y - snake.y) + math.pi

    state = State(-1,apple_dir, poss_dir)

    current_state = state
    if len(moves) > 50:
        #print(statelist, file=termdraw.f)
        moves[0].punish(custom_val=0.1)
        moves = moves[1:]

    best_state  = find_best_state(state, statelist)
    moves.append(Move(best_state, best_state.best_weight(poss_dir)[0]))
   # print(turns)
    if turns > 100:
        if len(snake.tail):
            [i.punish(custom_val=0.2) for i in moves]
        else:
            [i.reward(custom_val=len(snake.tail)/10-0.2) for i in moves]
        print("timeout", end=" ")
        
        #time.sleep(0.5)
        return ""
    return best_state.best_weight(poss_dir)[0]