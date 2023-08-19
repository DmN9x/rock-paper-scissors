import numpy as np
import time
import sys
import os
import keyboard
import sys
import threading

assistantName = "Rupert"
osName = "RPS System"
RPS_CHOICES = ["Rock", "Paper", "Scissors"]
lastPlay = None
skipText = False

def main():
    
    '''This is where you start and finish your journey'''
    os.system('cls')
    threadSkipText = threading.Thread(target=skipTexts, daemon=True)
    threadSkipText.start()
    
    # Presenting Rupert! The assistant throughout the game
    printSlowly(
        assistantName + ": Hello! I'm " + assistantName + "! I'll be your assistant throughout this journey.\n"\
        "The game of Rock Paper Scissors can be tricky sometimes. That's why I'm here!\n"\
        "Let's start by getting your information. (press ENTER to continue)", True
        )
    
    # Getting all the info we need to get access to your twitter account and get access to your schedule (don't worry)
    playerInfos = getPlayerInformations()
    
    # Introducing the player to the game
    printSlowly(
        osName + ": Welcome, " + playerInfos['Name'] + ", and welcome to the Rock, Paper and Scissors game!\n"\
        "This game might sound easy, but it's not for amateurs.", True
        )
    
    # Explaining the rules of the game and how to play it
    printSlowly(
        assistantName + ": Alright buddy, don't let the game system scare you. It thinks it's better than everyone else...\n"\
        "Don't worry, the game is pretty intuitive!", True
        )
            
    # Loop if the player wants to play again
    while True:
        os.system("cls")
        # Asking how many rounds the player wants to play
        while True:
            printSlowly(osName + ": How many rounds do you want to play:\n")
            try:
                rounds = int(input())
            except ValueError:
                printSlowly("It has to be a natural number, baby. (ex: 3, 5, 7...)", True); continue
            if int(rounds) % 2 == 0: printSlowly(osName + ": It's gotta be an odd number, honey. (ex: 3, 5, 7...)", True); continue
            else: break
        
        # Calls the game function
        result = playGame(rounds)
        
        # Finishing the main function
        if result == 'Win':
            printSlowly(osName + ": Congratulations! You won the game! :)", True)
        else:
            printSlowly(osName + ": Unfortunately, you lost! I told you this would happen!\nDon't beat yourself up, try again later!", True)
            
        printSlowly(assistantName + ": This is the end of the game!\n")
        printSlowly("Thank you for playing!\n\n")
        printSlowly("Choose if you want to play again: (Y/N)\n")
        while True:
            playAgain = input().lower()
            if playAgain != "y" and playAgain != "n":
                printSlowly("Invalid answer, bitch", True)
            else: break
        if playAgain == "n": break
        
def skipTexts():
    
    '''This function is used to skip texts, it runs in a thread in the background'''
    
    global skipText
    while True:
        if keyboard.is_pressed('shift'):
            skipText = True
    
def getPlayerInformations():
    
    '''This function gets all the players informations and returns them'''
    
    # Setting the empty dictionary
    playerInfos = {}
    
    # Setting a few phrases of to spice things up!
    phrasesName = ["What an interesting name!", "That's a pretty name!", "Such an exquisite name!",
                   "I didn't even know that name existed!", "Really? Alright then..."]
    phrasesAge = ["Didn't know dinossaurs were still around...", "Jesus Christ must've been your friend, I imagine.",
                  "when's your back surgery scheduled to?", "pretty young to be playing with me, huh? That's okay, I'll take it easy :)",
                  "aww, you're still a baby!"]
    names = [
        "Luisa Bernard", "Jair Pope", "Aurelia Woods", "Zion Wallace", "Arianna Richmond", "Mordechai Mathews", "Sloan Mayer",
        "Yahir Krueger", "Kamari Rosales", "Wilder Rojas", "Adaline Fleming", "Fernando Atkinson", "Jazmin Beltran",
        "Ricky Gilmore", "Chanel Calderon"]
    
    # Asking for the player's name
    printSlowly(osName + ': What is your name?\n')
    playerInfos['Name'] = input()
    if playerInfos['Name'] != '':
        printSlowly(assistantName + ': ' + playerInfos['Name'] + ', huh? ' + np.random.choice(phrasesName), True)
    else:
        randomName = np.random.choice(names)
        printSlowly(
            assistantName + ': I see we have an anonymous around here.\n'\
            "Alright, I'll call you " + randomName, True)
        playerInfos['Name'] = randomName
    
    # Asking for the player's age
    printSlowly(osName + ": How old are you?\nIf you don't want to say it, just press ENTER\n")
    playerInfos['Age'] = input().strip()
    if playerInfos['Age'] == '' or playerInfos['Age'] != int:
        printSlowly(
            "Okay, I see you don't want to tell me your age.\n"\
            "That's okay. But you just lost some point with me...\n"\
            "Just kidding!\n"\
            "Or not...", True
            )
    elif int(playerInfos['Age']) <= 18:
        phrasesAge = [phrasesAge[index] for index in range(3, 5)]
        printSlowly(assistantName + ": " + playerInfos['Age'] + ", " + np.random.choice(phrasesAge), True)
    elif int(playerInfos['Age']) > 18 and int(playerInfos['Age']) <= 30:
        phrasesAge = phrasesAge[2]
        printSlowly(assistantName + ": "+ playerInfos['Age'] + ", " + phrasesAge, True)
    else:
        phrasesAge = [phrasesAge[index] for index in range(2)]
        printSlowly(assistantName + ": " + playerInfos['Age'] + ", " + np.random.choice(phrasesAge), True)
        
    # Returning the info
    
    printSlowly(assistantName + ": I think that's all the information I need to help you.\nLet's start!", True)
    
    return playerInfos

def printSlowly(string: str, clear = None):
    
    '''This function prints a string slowly'''
    
    global skipText
    
    for char in string:
        if skipText == False:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)
        else:
            os.system("cls")
            print(string); skipText = False
            break
    
    if clear == True:
        input() # This input is here so the text doesn't disappear instantly after it's printed
        os.system('cls')

def rpsSystem(difficulty, object, round):
    
    '''This is the brain of the game'''
    
    global lastPlay
    
    counterPlaysDict = {  # this dict stores all the counter plays, pretty simple actually
        1: 2, 2: 3, 3: 1
    }
    
    if difficulty == 'hard':  # 1 in 5 change to get predicted
        predictRange = [1, 6]
    elif difficulty == 'master':  # (1-3)
        predictRange = [1, 4]
    
    # If you're unlucky, you'll simply get counterplayed. But this only happens on lever hard and master
    if (difficulty == 'hard' or difficulty == 'master') and np.random.randint(predictRange[0], predictRange[1]) == np.random.randint(predictRange[0], predictRange[1]):
        counterPlay = counterPlaysDict[object]
    else:
        
        # On level easy, the first round is random, but the rest of them are always the counter play of your last choice
        if difficulty == 'easy':
            if round == 1:
                counterPlay = np.random.randint(1, 4)
                lastPlay = object  # stores the last play by the player to use in the next round
            else:
                counterPlay = counterPlaysDict[lastPlay]
                lastPlay = object  # stores the last play by the player to use in the next round
        
        # On medium, every 5 rounds you get the counter play of your last choice, but the rest is random
        elif difficulty == 'medium':
            if round % 5 == 0:
                counterPlay = counterPlaysDict[lastPlay]
            else:
                counterPlay = np.random.randint(1, 4)
                lastPlay = object  # stores the last play by the player to use in the next round
        
        # Here things start to get interesting, it'll be random every even round (and the first one as well), and counter for your last choice every odd round
        elif difficulty == 'hard':
            if round % 2 == 0 or round == 1:
                counterPlay = np.random.randint(1, 4)
                lastPlay = object  # stores the last play by the player to use in the next round
            else:
                counterPlay = counterPlaysDict[lastPlay]
                lastPlay = object  # stores the last play by the player to use in the next round
        
        # This is complete bullshit to be honest, I've never made more than 2 rounds myself, it's almost impossible to win
        # If you don't get straight up countered (33% chance every round), you still have 25% chance of getting a random play
        # But if you don't get lucky, you'll either lose or draw.
        # The logic behind this code doesn't let the machine lose. Good luck!
        elif difficulty == 'master':
            if np.random.randint(1, 5) == np.random.randint(1, 5):
                counterPlay = np.random.randint(1, 4)
            elif object == 1:
                counterPlay = np.random.randint(1, 3)
            elif object == 2:
                counterPlay = np.random.randint(2, 4)
            elif object == 3:
                while True:
                    counterPlay = np.random.randint(1, 4)
                    if counterPlay == 2: continue
                    break
            
    return counterPlay

def playGame(rounds):
    
    '''This is the function where you actualy play the game'''
    
    # Score of the player and the system
    playerScore = 0
    rpsScore = 0
    
    # Some useful dictionaries
    difficulties = {
        1: 'easy', 2: 'medium', 3: 'hard', 4: 'master'
    }
    
    plays = {
        1: 'rock', 2: 'paper', 3: 'scissors'
    }
    
    counters = {
        1: 2, 2: 3, 3: 1
    }
    
    while True:
        
        printSlowly("Select the difficulty you want to play\n1 - Easy\n2 - Medium\n3 - Hard\n")
        
        try:
            difficulty = int(input())
        except ValueError:
            printSlowly("It's gotta be a natural number, honey.", True); continue
            
        if difficulty not in [1, 2, 3, 4]:
            printSlowly("This difficulty does not exist, try again.", True); continue
        
        if difficulty == 4:
            os.system("cls")
            print("Select the difficulty you want to play\n1 - Easy\n2 - Medium\n3 - Hard")
            printSlowly("4 - Master\n"); time.sleep(1)
            if rounds <= 3:
                printSlowly("On Master level you can't play less than 5 rounds, dear.")
                roundsBefore = rounds; rounds += (5-rounds)
                printSlowly("\nRounds adjusted from " + str(roundsBefore) + " to 5.", True)
        
        difficulty = difficulties[difficulty]
        
        break
    
    os.system("cls")
    for round in range(1, rounds+1):
        
        while True:
            while True:
                print("1 - Rock | 2 - Paper | 3 - Scissors\n")
                print("Your score: " + str(playerScore))
                print("RPS System score: "+ str(rpsScore) + "\n")
                print(osName + ": round " + str(round) + "/" + str(rounds) + "\n")
                try:
                    userPlay = int(input("Your turn: "))
                    if userPlay < 1 or userPlay > 3:
                        printSlowly('The number has to be 1, 2 or 3, for fucks sake.', True); continue
                    printSlowly("You play: " + plays[userPlay])
                    break
                except ValueError:
                    printSlowly('You have to play a number, dumbass.', True); continue
                
            systemAnswer = rpsSystem(difficulty, userPlay, round)
            printSlowly("\nRPS System plays: " + plays[systemAnswer])
            if systemAnswer == counters[userPlay]:
                printSlowly("\nRound lost, try again.\n", True); rpsScore += 1
            elif userPlay == counters[systemAnswer]:
                printSlowly("\nRound won, nice job!\n", True); playerScore += 1
            else:
                printSlowly("\nDraw! This round didn't count. Let's try again.\n", True); continue
            break
        os.system("cls")
        if rounds == 1:
            if round == 1 and playerScore == 0:
                winLose = 'Lose'
            elif round == 1 and rpsScore == 0:
                winLose = 'Win'
        elif rounds > 1:
            if (rounds/2)+0.5 == playerScore:
                winLose = 'Win'; break
            elif (rounds/2)+0.5 == rpsScore:
                winLose = 'Lose'; break
        
    return winLose

if __name__ == '__main__':
    main()
