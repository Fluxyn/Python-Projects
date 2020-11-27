#Importing modules and setting up the game
from turtle import *
from time import sleep
from random import random
import math
setup(420, 420, 370, 0)
title("The Quest")
player = Turtle()
player.goto(0, 0)
player.penup()

########
#PEOPLE#
########

#old man joe
joe = Turtle()
joe.hideturtle()
joe.penup()
joe.goto(28, 52)
joe.color("red")
joe.shape("circle")
#baby mike
mike = Turtle()
mike.hideturtle()
mike.penup()
mike.goto(-200, 100)
mike.color("white")
mike.shape("circle")
#sir keath of england
keath = Turtle()
keath.hideturtle()
keath.penup()
keath.goto(0, -100)
keath.color("gray")
keath.shape("circle")

##########
#GAMEPLAY#
##########

def play():
    player.clear()
    bgcolor('light green')
    player.color("blue")
    player.shape("turtle")
    #showing turtles
    player.showturtle()
    joe.showturtle()
    mike.showturtle()
    keath.showturtle()
    while True:
        key_move()
        
#Detecting colisions
def collided(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(), 2))
    if distance < 15:
        return True

def collision_check():
    if collided(player , joe):
        print("Old man Joe: Hey! Watch where yer' goin! When I was your age, you would be thrown in the dungeon for that!")
    if collided(player , mike):
        print("Baby Mike: BWAAAA!! I wat cookie!")      
    if collided(player , keath):
        print("Sir Keath of England: Good morrow kind fellow! Sir Keath of England at your service!")


#Adding keyed motion
def up():
    player.setheading(90)
    player.forward(50)
def down():
    player.setheading(270)
    player.forward(50)
def left():
    player.setheading(180)
    player.forward(50)
def right():
    player.setheading(0)
    player.forward(50)

def key_move():
    listen()
    onkey(up, 'Up')
    onkey(down, 'Down')
    onkey(left, 'Left')
    onkey(right, 'Right')
    mainloop()

###########
#MAIN_MENU#
###########

player.goto(-96, 15)
player.write("The Quest", font=("Arial", 35, "normal"))
player.goto(-120, -20)
player.write("To start, press the up arrow.", font=("Arial", 17, "normal")) 
player.goto(-160, -40)
player.write("To see the controls, press the down arrow", font=("Arial", 17, "normal")) 
player.hideturtle()
bgcolor("gray")
def print_controls():
    print("##########\n#CONTROLS#\n##########\nTo move, use the arrow keys. Note: to interacte with something, bump into it and exit!")

def menu_keys():
    listen()
    onkey(play, 'Up')
    onkey(print_controls, 'Down')
menu_keys()

collision_check()
mainloop()
