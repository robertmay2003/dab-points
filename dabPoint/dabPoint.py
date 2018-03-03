#!/usr/bin/env python
# -*- coding: utf-8 -*-


from random import *
from math import *
from time import *
from multiprocessing import Pool
import os



def move(board, dirr, xcoord, ycoord):
    if dirr=="a" and board[ycoord][xcoord-1] not in ["-","|"]:
        xcoord-=1
    elif dirr=="s" and board[ycoord+1][xcoord] not in ["-","|"]:
        ycoord+=1
    elif dirr=="d" and board[ycoord][xcoord+1] not in ["-","|"]:
        xcoord+=1
    elif dirr=="w" and board[ycoord-1][xcoord] not in ["-","|"]:
        ycoord-=1
    return xcoord, ycoord

def printScore(score, revives, infinOn):
    scoreStr = "| Dab Points: " + '\033[1;32m' + str(score) + '\033[0m' + " | "
    wraptop = "_" * (len(scoreStr) - len("\033[1;32m\033[0m"))
    wrapbottom = "~" * (len(scoreStr) - len("\033[1;32m\033[0m"))
    full = ""
    full += wraptop + "\n"
    full += scoreStr + ' \033[0;31m' + '◊'*revives + '\033[0m '
    if infinOn:
        full += '\033[1;34m∞\033[0m\n'
    else:
        full += "\n"
    full += wrapbottom + "\n"
    print full

def printboard(board, infinOn, moves, score, revives, nChar):
    justback='\033[0;'
    nc='\033[0m'
    red='\033[0;31;'
    redback='41m'
    lblue='\033[1;34;'
    lblueback='46m'
    yellow='\033[1;33;'
    brown='\033[0;33;'
    lgreen='\033[1;32;'
    greenback='42m'
    purple='\033[0;35;'
    yc = 0
    full = ""
    for y in board:
        xc = 0
        cuLine = ""
        for x in y:
            if [xc, yc] in moves:
                cuBack = lblueback
            else:
                cuBack = greenback
            if str(x).isdigit() or str(x)[1:].isdigit():
                if int(x) < 0:
                    cuLine += red + cuBack + str(x)[1:] + nc
                else:
                    cuLine += yellow + cuBack + str(x) + nc
            elif x == "∞":
                cuLine += lblue + cuBack + str(x) + nc
            elif x == "◊":
                cuLine += red + cuBack + str(x) + nc
            elif x == nChar:
                cuLine += red + cuBack + str(x) + nc
            elif x == "\"":
                cuLine += lgreen + cuBack + str(x) + nc
            elif x == "":
                cuLine += purple + cuBack + str(x) + nc
            elif x == "|" or x == "-":
                cuLine += brown + redback + str(x) + nc
            elif x == " ":
                cuLine += justback + cuBack + str(x) + nc
            else:
                cuLine += red + cuBack + str(x) + nc
            xc += 1
        full += cuLine + "\n"
        yc += 1
    print '\033c'
    print full
    printScore(score, revives, infinOn)

def printHelp():
    board=[["-"]*22,
    ["|"] + [" "]*5 + ["CONTROLS:"] + [" "]*6 + ["|"],
    ["|"] + [" "]*9 + ["^"] + [" "]*10 + ["|"],
    ["|"] + [" "]*9 + ["w"] + [" "]*10 + ["|"],
    ["|"] + [" "]*7 + ["<a"] + [" "] + ["d>"] + [" "]*8 + ["|"],
    ["|"] + [" "]*9 + ["d"] + [" "]*10 + ["|"],
    ["|"] + [" "]*9 + ["v"] + [" "]*10 + ["|"],
    ["|"] + [" "]*5 + ["POWER UPS:"] + [" "]*5 + ["|"],
    ["|"] + [" "]*2 + ["\033[0;35;42m\033[0m = High Points"] + [" "]*3 + ["|"],
    ["|"] + [" "]*5 + ["\033[0;31;42m◊\033[0m = Revive"] + [" "]*5 + ["|"],
    ["|"] + [" "]*3 + ["\033[1;34;42m∞\033[0m = Free Moves"] + [" "]*3 + ["|"],
    ["|"] + [" "]*2 + ["\033[1;31mAll red numbers\033[0m"] + [" "]*3 + ["|"],
    ["|"] + [" "]*3 + ["\033[1;31mare negative.\033[0m"] + [" "]*4 + ["|"],
    ["-"]*22]
    justback='\033[0;'
    nc='\033[0m'
    red='\033[0;31;'
    redback='41m'
    lblue='\033[1;34;'
    lblueback='46m'
    yellow='\033[1;33;'
    brown='\033[0;33;'
    lgreen='\033[1;32;'
    greenback='42m'
    purple='\033[0;35;'
    full = ""
    for y in board:
        cuLine = ""
        for x in y:
            cuBack = greenback
            if x == "|" or x == "-":
                cuLine += brown + redback + str(x) + nc
            elif x == " ":
                cuLine += justback + cuBack + str(x) + nc
            else:
                cuLine += red + cuBack + str(x) + nc
        full += cuLine + "\n"
    print '\033c'
    print full

def printMenu():
    board=[["-"]*22,
    ["|"] + [" "]*5 + ["DAB POINTS"] + [" "]*5 + ["|"],
    ["|"] + [" "]*20 + ["|"],
    #CUSTOM MESSAGE GOESHERE vvv (index 3)
    [],
    ["|"] + [" "]*20 + ["|"],
    ["|"] + [" "]*6 + ["PLAY [p]"] + [" "]*6 + ["|"],
    ["|"] + [" "]*6 + ["QUIT [q]"] + [" "]*6 + ["|"],
    ["|"] + [" "]*6 + ["HELP [h]"] + [" "]*6 + ["|"],
    ["|"] + [" "]*20 + ["|"],
    ["|"] + [" "]*5 + ["by Physch"] + [" "]*6 + ["|"],
    ["|"] + [" "]*20 + ["|"],
    ["-"]*22]
    messageNum = randint(0, 25)
    if messageNum == 0:
        board[3] = ["|"] + [" "]*2 + ["fuck off, johnny."] + [" "] + ["|"]
    elif messageNum == 1:
        board[3] = ["|"] + ["I honestly dont know"] + ["|"]
        board.insert(4, ["|"] + [" "]*2 + ["what you expected"] + [" "] + ["|"])
        board.insert(5, ["|"] + [" "]*6 + ["from me."] + [" "]*6 + ["|"])
    elif messageNum == 2:
        board[3] = ["|"] + [" "] + ["Gotta catch em all"] + [" "] + ["|"]
    elif messageNum == 3:
        board[3] = ["|"] + [" "]*3 + ["\"My name Jeff\""] + [" "]*3 + ["|"]
        board.insert(4, ["|"] + [" "]*10 + ["-Jeff"] + [" "]*5 + ["|"])
    elif messageNum == 4:
        board[3] = ["|"] + [" "]*7 + ["\"Hola\""] + [" "]*7 + ["|"]
        board.insert(4, ["|"] + [" "]*1 + ["-A Mexican probably"] + ["|"])
    elif messageNum == 5:
        board[3] = ["|"] + [" "] + ["this was a mistake"] + [" "] + ["|"]
    elif messageNum == 6:
        board[3] = ["|"] + [" "]*8 + ["yote"] + [" "]*8 + ["|"]
    elif messageNum == 7:
        board[3] = ["|"] + [" "]*3 + ["Holy sheep its"] + [" "]*3 + ["|"]
        board.insert(4, ["|"] + [" "]*6 + ["Notch!!!"] + [" "]*6 + ["|"])
    elif messageNum == 8:
        board[3] = ["|"] + [" "]*3 + ["Its not like I"] + [" "]*3 + ["|"]
        board.insert(4, ["|"] + [" "]*3 + ["l-l-like you or"] + [" "]*2 + ["|"])
        board.insert(5, ["|"] + [" "]*5 + ["anything!!"] + [" "]*5 + ["|"])
        board.insert(6, ["|"] + [" "]*20 + ["|"])
        board.insert(7, ["|"] + [" "]*6 + ["...baka"] + [" "]*7 + ["|"])
    elif messageNum == 9:
        board[3] = ["|"] + [" "]*3 + ["you're mom fat"] + [" "]*3 + ["|"]
    elif messageNum == 10:
        board[3] = ["|"] + [" "]*4 + ["The bees are"] + [" "]*4 + ["|"]
        board.insert(4, ["|"] + [" "]*4 + ["dying at an"] + [" "]*5 + ["|"])
        board.insert(5, ["|"] + [" "]*4 + ["alarming rate"] + [" "]*3 + ["|"])
    elif messageNum == 11:
        board[3] = ["|"] + [" "]*4 + ["damn daniel!"] + [" "]*4 + ["|"]
    elif messageNum == 12:
        board[3] = ["|"] + [" "]*3 + ["She say do you"] + [" "]*3 + ["|"]
        board.insert(4, ["|"] + [" "]*6 + ["love me"] + [" "]*7 + ["|"])
        board.insert(5, ["|"] + [" "]*2 + ["I tell her only"] + [" "]*3 + ["|"])
        board.insert(6, ["|"] + [" "]*7 + ["partly"] + [" "]*7 + ["|"])
        board.insert(7, ["|"] + [" "]*3 + ["I only love my"] + [" "]*3 + ["|"])
        board.insert(8, ["|"] + [" "]*3 + ["uncle Randy and"] + [" "]*2 + ["|"])
        board.insert(9, ["|"] + [" "]*1 + ["Sonic hentai, I'm"] + [" "]*2 + ["|"])
        board.insert(10, ["|"] + [" "]*7 + ["sorry"] + [" "]*8 + ["|"])
    elif messageNum == 13:
        board[3] = ["|"] + [" "]*4 + ["more pickle"] + [" "]*5 + ["|"]
    elif messageNum == 14:
        board[3] = ["|"] + [" "]*3 + ["pee pee poo poo"] + [" "]*2 + ["|"]
        board.insert(4, ["|"] + [" "]*4 + ["doo doo head"] + [" "]*4 + ["|"])
    elif messageNum == 15:
        board[3] = ["|"] + [" "]*3 + ["dont say n-word"] + [" "]*2 + ["|"]
        board.insert(4, ["|"] + [" "]*4 + ["its bad word"] + [" "]*4 + ["|"])
    elif messageNum == 16:
        board[3] = ["|"] + [" "]*3 + ["\033[0mjust monika"] + [" "]*2 + ["|"]
    elif messageNum == 17:
        board[3] = ["|"] + ["so there's this girl"] + ["|"]
        board.insert(4, ["|"] + [" "]*2 + ["she's so amazing"] + [" "]*2 + ["|"])
        board.insert(5, ["|"] + ["and here's the thing"] + ["|"])
        board.insert(6, ["|"] + [" "]*1 + ["SHES READING THIS"] + [" "]*2 + ["|"])
        board.insert(7, ["|"] + [" "]*5 + ["RIGHT NOW"] + [" "]*6 + ["|"])
    elif messageNum == 18:
        board[3] = ["|"] + [" "]*8 + ["dab"] + [" "]*9 + ["|"]
    elif messageNum == 19:
        board[3] = ["|"] + [" "]*5 + ["spiritual"] + [" "]*6 + ["|"]
        board.insert(4, ["|"] + [" "]*3 + ["predecessor to"] + [" "]*3 + ["|"])
        board.insert(5, ["|"] + ["DaBall, coming soon"] + [" "] + ["|"])
    elif messageNum == 20:
        board[3] = ["|"] + [" "]*3 + ["im running out"] + [" "]*3 + ["|"]
        board.insert(4, ["|"] + [" "]*4 + ["of ideas for"] + [" "]*4 + ["|"])
        board.insert(5, ["|"] + [" "]*8 + ["this"] + [" "]*8 + ["|"])
    elif messageNum == 21:
        board[3] = ["|"] + [" "]*3 + ["you know i had"] + [" "]*3 + ["|"]
        board.insert(4, ["|"] + [" "]*3 + ["to do it to em"] + [" "]*3 + ["|"])
    elif messageNum == 22:
        board[3] = ["|"] + [" "]*3 + ["oh god, oh fuh"] + [" "]*3 + ["|"]
    elif messageNum == 23:
        board[3] = ["|"] + [" "]*3 + ["toast backwards"] + [" "]*2 + ["|"]
        board.insert(4, ["|"] + [" "]*3 + ["is still toast."] + [" "]*2 + ["|"])
    elif messageNum == 24:
        board[3] = ["|"] + [" "]*2 + ["he did the bash-"] + [" "]*2 + ["|"]
        board.insert(4, ["|"] + [" "]*2 + ["he did the game"] + [" "]*3 + ["|"])
        board.insert(5, ["|"] + [" "]*5 + ["for bash!"] + [" "]*6 + ["|"])
        board.insert(6, ["|"] + [" "]*2 + ["he did the bash-"] + [" "]*2 + ["|"])
        board.insert(7, ["|"] + [" "]*2 + ["it was mediocre."] + [" "]*2 + ["|"])
    elif messageNum == 25:
        board[3] = ["|"] + [" "]*3 + ["swagger-filled!"] + [" "]*2 + ["|"]
    justback='\033[0;'
    nc='\033[0m'
    red='\033[0;31;'
    redback='41m'
    lblue='\033[1;34;'
    lblueback='46m'
    yellow='\033[1;33;'
    brown='\033[0;33;'
    lgreen='\033[1;32;'
    greenback='42m'
    purple='\033[0;35;'
    full = ""
    for y in board:
        cuLine = ""
        for x in y:
            cuBack = greenback
            if x == "|" or x == "-":
                cuLine += brown + redback + str(x) + nc
            elif x == " ":
                cuLine += justback + cuBack + str(x) + nc
            else:
                cuLine += red + cuBack + str(x) + nc
        full += cuLine + "\n"
    print '\033c'
    print full

def printGameOver(score, high):
    board=[["-"]*22,
    ["|"] + [" "]*20 + ["|"],
    ["|"] + [" "]*20 + ["|"],
    ["|"] + [" "]*5 + ["GAME OVER!"] + [" "]*5 + ["|"],
    ["|"] + [" "]*20 + ["|"],
    ["|"] + [" "]*5 + ["your score"] + [" "]*5 + ["|"],
    ["|"] + [" "]*5 + [" "]*(9 - len(str(score))) + [str(score)] + [" "]*5 + [" "] + ["|"],
    ["|"] + [" "]*20 + ["|"],
    ["|"] + [" "]*5 + ["high score"] + [" "]*5 + ["|"],
    ["|"] + [" "]*5 + [" "]*(9 - len(str(high))) + [str(high)] + [" "]*5 + [" "] + ["|"],
    ["|"] + [" "]*20 + ["|"],
    ["-"]*22]
    justback='\033[0;'
    nc='\033[0m'
    red='\033[0;31;'
    redback='41m'
    lblue='\033[1;34;'
    lblueback='46m'
    yellow='\033[1;33;'
    brown='\033[0;33;'
    lgreen='\033[1;32;'
    greenback='42m'
    purple='\033[0;35;'
    full = ""
    for y in board:
        cuLine = ""
        for x in y:
            cuBack = greenback
            if str(x).isdigit():
                cuLine += yellow + cuBack + str(x) + nc
            elif x == "∞":
                cuLine += lblue + cuBack + str(x) + nc
            elif x == "◊":
                cuLine += red + cuBack + str(x) + nc
            elif x == "\"":
                cuLine += lgreen + cuBack + str(x) + nc
            elif x == "":
                cuLine += purple + cuBack + str(x) + nc
            elif x == "|" or x == "-":
                cuLine += brown + redback + str(x) + nc
            elif x == " ":
                cuLine += justback + cuBack + str(x) + nc
            else:
                cuLine += red + cuBack + str(x) + nc
        full += cuLine + "\n"
    print '\033c'
    print full

def enterHigh(plscore):
    leaderboard = [line.rstrip('\n') for line in open('leaderboard.txt')]
    scores = []
    for entry in leaderboard:
        score = int(entry.split(";")[1])
        scores.append(score)
    index = 0
    scores.append(0)
    scores = scores[0:11]
    scores.sort()
    scores.reverse()
    leaderboard.append("placeholder;0")
    leaderboard = leaderboard[:11]
    while index < 11:
        score = scores[index]
        if score < plscore:
            print "You got a high score!"
            os.spawnlp(os.P_NOWAIT, "/usr/bin/afplay", "afplay", './audio/sfx/game/damn.mp3')
            sleep(2)
            name = raw_input("Enter your name: ")
            leaderboard.insert(index, "%s;%s" % (name, plscore))
            if leaderboard[-1] == "placeholder;0":
                leaderboard.pop()
            print "LEADERBOARD: "
            for entry in leaderboard:
                print entry.split(';')[0] + ": " + entry.split(';')[1]
            ld = open('leaderboard.txt', 'w')
            ind = 0
            for entry in leaderboard[:10]:
                if ind == 0:
                    ld.write(entry)
                else:
                    ld.write("\n" + entry)
                ind += 1
            ld.close()
            index = 11
        index += 1


def play():
    playing = 'y'
    nChar = (raw_input("Enter your name: ")+ "Y")[0].upper()
    click = os.spawnlp(os.P_NOWAIT, "/usr/bin/afplay", "afplay", "./audio/sfx/menu/click.mp3")
    while playing != "n":
        board=[["-"]*22,
        ["|"] + [" "]*20 + ["|"],
        ["|"] + [" "]*20 + ["|"],
        ["|"] + [" "]*20 + ["|"],
        ["|"] + [" "]*20 + ["|"],
        ["|"] + [" "]*20 + ["|"],
        ["|"] + [" "]*20 + ["|"],
        ["|"] + [" "]*20 + ["|"],
        ["|"] + [" "]*20 + ["|"],
        ["|"] + [" "]*20 + ["|"],
        ["|"] + [" "]*20 + ["|"],
        ["-"]*22]
        dabPoints = 10
        score = 0
        dabsPlaced = 0
        specPlaced = 0
        dabsCollected = True
        gameOver = False
        xcoord = 5
        ycoord = 5
        grassPlaced = 0
        while grassPlaced < randint(5, 50):
            grassx = randint(1, 21)
            grassy = randint(1, 11)
            if board[grassy][grassx] == " ":
                grassPlaced +=1
                board[grassy][grassx] = "\""
        defaultBoard = [row[:] for row in board]
        moves = []
        infinOn = False
        dabsDurInf=0
        revives = 0
        board[ycoord][xcoord] = nChar
        gameSong = os.spawnvp(os.P_NOWAIT, "afplay", ["afplay", "--volume", "0.2", "./audio/game/%s"%(choice([x for x in os.listdir("./audio/game/")]))])
        while not gameOver:
            dabsPlaced = 0
            lowerR = 3-(dabPoints/15)
            upperR = 6-(dabPoints/15)
            if lowerR < 0:
                lowerR = 0
            if upperR < 2:
                upperR = 2
            dabsRequired = randint(int(lowerR), int(upperR))
            if dabsCollected:
                board = [row[:] for row in defaultBoard]
            while dabsCollected and dabsPlaced < dabsRequired:
                board[ycoord][xcoord] = nChar
                dabx = randint(1, 21)
                daby = randint(1, 11)
                lowerV = 3-(dabPoints/4)
                upperV = 14-(dabPoints/4)
                if lowerV < -9:
                    lowerV = -9
                if upperV < 0:
                    upperV = 0
                dabval = randint(int(lowerV), int(upperV-specPlaced))
                if board[daby][dabx] in [" ", "\""]:
                    if dabval < 10:
                        board[daby][dabx] = dabval
                        dabsPlaced +=1
                    else:
                        specVal = randint(1, 8)
                        if specVal in [1, 2, 3, 4, 5]:
                            board[daby][dabx] = ""
                            specPlaced += 1
                            dabsPlaced +=1
                        elif specVal in [6, 7]:
                            board[daby][dabx] = "◊"
                            specPlaced += 2
                            dabsPlaced +=1
                        elif specVal == 8:
                            board[daby][dabx] = "∞"
                            specPlaced += 3
                            dabsPlaced +=1

            dabsCollected = False
            printboard(board, infinOn, moves, dabPoints, revives, nChar)
            nextx, nexty = move(board, (raw_input("(W, A, S, D):").lower()+";")[0], xcoord, ycoord)
            dabsCollected = True
            board[ycoord][xcoord] = defaultBoard[ycoord][xcoord]
            if str(board[nexty][nextx]).isdigit() or str(board[nexty][nextx])[1:].isdigit():
                dabPoints += board[nexty][nextx]
                score += ((dabPoints)/2) * int(board[nexty][nextx])
                xcoord, ycoord = nextx, nexty
                dabsCollected = True
                dabsPlaced = 0
                specPlaced = 0
                dabsDurInf += 1
                if board[nexty][nextx] > 0:
                    up = os.spawnlp(os.P_NOWAIT, "/usr/bin/afplay", "afplay", "./audio/sfx/game/up.mp3")
                else:
                    down = os.spawnlp(os.P_NOWAIT, "/usr/bin/afplay", "afplay", "./audio/sfx/game/down.mp3")
            elif board[nexty][nextx] == "":
                dabPoints += randint(10, 15)
                score += 90
                xcoord, ycoord = nextx, nexty
                dabsCollected = True
                dabsPlaced = 0
                specPlaced = 0
                dabsDurInf += 1
                apple = os.spawnvp(os.P_NOWAIT, "afplay", ["afplay", "--volume", "7", "./audio/sfx/game/apple.mp3"])
            elif board[nexty][nextx] == "◊":
                revives += 1
                score += 100
                xcoord, ycoord = nextx, nexty
                dabsCollected = True
                dabsPlaced = 0
                specPlaced = 0
                dabsDurInf += 1
                gem = os.spawnlp(os.P_NOWAIT, "/usr/bin/afplay", "afplay", "./audio/sfx/game/gem.mp3")
            elif board[nexty][nextx] == "∞":
                infinOn = True
                score += 200
                xcoord, ycoord = nextx, nexty
                dabsCollected = True
                dabsPlaced = 0
                specPlaced = 0
                dabsDurInf = 0
                infin = os.spawnlp(os.P_NOWAIT, "/usr/bin/afplay", "afplay", "./audio/sfx/game/infin.mp3")
            else:
                walk = os.spawnlp(os.P_NOWAIT, "/usr/bin/afplay", "afplay", "./audio/sfx/walk/%s"%(choice([x for x in os.listdir("./audio/sfx/walk/")])))
                score += 10
                dabsCollected = False
                xcoord, ycoord = nextx, nexty
            board[ycoord][xcoord] = nChar
            moves.append([xcoord, ycoord])
            if len(moves) > 3:
                del moves[0]
            if dabsDurInf > 2:
                if infinOn:
                    infinOff = os.spawnlp(os.P_NOWAIT, "/usr/bin/afplay", "afplay", "./audio/sfx/game/infinOff.mp3")
                infinOn=False
            if not infinOn:
                dabPoints-=1
            if dabPoints <= 0:
                if revives > 0:
                    revives -= 1
                    dabPoints = 10
                    revive = os.spawnlp(os.P_NOWAIT, "/usr/bin/afplay", "afplay", "./audio/sfx/game/revive.mp3")
                else:
                    gameOver = True
        leaderboard = [line.rstrip('\n') for line in open('leaderboard.txt')]
        scores = [0]
        for entry in leaderboard:
            enscore = int(entry.split(";")[1])
            scores.append(enscore)
        os.system("kill %s;kill \"$(cat /tmp/cu-song.pid)\"" % (gameSong))
        printGameOver(int(score), scores[0])
        os.spawnlp(os.P_NOWAIT, "/usr/bin/afplay", "afplay", "./audio/sfx/death/%s"%(choice([x for x in os.listdir("./audio/sfx/death/")])))
        sleep(2)
        enterHigh(int(score))
        revive = os.spawnlp(os.P_NOWAIT, "/usr/bin/afplay", "afplay", "./audio/sfx/game/damn.mp3")
        playing = (raw_input("One more round? [y/n]: ").lower()+";")[0]

def main():
    menu = os.spawnlp(os.P_NOWAIT, "./audioPlayer.sh", "afplay", "./audio/menu/%s"%(choice([x for x in os.listdir("./audio/menu/")])))
    home = True
    while home:
        printMenu()
        action = (raw_input("[ p / h / q ] ") + ";")[0].lower()
        click = os.spawnlp(os.P_NOWAIT, "/usr/bin/afplay", "afplay", "./audio/sfx/menu/click.mp3")
        if action == 'h':
            printHelp()
            raw_input("Press any key to return.")
            click = os.spawnlp(os.P_NOWAIT, "/usr/bin/afplay", "afplay", "./audio/sfx/menu/click.mp3")
        elif action == 'p':
            os.system("kill %s;kill \"$(cat /tmp/cu-song.pid)\"" % (menu))
            play()
            menu = os.spawnlp(os.P_NOWAIT, "./audioPlayer.sh", "afplay", "./audio/menu/%s"%(choice([x for x in os.listdir("./audio/menu/")])))
            click = os.spawnlp(os.P_NOWAIT, "/usr/bin/afplay", "afplay", "./audio/sfx/menu/click.mp3")
        elif action == 'q':
            os.system("kill %s;kill \"$(cat /tmp/cu-song.pid)\"" % (menu))
            print "Thank you for playing!"
            home = False

main()
