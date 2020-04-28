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
        self.text=body
        self.text=self.text[:-1]
        self.t.delete('1.0', END)
        self.t.insert(INSERT,self.text)
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    def run(self):
        connection = pika.BlockingConnection()
        channel = connection.channel()
        channel.basic_consume(self.q1, self.on_message)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        connection.close()
class sender(threading.Thread) :
    def send (self,msg):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=self.q)
        channel.basic_publish(exchange='',routing_key=self.q,body=msg)
        channel.queue_declare(queue=self.q2)
        channel.basic_publish(exchange='',routing_key=self.q2,body=msg)
        connection.close()
    def key (self,e):
        print(e.char)
        if e.char.isalpha() or e.char==' '  :
            self.text=self.t.get('1.0','end')
            self.send(self.text)
    def bs (self,e):
        text=self.text
        text=text[:-1]
        self.t.delete('1.0', END)
        self.t.insert(INSERT,text)
        self.text=text
        self.send(self.text)   
    def run(self) :
        self.ROOT = Tk()
        self.text=""
        self.ROOT.title('sender')
        self.frame = Frame(self.ROOT,width=50,height=30)
        self.t=Text(self.ROOT,borderwidth=5,height=30,width=50)
        self.t.bind('<KeyRelease>',self.key)
        self.t.bind('<BackSpace>',self.bs)
        self.t.grid(row=0,column=0)
        self.frame.grid()
        APP = App(self.ROOT,self.t,self.text,self.q1)
        self.ROOT.mainloop()
    def __init__(self,q,q1,q2) :
        threading.Thread.__init__(self)
        self.start()
        self.q=q
        self.q1=q1
        self.q2=q2

        



