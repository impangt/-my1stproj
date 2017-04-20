import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle


class DraggableRectangle(object):
    def __init__(self, axes, rectwidth=100, lrwidth=10, recty=100):
        self.ax = axes  # plt.gca()

        self.rect_x = axes.get_xlim()[1] - rectwidth - lrwidth
        self.rect = Rectangle((self.rect_x, 0), rectwidth, recty, facecolor='g', alpha=0.2)
        self.rectl = Rectangle((self.rect_x - lrwidth, 0), lrwidth, recty, facecolor='b', alpha=0.8)
        self.rectr = Rectangle((self.rect_x + rectwidth, 0), lrwidth, recty, facecolor='b', alpha=0.8)

        self.ax.add_patch(self.rect)
        self.ax.add_patch(self.rectl)
        self.ax.add_patch(self.rectr)

        self.rect_width = rectwidth
        self.press = None  # 0,
        self.pressl = None
        self.pressr = None

        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

        # self.reset_right()

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
        # print ('release')
        self.press = None
        self.pressl = None
        self.pressr = None
        self.ax.figure.canvas.draw()

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None and self.pressl is None and self.pressr is None: return
        if event.inaxes != self.rect.axes and event.inaxes != self.rectl.axes and event.inaxes != self.rectr.axes: return

        rectwidth = self.rect_width
        if self.press != None:
            x0, y0, xpress, ypress = self.press
            dx = event.xdata - xpress
            rectl_x = x0 + dx  - self.rectl.get_width()

            # to tell the left edge overriding
            if rectl_x < 0:
                rectl_x = 0
            # to tell the right edge overriding
            if rectl_x + self.rectl.get_width() + rectwidth + self.rectr.get_width() > self.ax.get_xlim()[1]:
                rectl_x = self.rect_x - self.rectl.get_width()

            self.rect_x = rectl_x + self.rectl.get_width()
            self.rect.set_x(self.rect_x)
            self.rectl.set_x(rectl_x)
            self.rectr.set_x(self.rect_x + self.rect.get_width())
            # self.rect.figure.canvas.draw()
        elif self.pressl != None:
            if event.xdata >= self.rectr.get_x() - 10:
                self.rect_width = 10
                return

            xl, yl, xpress, ypress = self.pressl
            dx = event.xdata - xpress
            rectl_x = xl + dx #- self.rectl.get_width()

            # to tell the left edge overriding
            if rectl_x < 0:
                self.rect_width = self.rectr.get_x() - self.rectl.get_width()
                rectl_x = 0

            self.rectl.set_x(rectl_x)
            # draw rect
            self.rect.set_x(rectl_x + self.rectl.get_width())
            xr = self.rectr.get_x()
            rectwidth = xr - rectl_x - self.rectl.get_width()
            # self.rectl.figure.canvas.draw()
        elif self.pressr != None:
            if event.xdata <= self.rect_x + 10:
                self.rect_width = 10
                return

            xr, yr, xpress, ypress = self.pressr
            dx = event.xdata - xpress
            rectr_x = xr + dx

            # to tell the right edge overriding
            xlim = self.ax.get_xlim()[1]
            if rectr_x + self.rectr.get_width() > xlim:
                self.rect_width = xlim -self.rectl.get_x() - self.rectl.get_width()
                rectr_x = xlim - self.rectr.get_width()

            self.rectr.set_x(rectr_x)
            # draw rect
            rectwidth = rectr_x - self.rectl.get_x() - self.rectl.get_width()
            # self.rectr.figure.canvas.draw()

        self.rect.set_width(rectwidth)
        self.rect_width = rectwidth
        self.ax.figure.canvas.draw()
        # self.rect.figure.canvas.draw()  # why we just draw rect here, but rectl and rectr are drawed too ?

    def reset_left(self):
        self.rectl.set_x(0.0)
        self.rect_x = self.rectl.get_width()
        self.rect.set_x(self.rect_x)
        self.rectr.set_x(self.rect_x + self.rect_width)

    def reset_right(self):
        xlim = self.ax.get_xlim()[1]
        self.rectr.set_x(xlim - self.rectl.get_width())
        self.rect_x = xlim - self.rectl.get_width()-self.rect_width
        self.rect.set_x(self.rect_x)
        self.rectl.set_x(self.rect_x - self.rectl.get_width())

    def reset_full(self):
        self.rectl.set_x(0.0)
        xlim = self.ax.get_xlim()[1]
        self.rect_x = self.rectl.get_width()
        self.rect.set_x(self.rect_x)
        self.rectr.set_x(xlim - self.rectl.get_width())
        self.rect_width = xlim - self.rectl.get_width() - self.rect_x
        self.rect.set_width(self.rect_width)
        self.ax.figure.canvas.draw()

    def get_rect_x1(self):
        return int(self.rectl.get_x())

    def get_rect_x2(self):
        return int(self.rectr.get_x()+self.rectr.get_width())

        # t = np.arange(0, 8, .01)
        # s = np.sin(3 * np.pi * t)
        # plt.plot(t,s)
        #
        # plt.axis([0, 2, 0, 2])
        # a = DraggableRectangle()
        # plt.show()
