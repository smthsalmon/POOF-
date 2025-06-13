from turtle import*
import turtle
import random
import keyboard
from pynput import mouse
import time
import math
from collections import Counter

def grid():
    lineh = -300
    lined = -300
    turtle.penup()
    turtle.setpos(-300,300)
    turtle.pendown()
    for i in range(4):
        forward(600)
        right(90)
    for i in range(5):
        lineh += 100
        turtle.penup()
        turtle.setpos(-300,lineh)
        turtle.setheading(0)
        turtle.pendown()
        forward(600)

        lined += 100
        turtle.penup()
        turtle.setpos(lined,-300)
        turtle.setheading(90)
        turtle.pendown()
        forward(600)
    for i in range (6):
        turtle.penup()
        turtle.setpos(100 * i - 250, 325)
        turtle.pendown()
        turtle.write(i,align = "center",font = ("Georgia",20,"normal"))
    for i in range(6):
        turtle.penup()
        turtle.setpos(-334.5, -100 * i + 234.5)
        turtle.pendown()
        turtle.write(i, align="center", font=("Georgia", 20, "normal"))

def is_valid(x, y, board, visited, player):
    return 0 <= x < len(board) and 0 <= y < len(board[0]) and not visited[x][y] and board[x][y] == player


def is_empty(x, y, board):
    # if at edge, return FALSE (because not a liberty/empty space)
    return 0 <= x < len(board) and 0 <= y < len(board[0]) and board[x][y] == 0


# Find clusters Search
def adjacentsearch(x, y, board, visited, cluster):
    piece = board[x, y]

    cluster.append([x, y])
    visited[x][y] = True

    # look in 4 directions for similar adjacent pieces
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    for dx, dy in directions:

        nx, ny = x + dx, y + dy

        # check if not at edge, and "valid" matching player piece
        if is_valid(nx, ny, board, visited, piece):
            # find next adjacent pieces that match current piece
            adjacentsearch(nx, ny, board, visited, cluster)


#
def find_clusters(board):
    clusters = {"p": [], "c": []}

    visited = [[False] * len(board[0]) for k in range(len(board))]

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != 0 and not visited[i][j]:
                player = board[i][j]
                cluster = []
                adjacentsearch(i, j, board, visited, cluster)
                clusters[player].append(cluster)
    return clusters


# Depth First Search
def dfs(x, y, board, visited, player, group):
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    visited[x][y] = True
    group.append([x, y])
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, board, visited, player):
            dfs(nx, ny, board, visited, player, group)


#
def find_groups(board):
    groups = {"p": [], "c": [], "libp": [[]], "libc": [[]]}

    groups["libp"] = [False for k in range(36)]
    groups["libc"] = [False for k in range(36)]

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != 0:
                skiplocation = False
                player = board[i][j]

                # checks if this location has already been found in a previous group
                for checkgroup in groups[player]:

                    if [i, j] in checkgroup:
                        skiplocation = True
                        break

                # if not found in previous groups, find new group
                if not skiplocation:
                    group = []
                    visited = [[False] * len(board[0]) for k in range(len(board))]

                    # depth scan for cluster
                    dfs(i, j, board, visited, player, group)

                    # add newly found cluster to GROUPS
                    groups[player].append(group)

                    group_index = groups[player].index(group)

                    # check every point in cluster for adjacent locations that are liberties (empty spaces)
                    for [x, y] in group:

                        liberty_exists = False

                        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
                        for dx, dy in directions:
                            nx, ny = x + dx, y + dy
                            if is_empty(nx, ny, board):
                                print("lib" + player)
                                print("====================")
                                liberty_exists = True
                                groups["lib" + player][group_index] = True

                            if liberty_exists:
                                print(groups["lib" + player])

                                #break

    return groups


# finds empty spaces on the board
def find_liberties(groups, board, liberties):
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    for player in ["p","c"]:
    #for player, group_list in groups.items():
        for group in groups[player]:
        #for group in group_list:
            for coord in group:
                # ERROR HERE: GROUPS IS NO LONGER A DICTIONARY, IT NOW HAS 3 DIMENSIONS
                if len(coord) == 2:
                    x, y = coord
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy

                        # Check nx ny are in BOUNDS of board && empty space (a liberty)
                        if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == 0:
                            liberties[player].append((nx, ny))
    return liberties


def start():
    for i,j,y in [["POOF!",100,0],["EASY",40,-50],["MEDIUM",40,-150],["HARD",40,-250]]:
        turtle.penup()
        turtle.goto(0,y)
        turtle.pendown()
        turtle.write(i,align="center",font=("Georgia",j,"normal"))

def check_capture(x, y, board, groups):
    # determine which player's piece X,Y is
    player = board[x][y]
    opponent = "c" if player == "p" else "p"

    # look for adjacent enemy clusters (lrud)
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(board) and 0 <= ny < len(board[0]):

            # check each group cluster to see if NX,NY is in that cluster
            for checkopponentgroup in groups[opponent]:

                if [nx, ny] in checkopponentgroup:

                    index = groups[opponent].index(checkopponentgroup)

                    # if enemy cluster has no liberties (not implemented), then CAPTURE/FLIP pieces
                    if groups["lib" + opponent][index] == False:

                        print("CAPTURE FOUND", [nx, ny])
                        turtle.penup()
                        turtle.goto(0,350)
                        turtle.write("POOF!",align = "center",font = ("Georgia",40,"normal"))

                        # if everything is filled up or at an edge
                        for flipx, flipy in checkopponentgroup:
                            board[flipx][flipy] = player
                    else:
                        print("Liberties FOUND for ", player, [nx, ny], )

def drawpiece(x,y):
    turtle.penup()
    turtle.setpos(100 * x - 275, -100 * y + 275)
    turtle.setheading(0)
    for k in range(4):
        turtle.pendown()
        forward(50)
        right(90)

def weiqi():
    turtle.hideturtle()
    turtle.tracer(5)
    selectscreen = True
    yselector = 2
    turtle.penup()
    turtle.setpos(-200,yselector*100-180)
    turtle.setheading(0)
    for k in range(2):
        turtle.pendown()
        forward(400)
        right(90)
        forward(70)
        right(90)
    while selectscreen == True:
        start()
        if keyboard.is_pressed("s"):
            yselector = yselector -1
            if yselector < 0:
                yselector = 2
            turtle.clear()
            turtle.penup()
            turtle.setpos(-200, yselector * 100 - 180)
            turtle.setheading(0)
            for k in range(2):
                turtle.pendown()
                forward(400)
                right(90)
                forward(70)
                right(90)
            start()
            time.sleep(0.08)
        if keyboard.is_pressed("w"):
            yselector = yselector +1
            if yselector > 2:
                yselector = 0
            turtle.clear()
            turtle.penup()
            turtle.setpos(-200, yselector * 100 - 180)
            turtle.setheading(0)
            for k in range(2):
                turtle.pendown()
                forward(400)
                right(90)
                forward(70)
                right(90)
            start()
            time.sleep(0.08)
        if keyboard.is_pressed("Enter"):
            turtle.clear()
            selectscreen = False
        if yselector == 2:
            difficulty = "EASY"
        if yselector == 1:
            difficulty = "MEDIUM"
        if yselector == 0:
            difficulty = "HARD"
        time.sleep(0.08)
    grid()
    x1 = 0
    y1 = 0
    board = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]
    limit1 = 0
    limit2 = 5
    visited = [[False] * len(board[0]) for k in range(len(board))]
    group = []
    #captured_coords = {"p": [], "c": []}
    liberties = {"p": [], "c": []}
    #group_liberties = []
    game = True
    while game:
        #print(board)
        invalidmove = False
        drawpiece(x1,y1)
        right(45)
        forward(math.sqrt(5000))
        left(135)
        forward(50)
        left(135)
        forward(math.sqrt(5000))
        right(135)
        forward(50)
        turtle.setheading(0)

        turtle.penup()
        turtle.goto(0,-375)
        turtle.pendown()
        turtle.write(f"CURSOR AT ({x1},{y1})",align = "center",font = ("Georgia",40,"normal"))

        if not 0 in board[0] and not 0 in board[1] and not 0 in board[2] and not 0 in board[3] and not 0 in board[4] and not 0 in board[5]:
            game = False

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == "p":
                    turtle.penup()
                    turtle.setpos(100 * i - 275, -100 * j + 275)
                    turtle.setheading(0)
                    turtle.begin_fill()
                    for k in range(4):
                        turtle.pendown()
                        forward(50)
                        right(90)
                    turtle.end_fill()
                if board[i][j] == "c":
                    drawpiece(i,j)

        if keyboard.is_pressed("d"):
            turtle.clear()
            grid()
            x1 = x1 + 1
            if x1 > limit2:
                x1 = limit1

        if keyboard.is_pressed("a"):
            turtle.clear()
            grid()
            x1 = x1 - 1
            if x1 < limit1:
                x1 = limit2

        if keyboard.is_pressed("w"):
            turtle.clear()
            grid()
            y1 = y1 - 1
            if y1 < limit1:
                y1 = limit2

        if keyboard.is_pressed("s"):
            turtle.clear()
            grid()
            y1 = y1 + 1
            if y1 > limit2:
                y1 = limit1


        if keyboard.is_pressed("Enter"):
            if board[x1][y1] != 0:
                turtle.penup()
                turtle.goto(0,325)
                turtle.pendown()
                turtle.write("INVALID MOVE!",align="center",font=("Georgia",40,"normal"))
                invalidmove = True

            else:
                board[x1][y1] = "p"

            groups = find_groups(board)

            #POSSIBLE ERROR?
            check_capture(x1, y1, board, groups)
            time.sleep(0.08)

            if not invalidmove:

                xcpu = random.randint(0, 5)
                ycpu = random.randint(0, 5)

                #EASY CPU
                if difficulty == "EASY":
                    while board[xcpu][ycpu] != 0:
                        xcpu = random.randint(0, 5)
                        ycpu = random.randint(0, 5)

                    drawpiece(xcpu, ycpu)
                    board[xcpu][ycpu] = "c"
                #MEDIUM CPU
                elif difficulty == "MEDIUM":
                    for player in ["p", "c"]:
                        liberties = {"p":[],"c":[]}
                        find_liberties(groups, board, liberties)
                    #print(liberties["p"])
                    if random.randint(0, 1) == 0:
                        if liberties["p"]:
                            lib_rrow = random.randint(0, (len(liberties["p"]) - 1))
                            xcpu = liberties["p"][lib_rrow][0]
                            ycpu = liberties["p"][lib_rrow][1]
                            while board[xcpu][ycpu] != 0:
                                lib_rrow = random.randint(0, len(liberties["p"]) - 1)
                            drawpiece(xcpu, ycpu)
                            board[xcpu][ycpu] = "c"
                        else:
                            while board[xcpu][ycpu] != 0:
                                xcpu = random.randint(0, 5)
                                ycpu = random.randint(0, 5)
                            drawpiece(xcpu, ycpu)
                            board[xcpu][ycpu] = "c"
                    else:
                        while board[xcpu][ycpu] != 0:
                            xcpu = random.randint(0, 5)
                            ycpu = random.randint(0, 5)
                        drawpiece(xcpu, ycpu)
                        board[xcpu][ycpu] = "c"
                #HARD CPU
                elif difficulty == "HARD":
                    for player in ["p", "c"]:
                        liberties = {"p": [], "c": []}
                        find_liberties(groups, board, liberties)
                    if liberties["p"]:
                        lib_rrow = random.randint(0, (len(liberties["p"]) - 1))
                        xcpu = liberties["p"][lib_rrow][0]
                        ycpu = liberties["p"][lib_rrow][1]
                        while board[xcpu][ycpu] != 0:
                            lib_rrow = random.randint(0, len(liberties["p"]) - 1)
                        drawpiece(xcpu, ycpu)

                        board[xcpu][ycpu] = "c"
                    else:
                        while board[xcpu][ycpu] != 0:
                            xcpu = random.randint(0, 5)
                            ycpu = random.randint(0, 5)
                        drawpiece(xcpu, ycpu)
                        board[xcpu][ycpu] = "c"

                groups = find_groups(board)
                check_capture(xcpu, ycpu, board, groups)


        time.sleep(0.08)

    turtle.clear()
    while not game:
        turtle.penup()
        turtle.goto(0,50)
        turtle.pendown()
        turtle.write("GAME OVER!",align = "center", font = ("Georgia",60,"normal"))
        turtle.penup()
        turtle.goto(0,-50)
        turtle.pendown()
        endpieces = {"p": [], "c": []}
        for i in range (5):
            rowendpieces = Counter(board[i])
            endpieces["p"].append(rowendpieces["p"])
            endpieces["c"].append(rowendpieces["c"])
        if endpieces["c"] > endpieces["p"]:
            turtle.write("WHITE WINS",align = "center", font = ("Georgia",40,"normal"))
        elif endpieces["p"] > endpieces["c"]:
            turtle.write("BLACK WINS", align="center", font=("Georgia", 40, "normal"))
        elif endpieces["c"] == endpieces["p"]:
            turtle.write("IT'S A TIE!", align = "center", font = ("Georgia",40,"normal"))


    pass

weiqi()