import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

class DraggableRectangle(object):
    def __init__(self):
        self.ax = plt.gca()
        self.rect = Rectangle((0.5,0), 0.22, 2,facecolor='g', alpha=0.2)
        self.rectl = Rectangle((0.5-0.05, 0), 0.05, 0.2, facecolor='b', alpha=0.8)
        self.rectr = Rectangle((0.5+0.22, 0), 0.05, 0.2, facecolor='b', alpha=0.8)
        self.rect_x = 0.5

        self.ax.add_patch(self.rect)
        self.ax.add_patch(self.rectl)
        self.ax.add_patch(self.rectr)

        self.press = None # 0,
        self.pressl = None
        self.pressr = None

        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)


    def on_press(self, event):
        if event.inaxes != self.rect.axes: return
        contains, attrd = self.rect.contains(event)
        containsl, attrdl = self.rectl.contains(event)
        containsr, attrdr = self.rectr.contains(event)
        if contains:
            x0, y0 = self.rect.xy
            self.press = x0, y0, event.xdata, event.ydata
        elif containsl:
            xl, yl = self.rectl.xy
            self.pressl = xl, yl, event.xdata, event.ydata
        elif containsr:
            xr, yr = self.rectr.xy
            self.pressr = xr, yr, event.xdata, event.ydata
        else:
            return

    def on_release(self, event):
        print ('release')
        self.press = None
        self.pressl = None
        self.pressr = None
        self.ax.figure.canvas.draw()

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None and self.pressl is None and self.pressr is None: return
        if event.inaxes != self.rect.axes and event.inaxes != self.rectl.axes and event.inaxes != self.rectr.axes: return

        if self.press != None:
            x0, y0, xpress, ypress = self.press
            dx = event.xdata - xpress
            self.rect_x = x0+dx
            self.rect.set_x(self.rect_x)
            self.rectl.set_x(self.rect_x-self.rectl.get_width())
            self.rectr.set_x(self.rect_x+self.rect.get_width())
            # self.rect.figure.canvas.draw()
        elif self.pressl != None:
            if event.xdata >= self.rectr.get_x()-0.1: return
            xl, yl, xpress, ypress = self.pressl
            dx = event.xdata - xpress
            self.rectl.set_x(xl + dx - self.rectl.get_width())
            # draw rect
            self.rect.set_x(xl + dx)
            xr = self.rectr.get_x()
            recwidth = xr-xl-dx
            self.rect.set_width(recwidth)
            # self.rectl.figure.canvas.draw()
        elif self.pressr != None:
            if event.xdata <= self.rectl.get_x()+self.rectl.get_width()+0.1: return
            xr, yr, xpress, ypress = self.pressr
            dx = event.xdata - xpress
            self.rectr.set_x(xr+dx)
            # draw rect
            xl = self.rectl.get_x()
            recwidth = xr+dx - xl - self.rectl.get_width()
            self.rect.set_width(recwidth)
            # self.rectr.figure.canvas.draw()

        self.rect.figure.canvas.draw()# why we just draw rect here, but rectl and rectr are drawed too ?


t = np.arange(0, 8, .01)
s = np.sin(3 * np.pi * t)
plt.plot(t,s)

plt.axis([0, 2, 0, 2])
a = DraggableRectangle()
plt.show()