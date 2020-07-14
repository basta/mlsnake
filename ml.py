import typing
import random
import math
from classes import *

statesave_filename = "state.txt"

o = open("out.log", "a+")

current_state = None

class Move:
    def __init__(self, state, dir):
        self.dir = dir
        self.state: State = state

    def reward(self):
        # Here, modify the reward mechanism
        self.state.dir_weights[self.dir] += 0.2

    def punish(self, custom_val=0.1):
        if self.state.dir_weights[self.dir] > 0:
            self.state.dir_weights[self.dir] -= random.uniform(0, custom_val * 2)
            for i in self.state.dir_weights:
                if i != self.dir:
                    self.state.dir_weights[i] += random.uniform(0, custom_val)


class State:
    def __init__(self, id, apple_dir, poss_dir, dir_weights = None):
        self.id = id
        self.apple_dir : float = apple_dir
        self.poss_dir : dict = poss_dir
        
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
        coeff += self.similiarity_to(other) * 2 #Here, maybe increase the weight of similiarity
        coeff += other.best_weight()[1] * 1 #Here, maybe modify the weight of state's weight

        if (other.best_weight()[0]) == "":
            #termdraw.f.write(str(other.dir_weights))
            pass

        #print("dir weights: ", self.dir_weights,other.dir_weights, file=o)
        for i in self.poss_dir:
            if self.poss_dir[i] != other.poss_dir[i]:
                #print("returned-1", self, other, file=o)
                return -1
        
        return coeff

    def best_weight(self):
        best_weight = -1
        best_dir = ""

        for i in self.dir_weights:
            if self.dir_weights[i] > best_weight and self.poss_dir[i]:
                best_weight = self.dir_weights[i]
                best_dir = i 
        return [best_dir, best_weight]
    
    def __str__(self):
        return str(self.apple_dir) + str(self.dir_weights) + str(self.poss_dir)

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
        for i, state in enumerate(self.states):
            state.id = i
            o.write(str(state.id) + " " + str(state.apple_dir) + " ")
            for ii in ["up", "left", "right", "down"]:
                if state.poss_dir[ii]:
                    o.write("1 ")
                else:
                    o.write("0 ")
            for ii in ["up", "left", "right", "down"]:
                o.write(str(state.dir_weights[ii]))
            o.write("\n")
    
    def __iter__(self):
        return iter(self.states)
    

    def __str__(self):
        return str([str(i)+"\n" for i in self.states])


statelist = StateList()
moves : typing.List[Move] = []

def find_best_state(state: State, statearr: StateList):
    best_coeff = -1
    best_other = None
    for other_state in statearr.states:
        if state.coeff_with(other_state) > best_coeff:
            best_other = other_state
            best_coeff = state.coeff_with(other_state)
    
    if best_coeff >= 1.9: #Here, maybe modify the value to use existing state
        #print("Used existing state with coeff ", best_coeff, file=o)
        return best_other

    else:
        #print("Used new state because of coeff", best_coeff, file = o)
        statearr.states.append(state)
        return state

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

    if (snake.x == apple.x and snake.y == apple.y):
        [i.reward() for i in moves[-100:]] #Here, modify the amount of rewarded moves
        moves = []
        o.writelines(["jablko snězeno"])
        turns = 0
    apple_dir = math.atan2(apple.x - snake.x, apple.y - snake.y) + math.pi

    state = State(-1,apple_dir, poss_dir)
    #print("1own_state: ", state, file=o)
    current_state = state
    if len(moves) > 100:
        #print(statelist, file=termdraw.f)
        moves[0].punish(custom_val=0.01)
        moves = moves[1:]

    best_state  = find_best_state(state, statelist)
    #print("2beststate: ", best_state, file=o)
    moves.append(Move(best_state, best_state.best_weight()[0]))
    #o.write(str(turns) + " \n")
    #o.write("Pocet stateu: " + str(len(statelist.states)) + "\n")

    if turns > 2000:
        [i.punish(custom_val=0.01) for i in moves]
        return ""
    return best_state.best_weight()[0]