import gc
import random
import time
from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
import sys
from collections import Counter

root = tk.Tk()
root.resizable(False, False)
# root.overrideredirect(True)
SIZE = 800
PICTURE_SIZE = 100
canvas = tk.Canvas(root, width=SIZE, height=SIZE)
picture, picture_data, picture_data_new = None, None, None
running = True
randomFillPercent = 47

RED, GREEN, BLUE, BLACK, WHITE = [255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 0, 0], [255, 255, 255]


def setWindowCenter():
    win_height = root.winfo_screenheight()
    win_width = root.winfo_screenwidth()

    posR = int(win_width / 2 - SIZE / 2)
    posD = int(win_height / 2 - SIZE / 2)
    root.geometry(f"+{posR}+{posD}")


def create_image_and_data():
    global picture, picture_data, picture_data_new
    picture = Image.new(mode="RGB", size=(PICTURE_SIZE, PICTURE_SIZE))
    picture_data_new = np.array(picture)
    for i in range(len(picture_data_new)):
        for j in range(len(picture_data_new[i])):
            if i <= 0 or i >= PICTURE_SIZE - 1 or j <= 0 or j >= PICTURE_SIZE - 1:  # if on border (2 pixels around)
                picture_data_new[i][j] == BLACK
            else:
                chance = random.randint(0, 100)
                if chance <= randomFillPercent:
                    picture_data_new[i][j] = BLACK
                else:
                    picture_data_new[i][j] = WHITE
    picture_data = picture_data_new.copy()


def edit_Image():
    global picture_data, picture_data_new, picture
    for i in range(len(picture_data)):
        for j in range(len(picture_data[i])):
            black_pixels = count_color_around_pixels(i, j, BLACK)

            if black_pixels > 4:
                change_pixel_color(i, j, BLACK)
            elif black_pixels < 4:
                change_pixel_color(i, j, WHITE)

    picture = Image.fromarray(picture_data_new)
    picture = picture.resize((SIZE, SIZE), resample=Image.BOX)
    picture_data = picture_data_new.copy()


def count_color_around_pixels(i: int, j: int, color, just_is=False):
    iStart, iStop = i - 1, i + 2
    jStart, jStop = j - 1, j + 2
    iMid, jMid = 1, 1

    if iStart < 0:
        iStart += 1
        iMid -= 1
    elif iStop >= PICTURE_SIZE:
        iStop -= 1

    if jStart < 0:
        jStart += 1
        jMid -= 1
    elif jStop >= PICTURE_SIZE:
        jStop -= 1

    around = picture_data[iStart:iStop, jStart:jStop]
    count = 9 - int(around.size / 3)
    for a in range(len(around)):
        for b in range(len(around[a])):
            if a == iMid and b == jMid:
                continue
            if (around[a, b] == color).all():
                if just_is:
                    return True
                count += 1
    if just_is:
        return False
    return count


def check_pixel_color(x: int, y: int):
    if 0 <= x < PICTURE_SIZE and 0 <= y < PICTURE_SIZE:
        return picture_data[x][y]
    else:
        return None


def change_pixel_color(x: int, y: int, color: list):
    global picture_data_new
    # if 0 <= x < PICTURE_SIZE and 0 <= y < PICTURE_SIZE:
    picture_data_new[x, y, :] = color


phase = 0
label = None
old_phase = -1


def loop():
    global label, old_phase, phase
    if phase == 0:
        build_phase()
    elif phase == 1:
        turn_areas_green_phase()
    elif phase == 2:
        turn_biggest_area_white()
    elif phase == 3:
        turn_small_areas_black()

    drawn_picture = ImageTk.PhotoImage(picture)
    if not label:
        label = tk.Label(image=drawn_picture)
    else:
        label.configure(image=drawn_picture)
    # label.image = drawn_picture # this makes so garbage collector doesn't erase it; we want it to be erased
    label.grid(column=0, row=0)
    root.update()


def build_phase():
    global phase
    old_data = picture_data_new.copy()

    edit_Image()

    if np.array_equal(picture_data_new, old_data):
        phase = 1


waiting = False
count_list = [0]
count_list_index = [[0, 0]]


def turn_biggest_area_white():
    global waiting, phase, picture, picture_data_new, picture_data
    # turn biggest area white
    if waiting:
        changed = False
        for i in range(len(picture_data)):
            for j in range(len(picture_data[i])):
                if (picture_data[i][j] == GREEN).all():
                    is_around = count_color_around_pixels(i, j, [255, 255, 255], just_is=True)
                    if is_around:
                        picture_data_new[i][j] = [255, 255, 255]
                        changed = True
        if not changed:
            phase += 1
            waiting = False
    else:
        m = max(count_list)
        for i, item in enumerate(count_list_index):
            if count_list[i] == m:
                picture_data_new[item[0]][item[1]] = [255, 255, 255]
                waiting = True
                break

    picture = Image.fromarray(picture_data_new)
    picture = picture.resize((SIZE, SIZE), resample=Image.BOX)
    picture_data = picture_data_new.copy()


def turn_small_areas_black():
    global picture, picture_data, picture_data_new, waiting
    if not waiting:
        changed = False
        for i in range(len(picture_data)):
            for j in range(len(picture_data[i])):
                if (picture_data[i][j] == GREEN).all():
                    c = count_color_around_pixels(i, j, BLACK)
                    if c > 0:
                        picture_data_new[i][j] = BLACK
                        changed = True
        if not changed:
            waiting = True
        picture = Image.fromarray(picture_data_new)
        picture = picture.resize((SIZE, SIZE), resample=Image.BOX)
        picture_data = picture_data_new.copy()


def green_phase_loop():
    global picture_data, picture_data_new, waiting, count_list, count_list_index, phase

    if not waiting:
        for i in range(len(picture_data)):
            for j in range(len(picture_data[i])):
                if (picture_data[i][j] == WHITE).all():
                    picture_data_new[i][j] = GREEN
                    count_list[-1] += 1
                    count_list_index[-1] = [i, j]
                    waiting = True
                    return
        # no more white pixels!
        count_list = count_list[:-1]
        count_list_index = count_list_index[:-1]
        waiting = False
        phase += 1
    else:
        changed = False
        # if white pixel is next to green, it changes to green
        for i in range(len(picture_data)):
            for j in range(len(picture_data[i])):
                if (picture_data[i][j] == WHITE).all():
                    is_green_around = count_color_around_pixels(i, j, GREEN, just_is=True)
                    if is_green_around:
                        picture_data_new[i][j] = GREEN
                        count_list[-1] += 1
                        changed = True
        if not changed:
            waiting = False
            count_list.append(0)
            count_list_index.append([-1, -1])


def turn_areas_green_phase():
    # global picture_data, picture_data_new, picture, waiting, count_list
    global picture, picture_data

    green_phase_loop()

    '''
    # find white pixels
    x = np.where(picture_data_new == 255)
    indexList = list(zip(x[0], x[1]))
    whiteIndexValues = [ele for ele, count in Counter(indexList).items() if count == 3]

    for item in whiteIndexValues:
        pass
    '''

    picture = Image.fromarray(picture_data_new)
    picture = picture.resize((SIZE, SIZE), resample=Image.BOX)
    picture_data = picture_data_new.copy()


delta_time = 0
frames = 0


def time_and_loop():
    global delta_time, frames, old_phase, phase
    startTime = time.time()

    loop()

    endTime = time.time()
    delta_time += endTime - startTime
    frames += 1
    if delta_time >= 1:
        num = gc.get_count()
        if old_phase != phase:
            print(f"FPS: {frames}; GC: {num}; Phase: {phase}")
            old_phase = phase
        else:
            print(f"FPS: {frames}; GC: {num}")
        delta_time = 0
        frames = 0


def main():
    setWindowCenter()
    create_image_and_data()
    while running:
        loop()
        # time_and_loop()


if __name__ == '__main__':
    main()
