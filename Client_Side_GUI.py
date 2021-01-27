import socket
from tkinter import *
import threading
import requests

response = 'Nothing'
#insert raspberry pi IP on the network
#currently set to local host

global IP

http = 'http://'
IP = 'http://127.0.0.1:8080'

def setIP(ip):
    global IP
    IP = http + ip + ":8080"
    print(IP)

class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.title("Beta Carnival Control Code")
        self.root.geometry("550x550")

        self.IPvar = StringVar()
        self.IPvar.set(IP)

        canvas = Canvas(self.root, width = 250, height = 130)      
        canvas.pack()      
        img = PhotoImage(file="CarnivalLogo.gif")      
        canvas.create_image(125,65, anchor=CENTER, image=img)  

        self.root.iconphoto(False, PhotoImage(file='dragon.png'))

        w0 = Label(self.root,text=response)
        l = Label(self.root, text = "Beta Carnival Control Panel") 
        l.config(font =("Courier", 15))
        l.pack()

        #IP label
        l3 = Label(self.root, text = "Current Raspberry PI IP:") 
        l3.config(font =("Courier", 12))
        l3.pack()

        #IP label
        self.l4 = Label(self.root, textvariable = self.IPvar) 
        self.l4.config(font =("Courier", 12))
        self.l4.pack()

        self.IPentry = Entry(self.root, width=50, textvariable=StringVar, justify='center')
        self.IPentry.pack(side=TOP,padx=10,pady=10)

        b1 = Button(self.root,text="Set IP (insert only the numbers before the colon)",command = self.test)
        b1.pack()

        l0 = Label(self.root, text = "This control code resets the position of the ball launcher. \n Move the sliders to the desired position then release the button") 
        l0.config(font =("Courier", 9))
        l0.pack()

        #pitch label
        l1 = Label(self.root, text = "Pitch Control") 
        l1.config(font =("Courier", 12))
        l1.pack()

        #pitch slider 
        self.pitchSlider = Scale(self.root, from_=60, to=0)
        self.pitchSlider.set(0)
        self.pitchSlider.bind("<ButtonRelease-1>", self.pitchUpdate)
        self.pitchSlider.pack()

        #yaw label
        l2 = Label(self.root, text = "Yaw Control") 
        l2.config(font =("Courier", 12))
        l2.pack()

        #yaw slider
        self.yawSlider = Scale(self.root, from_=-60, to=60, orient=HORIZONTAL)
        self.yawSlider.set(0)
        self.yawSlider.bind("<ButtonRelease-1>", self.yawUpdate)
        self.yawSlider.pack()
        

        self.root.mainloop()

    def pitchUpdate(self, event):
        val = self.pitchSlider.get()
        msg = {'pitch.Set': val}
        requests.post(IP, data = msg)
        print(val)

    def yawUpdate(self, event):
        val = self.yawSlider.get()
        msg = {'yaw.Set': val}
        requests.post(IP, data = msg)
        print(val)

    def test(self):
        ip = self.IPentry.get()
        self.IPvar.set(http + ip + ":8080")
        setIP(self.IPentry.get())   

    

app = App()

server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'mitbetastream'
token = 'oauth:hpptp1vgedhbvlv75gzr33n18stotd'
channel = '#mitbetastream'

sock = socket.socket()

sock.connect((server, port))
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))  


while True:
    resp = sock.recv(2048).decode('utf-8')

    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))
    
    elif len(resp) > 0:
        formatted = resp.split(":")
        if formatted[-1].rstrip().upper() == 'W':
            msg = {'pitch.Inc': 1}
            requests.post(IP, data = msg)
            print('Up')
        elif formatted[-1].rstrip().upper() == 'S':
            msg = {'pitch.Inc': -1}
            requests.post(IP, data = msg)
            print('Down')
        elif formatted[-1].rstrip().upper() == 'A':
            msg = {'yaw.Inc': -1}
            requests.post(IP, data = msg)
            print('Left')
        elif formatted[-1].rstrip().upper() == 'D':
            msg = {'yaw.Inc': 1}
            requests.post(IP, data = msg)
            print('Right')
        
        
        response = resp



    

