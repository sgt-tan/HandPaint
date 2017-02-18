import Tkinter as tk
from PIL import Image,ImageDraw
import os

class ImageGenerator:
    def __init__(self,parent,posx,posy,*kwargs):
        self.parent = parent
        self.posx = posx
        self.posy = posy
        self.sizex = 700
        self.sizey = 700
        self.b1 = "up"
        self.xold = None
        self.yold = None
        self.coords= []
        self.drawing_area=tk.Canvas(self.parent,width=self.sizex,height=self.sizey)
        self.drawing_area.place(x=self.posx,y=self.posy)
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.b1down)
        self.drawing_area.bind("<ButtonRelease-1>", self.b1up)
        self.button=tk.Button(self.parent,text="Done!",width=10,bg='white',command=self.save)
        self.button.place(x=self.sizex/6,y=self.sizey+20)
        self.button1=tk.Button(self.parent,text="Clear!",width=10,bg='white',command=self.clear)
        self.button1.place(x=(self.sizex - self.sizex/6),y=self.sizey+20)
        #self.button1=tk.Button(self.parent,text="Close!",width=10,bg='white',command=self.close)
        #self.button1.place(x=(self.sizex/8)+220,y=self.sizey+20)
        self.image=Image.new("RGB",(800,800),"white")
        self.draw=ImageDraw.Draw(self.image)

    def save(self):
        print self.coords
        self.draw.line(self.coords,('black'),width=2)
        filename = "canvas.png"
        self.image.save(filename)
        self.draw.line(self.coords,('white'),width=2)

    def clear(self):
        self.coords=[]
        self.drawing_area.delete("all")
    
    #def close(self):
    #    self.destroy()

    def b1down(self,event):
        self.b1 = "down"

    def b1up(self,event):
        self.b1 = "up"
        self.xold = None
        self.yold = None
        #self.draw.line(self.coords,('black'),width=2)
        #self.coords = []

    def motion(self,event):
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                event.widget.create_line(self.xold, self.yold, 
                                         event.x, event.y, 
                                         smooth='true', width=2, 
                                         fill='black')
                self.coords.append((self.xold,self.yold))
        elif self.xold is None and self.yold is None:
            self.draw.line(self.coords,('black'),width=2)
            self.coords = []

        self.xold = event.x
        self.yold = event.y

root=tk.Tk()
root.title("Draw a Sketch!")
root.wm_geometry("%dx%d+%d+%d" % (800, 800, 10, 10))
root.config(bg='white')
ImageGenerator(root,10,10)
root.mainloop()
