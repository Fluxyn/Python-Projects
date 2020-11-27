import matplotlib.pyplot as plt
import turtle, time, threading, sys, os
from tkinter import ttk
from tkinter import *
from random import randint

def startup_simulation(nfoxes, nrabbits):
        global startbutton
        global grass
        global foxes
        global rabbits
        global printcheck_val
        if printcheck_val.get() == 1:
                sys.stdout = open(os.devnull, 'w')
        setupbutton.destroy()
        frame2.destroy()
        frame3.destroy()
        startbutton = ttk.Button(main, text='Start simulation', command=run_simulation)
        startbutton.pack()
        wn.colormode(255)
        wn.bgcolor(0,100,0)
        grass = 100
        foxes = []
        rabbits = []
        wn.tracer(0)
        for i in range(int(nfoxes)):
                globals()['fox' + str(i)] = {'turt': turtle.Turtle(), 'speed': 12, 'energy': 50}
                globals()['fox' + str(i)]['turt'].color('orange')
                globals()['fox' + str(i)]['turt'].penup()
                globals()['fox' + str(i)]['turt'].speed(0)
                globals()['fox' + str(i)]['turt'].goto(randint(-400,400),randint(-400,400))
                globals()['fox' + str(i)]['turt'].speed(globals()['fox' + str(i)]['speed']/2)
                foxes.append(globals()['fox' + str(i)])
        for i in range(int(nrabbits)):
                globals()['rabbit' + str(i)] = {'turt': turtle.Turtle(), 'speed': 5, 'energy': 20}
                globals()['rabbit' + str(i)]['turt'].color('lightgray')
                globals()['rabbit' + str(i)]['turt'].penup()
                globals()['rabbit' + str(i)]['turt'].speed(0)
                globals()['rabbit' + str(i)]['turt'].goto(randint(-400,400),randint(-400,400))
                globals()['rabbit' + str(i)]['turt'].speed(globals()['rabbit' + str(i)]['speed']/2)
                rabbits.append(globals()['rabbit' + str(i)])
        turtle.update()
        wn.tracer(1)

wn = turtle.Screen()
wn.setup(500, 500)
wn.title('Ecosystem Simulator')

main = ttk.Frame(width=99, height=99)
main.pack(fill=BOTH)
frame1 = ttk.Frame(main, width=33, height=33)
frame1.pack(fill=BOTH, padx=100)
frame2 = ttk.Frame(main, width=33, height=33)
frame2.pack(fill=BOTH, padx=100)
frame3 = ttk.Frame(main, width=33, height=33)
frame3.pack(fill=BOTH, padx=100)

foxscale_val = IntVar()
rabbitscale_val = IntVar()
foxscale_val.set('0')
rabbitscale_val.set('0')

foxscale = ttk.Scale(frame2, orient='horizontal', from_=0, to=200, command=lambda s:foxscale_val.set('%0.f' % float(s)))
foxscale.pack(side='left')
foxscale_label_1 = ttk.Label(frame1, text='Number of Foxes:')
foxscale_label_1.pack(side='left')
foxscale_label_2 = ttk.Label(frame1, textvariable=foxscale_val)
foxscale_label_2.pack(side='left')

rabbitscale = ttk.Scale(frame2, orient='horizontal', from_=0, to=200, command=lambda s:rabbitscale_val.set('%0.f' % float(s)))
rabbitscale.pack(side='right')
rabbitscale_label_2 = ttk.Label(frame1, textvariable=rabbitscale_val)
rabbitscale_label_2.pack(side='right')
rabbitscale_label_1 = ttk.Label(frame1, text='Number of Rabbits:')
rabbitscale_label_1.pack(side='right')

printcheck_val = IntVar()

printcheck = ttk.Checkbutton(frame3, variable=printcheck_val, text='Disable printing')
printcheck.pack(side='left')

setupbutton = ttk.Button(frame3, text='Setup simulation', command = lambda: startup_simulation(foxscale.get(), rabbitscale.get()))
setupbutton.pack(side='right')


def lighten(r,g,b, factor):
        return [
        int(((100 - factor) * r + factor * 255) / 100),
        int(((100 - factor) * g + factor * 255) / 100),
        int(((100 - factor) * b + factor * 255) / 100),
        ]

def graph(nums1, nums1label, nums2, nums2label, nums3, nums3label, ylabel, xlabel, animate):
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        if animate == True:
                for i in range(len(nums1)):
                        plt.scatter(i, nums1[i], color='r')
                        plt.scatter(i, nums2[i], color='b')
                        plt.scatter(i, nums3[i], color='g')
                        plt.pause(0.01)
                plt.clf()
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.plot(nums1, color='r', label=nums1label)
        plt.plot(nums2, color='b', label=nums2label)
        plt.plot(nums3, color='g', label=nums3label)
        plt.legend()
        plt.pause(0.01)
        plt.show()

def dead():
        example = 'example.gif'
        wn = turtle.Screen()
        wn.register_shape(example)
        rocket = turtle.Turtle()
        rocket.shape(example)
        rocket.goto(100, 100)

def fox_actions():
        for f in foxes:
                if len(rabbits) > 0:
                        if f['energy'] < min([f['turt'].distance(r['turt']) for r in rabbits]):
                                f['turt'].goto(rabbits[[f['turt'].distance(r['turt']) for r in rabbits].index(min([f['turt'].distance(r['turt']) for r in rabbits]))]['turt'].pos())
                                if min([f['turt'].distance(r['turt']) for r in rabbits]) < 1 and len(rabbits) > 0:
                                        rabbits[[f['turt'].distance(r['turt']) for r in rabbits].index(min([f['turt'].distance(r['turt']) for r in rabbits]))]['turt'].hideturtle()
                                        f['energy'] += rabbits[[f['turt'].distance(r['turt']) for r in rabbits].index(min([f['turt'].distance(r['turt']) for r in rabbits]))]['energy']/2
                                        rabbits.pop([f['turt'].distance(r['turt']) for r in rabbits].index(min([f['turt'].distance(r['turt']) for r in rabbits])))
                                        print('A rabbit has been eaten!')
                if f['energy'] == 0 or f['energy'] < 0 and f in foxes:
                        f['turt'].hideturtle()
                        foxes.remove(f)
                        print('A fox has died of hunger!')
                f['energy'] =- 5
        if len(foxes) != 0:
                fox_actions()

def rabbit_actions():
        global grass
        for r in rabbits:
                if len(foxes) > 1:
                        if min([r['turt'].distance(f['turt']) for f in foxes]) < 10:
                                r['turt'].goto(list(x * -1 for x in list(foxes[[r['turt'].distance(f['turt']) for f in foxes].index(min([r['turt'].distance(f['turt']) for f in foxes]))]['turt'].pos())))
                                r['energy'] =- 5
                                print('A rabbit ran away from a fox!')
                        elif grass != 0 or grass < 0:
                                grass -= 5
                                r['energy'] =+ 2
                                print('A rabbit ate grass!' + str(grass))
                elif grass != 0 or grass < 0:
                        grass -= 5
                        r['energy'] =+ 2
                        print('A rabbit ate grass!' + str(grass))
                if r['energy'] == 0 or r['energy'] < 0 and r in rabbits:
                        r['turt'].hideturtle()
                        rabbits.remove(r)
                        print('A rabbit has died of hunger!')
                r['energy'] =- 5
        if len(rabbits) != 0:
                rabbit_actions()
        
def run_simulation():
        global startbutton
        global grass
        fox_populations = []
        rabbit_populations = []
        grass_levels = []
        startbutton.destroy()
        t1 = threading.Thread(target=fox_actions)
        t2 = threading.Thread(target=rabbit_actions)
        t1.start()
        t2.start()
        while True:
                if grass < 80:
                        grass += 20
                wn.bgcolor(lighten(0,100,0,100-grass))
                time.sleep(0.01)
                wn.update()
                foxscale_val.set(len(foxes))
                rabbitscale_val.set(len(rabbits))
                fox_populations.append(len(foxes))
                rabbit_populations.append(len(rabbits))
                grass_levels.append(grass)
                if len(foxes) == 0 and len(rabbits) == 0:
                        print('The simulation is over.')
                        graph(fox_populations, 'Foxes', rabbit_populations, 'Rabbits', grass_levels, 'Grass', 'Populations', 'Time', False)
                        break

turtle.mainloop()
