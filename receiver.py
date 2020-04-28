import pika
from tkinter import *
import threading
class App(threading.Thread):

    def __init__(self, tk_root,t,text,q1):
        self.root = tk_root
        threading.Thread.__init__(self)
        self.start()
        self.t=t
        self.text=text
        self.q1=q1
    def on_message(self,channel, method_frame, header_frame, body):
        self.t.config(state=NORMAL)
        self.text=body
        self.text=self.text[:-1]
        self.t.delete('1.0', END)
        self.t.insert(INSERT,self.text)
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        self.t.config(state=DISABLED)
    def run(self):
        connection = pika.BlockingConnection()
        channel = connection.channel()
        channel.basic_consume(self.q1, self.on_message)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        connection.close()
class receiver(threading.Thread) :
    def run(self) :
        self.ROOT = Tk()
        self.text=""
        self.ROOT.title('receiver')
        self.frame = Frame(self.ROOT,width=50,height=30)
        self.t=Text(self.ROOT,borderwidth=5,height=30,width=50)
        self.t.config(state=DISABLED)
        self.t.grid(row=0,column=0)
        self.frame.grid()
        APP = App(self.ROOT,self.t,self.text,self.q1)
        self.ROOT.mainloop()
    def __init__(self,q1) :
        threading.Thread.__init__(self)
        self.start()
        self.q1=q1


        



