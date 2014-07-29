from Tkinter import *

def InitalizeBoard(windowsSize,boxSize):
    theCanvas = Canvas(width = windowsSize[0], height = windowsSize[1])
    point1 = ((windowsSize[0]-boxSize[0])/2,(windowsSize[1]-boxSize[1])/2)
    point2 = ((windowsSize[0]-boxSize[0])/2+boxSize[0],(windowsSize[1]-boxSize[1])/2)
    point3 = ((windowsSize[0]-boxSize[0])/2+boxSize[0],(windowsSize[1]-boxSize[1])/2+boxSize[1])
    point4 = ((windowsSize[0]-boxSize[0])/2,(windowsSize[1]-boxSize[1])/2+boxSize[1])
    drawLine(theCanvas, point1, point2, "black", 2.0)
    drawLine(theCanvas, point2, point3, "black", 2.0)
    drawLine(theCanvas, point3, point4, "black", 2.0)
    drawLine(theCanvas, point4, point1, "black", 2.0)
    theCanvas.pack()
    return theCanvas

def drawPoint(canvas, point, col, r, windowsSize):
    (x,y) = point
    the_point = canvas.create_oval(x+windowsSize[0]/2-r,y+windowsSize[1]/2-r,x+windowsSize[0]/2+r,y+windowsSize[1]/2+r,fill=col,outline='')
    return the_point

def drawLine(canvas, point1, point2, col, linewidth):
    (x1,y1)=point1
    (x2,y2)=point2
    canvas.create_line(x1,y1,x2,y2,fill=col,width=linewidth)
