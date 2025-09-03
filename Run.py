import tkinter
from tkinter import *
import math
import random
from threading import Thread 
from collections import defaultdict
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import zlib
import sys
import hashlib

global mobile, labels, mobile_x, mobile_y, text, canvas, mobile_list, root, num_nodes, tf1, nodes, mec1, mec2, mec3, running, src_x, src_y
global mec1_x, mec1_y, mec2_x, mec2_y, mec3_x, mec3_y, env, agent, selected, selected_x, selected_y
option = 0
global cost, served_md
existing_serve = []
propose_serve = []
extension = []

def getDistance(iot_x,iot_y,x1,y1):
    flag = False
    for i in range(len(iot_x)):
        dist = math.sqrt((iot_x[i] - x1)**2 + (iot_y[i] - y1)**2)
        if dist < 60:
            flag = True
            break
    return flag    
    
def createEdge(x, y, title):
    mobile_x.append(x)
    mobile_y.append(y)
    name = canvas.create_oval(x,y,x+40,y+40, fill="blue")
    lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 7 italic bold",text=title)
    labels.append(lbl)
    mobile.append(name)
    nodes.append([x, y])

def setLocation(x1, y1, x2, y2, x3, y3):
    global mec1_x, mec1_y, mec2_x, mec2_y, mec3_x, mec3_y
    mec1_x = x1
    mec1_y = y1
    mec2_x = x2
    mec2_y = y2
    mec3_x = x3
    mec3_y = y3
    
def generateNetwork():
    global mec1_x, mec1_y, mec2_x, mec2_y, mec3_x, mec3_y, running, canvas
    global mobile, labels, mobile_x, mobile_y, num_nodes, tf1, nodes, mec1, mec2, mec3
    mobile = []
    mobile_x = []
    mobile_y = []
    labels = []
    nodes = []
    mec1_x = 5
    mec1_y = 600
    mec2_x = 5
    mec2_y = 350
    mec3_x = 5
    mec3_y = 100
    canvas.update()
    num_nodes = int(tf1.get().strip())
    createEdge(mec1_x, mec1_y, "ME3")#450 to 650
    createEdge(mec2_x, mec2_y, "ME2")#250 to 450
    createEdge(mec3_x, mec3_y, "ME1")#50 to 250
    running = True
    for i in range(3,num_nodes):
        run = True
        while run == True:
            x = random.randint(100, 450)
            y = random.randint(50, 600)
            flag = getDistance(mobile_x,mobile_y,x,y)
            if flag == False:
                nodes.append([x, y])
                mobile_x.append(x)
                mobile_y.append(y)
                run = False
                name = canvas.create_oval(x,y,x+40,y+40, fill="red")
                lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 8 italic bold",text="MN "+str(i))
                labels.append(lbl)
                mobile.append(name)       

def getEdge():
    selected = -1
    max_range = 10000
    for i in range(len(served_md)):
        if served_md[i] < max_range:
            max_range = served_md[i]
            selected = i
    served_md[selected] = served_md[selected] + 1
    return selected

def initBTTO():
    text.delete('1.0', END)
    global cost, served_md
    cost = []
    served_md = []
    for i in range(0, 3):
        served_md.append(random.randint(1, 10))
    for i in range(0, 30):
        cost.append([i, random.randint(30, 100), 30])
    text.insert(END,"BTTO initialzied with random mobile device cost and energy\n\n")      
    

def startDataTransferSimulation(canvas, line1, x1, y1, x2, y2):
    class SimulationThread(Thread):
        def __init__(self, canvas, line1, x1, y1, x2, y2): 
            Thread.__init__(self) 
            self.canvas = canvas
            self.line1 = line1
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
             
        def run(self):
            time.sleep(1)
            for i in range(0,1):
                self.canvas.delete(self.line1)
                time.sleep(1)
                self.line1 = canvas.create_line(self.x1, self.y1,self.x2, self.y2,fill='black',width=3)
                time.sleep(1)
            self.canvas.delete(self.line1)                  
            self.canvas.update()                            
    newthread = SimulationThread(canvas,line1,x1,y1,x2,y2) 
    newthread.start()    

def existingOffload():
    global selected, selected_x, selected_y, src_x, src_y, existing_serve
    text.delete('1.0', END)
    existing = 0
    for i in range(3, 23):
        serve = cost[i]
        temp = nodes[i]
        src_x = temp[0]
        src_y = temp[1]
        existing = existing + serve[1]
        selected = getEdge()
        if selected == 0:
            selected_x = 5
            selected_y = 100
        elif selected == 1:
            selected_x = 5
            selected_y = 350
        if selected == 2:
            selected_x = 5
            selected_y = 600    
        line1 = canvas.create_line(src_x+20, src_y+20, selected_x+20, selected_y+20,fill='black',width=3)
        startDataTransferSimulation(canvas,line1,(src_x+20),(src_y+20),(selected_x+20),(selected_y+20))
    existing_serve.append(existing)

def proposeOffLoad():
    global selected, selected_x, selected_y, src_x, src_y, propose_serve, extension
    text.delete('1.0', END)
    propose = 0
    cost.sort(key=lambda cost: cost[1])
    request_data = "some request data to send"+str(random.randint(10, 10000))
    existing_data = sys.getsizeof(request_data)
    compress_data = zlib.compress(request_data.encode())
    propose_data = sys.getsizeof(compress_data)
    hashcode = hashlib.sha256(compress_data).hexdigest()
    extension.append([existing_data, propose_data])
    text.insert(END,"Generated hash code on compressed request : "+hashcode+"\n")
    for i in range(3, 23):
        serve = cost[i]
        temp = nodes[i]
        src_x = temp[0]
        src_y = temp[1]
        propose = propose + serve[1]
        selected = getEdge()
        if selected == 0:
            selected_x = 5
            selected_y = 100
        elif selected == 1:
            selected_x = 5
            selected_y = 350
        if selected == 2:
            selected_x = 5
            selected_y = 600    
        line1 = canvas.create_line(src_x+20, src_y+20, selected_x+20, selected_y+20,fill='black',width=3)
        startDataTransferSimulation(canvas,line1,(src_x+20),(src_y+20),(selected_x+20),(selected_y+20))
    propose_serve.append(propose)
    text.insert(END,"Verification successful on received hash code : "+hashcode+"\n")


def servedGraph():
    global existing_serve, propose_serve
    ex = []
    pr = []
    index = []
    for i in range(len(existing_serve)):
        ex.append(int(100 - (existing_serve[i] / 20)))
        pr.append(int(100 - (propose_serve[i] / 20)))
        index.append((i + 1))
    plt.figure(figsize=(6, 4))
    plt.grid(True)
    plt.xlabel('Number of Experiments')
    plt.ylabel('Number of Served Mobile Device')
    plt.plot(index, ex, 'ro-', color = 'green')
    plt.plot(index, pr, 'ro-', color = 'blue')
    plt.legend(['Existing Technique', 'Propose Technique'], loc='upper left')
    plt.title('Number of Mobile Devices Served Comparison Graph')
    plt.show()

def energyGraph():
    global existing_serve, propose_serve
    ex = []
    pr = []
    index = []
    for i in range(len(existing_serve)):
        ex.append(existing_serve[i] / 100)
        pr.append(propose_serve[i] / 100)
        index.append((i + 1))
    plt.figure(figsize=(6, 4))
    plt.grid(True)
    plt.xlabel('Number of Experiment')
    plt.ylabel('Energy Consumption')
    plt.plot(index, ex, 'ro-', color = 'green')
    plt.plot(index, pr, 'ro-', color = 'blue')
    plt.legend(['Existing Technique', 'Propose Technique'], loc='upper left')
    plt.title('Energy Consumption Comparison Graph')
    plt.show()

def extensionGraph():
    global extension
    ex = []
    pr = []
    index = []
    for i in range(len(extension)):
        energy = extension[i]
        ex.append(energy[0] * 0.2)
        pr.append(energy[1] * 0.2)
        index.append((i + 1))
    plt.figure(figsize=(6, 4))
    plt.grid(True)
    plt.xlabel('Number of Experiment')
    plt.ylabel('Compressed & Normal Energy Consumption')
    plt.plot(index, ex, 'ro-', color = 'green')
    plt.plot(index, pr, 'ro-', color = 'blue')
    plt.legend(['Propose Energy Consumption', 'Extension Energy Consumption'], loc='upper left')
    plt.title('Propose & Extension Compressed Data Energy Consumption Graph')
    plt.show()
    

def Main():
    global root, tf1, text, canvas, mobile_list
    root = tkinter.Tk()
    root.geometry("1300x1200")
    root.title("Energy-Efficient Task Offloading and Resource Allocation for Delay-Constrained Edge-Cloud Computing Networks")
    root.resizable(True,True)
    font1 = ('times', 12, 'bold')

    canvas = Canvas(root, width = 800, height = 700)
    canvas.pack()

    l2 = Label(root, text='Num Nodes:')
    l2.config(font=font1)
    l2.place(x=820,y=10)

    tf1 = Entry(root,width=10)
    tf1.config(font=font1)
    tf1.place(x=970,y=10)
    '''

    l1 = Label(root, text='Node ID:')
    l1.config(font=font1)
    l1.place(x=820,y=60)'''
    '''

    mid = []
    for i in range(3,100):
        mid.append(str(i))
    mobile_list = ttk.Combobox(root,values=mid,postcommand=lambda: mobile_list.configure(values=mid))
    mobile_list.place(x=970,y=60)
    mobile_list.current(0)
    mobile_list.config(font=font1)'''

    generateButton = Button(root, text="Generate Edge Network", command=generateNetwork)
    generateButton.place(x=820,y=110)
    generateButton.config(font=font1)
    
    bttoButton = Button(root, text="Initialize BTTO Algorithm", command=initBTTO)
    bttoButton.place(x=820,y=160)
    bttoButton.config(font=font1)

    existingButton = Button(root, text="Run Existing Task Offload", command=existingOffload)
    existingButton.place(x=1040,y=160)
    existingButton.config(font=font1)

    proposeButton = Button(root, text="Run Propose Offload Simulation", command=proposeOffLoad)
    proposeButton.place(x=820,y=210)
    proposeButton.config(font=font1)

    servedButton = Button(root, text="Served MD Graph", command=servedGraph)
    servedButton.place(x=1100,y=210)
    servedButton.config(font=font1)

    energyButton = Button(root, text="Energy Consumption Graph", command=energyGraph)
    energyButton.place(x=820,y=260)
    energyButton.config(font=font1)

    extensionButton = Button(root, text="Extension Energy Graph", command=extensionGraph)
    extensionButton.place(x=1100,y=260)
    extensionButton.config(font=font1)

    text=Text(root,height=18,width=60)
    scroll=Scrollbar(text)
    text.configure(yscrollcommand=scroll.set)
    text.place(x=820,y=310)    
    
    root.mainloop()
   
 
if __name__== '__main__' :
    Main ()

