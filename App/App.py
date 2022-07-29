import tkinter as tk
from tkinter import Tk
from PIL import Image, ImageTk, ImageDraw
from PIL import ImageColor as ImgC
import numpy


class App(Tk):
    def __init__(self, img_size, scale):
        super().__init__()
        # Vars
        self.size = img_size * scale
        self.img_size = img_size
        self.scale = scale
        self.center = int(self.size / 2)
        self.tk_img = None

        # Window Setup
        self.title("Simulation")
        self.resizable(False, False)
        self.canvas = tk.Canvas(self, width=self.size, height=self.size)
        self.canvas.pack()

        # Center on screen
        posR = int(self.winfo_screenwidth() / 2 - self.center)
        posD = int(self.winfo_screenheight() / 2 - self.center)
        self.geometry(f"+{posR}+{posD}")

        self.image = Image.new("RGB", (self.img_size, self.img_size))
        self.pixelX = 0
        self.pixelY = 0
        self.image.putpixel((self.pixelX, self.pixelY), ImgC.getrgb("Red"))
        self.color_border(ImgC.getrgb("BLUE"))
        self.update_image()

    def update_image(self):
        self.tk_img = ImageTk.PhotoImage(self.image.resize((self.size, self.size), Image.BOX))
        self.canvas.create_image(self.center, self.center, image=self.tk_img)

    def color_border(self, color):
        draw = ImageDraw.Draw(self.image)
        draw.line([(0, 0), (0, self.img_size - 1)], color, 1)
        draw.line([(0, 0), (self.img_size - 1, 0)], color, 1)
        draw.line([(0, self.img_size - 1), (self.img_size - 1, self.img_size - 1)], color, 1)
        draw.line([(self.img_size - 1, 0), (self.img_size - 1, self.img_size - 1)], color, 1)

    def color_pixel(self, x, y, color):
        self.image.putpixel((x, y), color)

    def get_neighbor_count(self, colorList):
        img_array = numpy.array(self.image)
        count = []
        for i in range(len(img_array)):  # each row
            for j in range(len(img_array[i])):  # each pixel
                tempColorList = []
                for color in colorList:  # check each color given
                    tempColorList.append(0)
                    for k in range(max(i - 1, 0), min(i + 1, self.img_size - 1), 1):  # check neighbors
                        for m in range(max(j - 1, 0), min(j + 1, self.img_size - 1), 1):
                            if k == i and m == j:  # don't count current pixel
                                continue
                            if img_array[k][m] == color:
                                tempColorList[-1] += 1
                count.append(tempColorList)
        return count

    def mainloop(self, n=0):  # will need to do the main loop in main method
        while True:
            self.update()
            self.update_idletasks()
            # self.move_pixel()
            self.update_image()


if __name__ == '__main__':
    app = App(100, 5)  # Need to do this in main method
    app.mainloop()
