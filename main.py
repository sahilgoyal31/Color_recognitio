from tkinter import *
from PIL import Image
from PIL import ImageTk
import tkinter.filedialog as tkFileDialog
import cv2 as cv2
import pandas as pd

# -------------------------------------------------------------------------------------------------------------
imagee = cv2.imread("color_new.jpg")


def startt():
    app.destroy()


# -------------------------------------------------------------------------------------------------------------
def select_image():
    global panelA;

    path = tkFileDialog.askopenfilename()

    # ensure a file path was selected
    if len(path) > 0:
        img = cv2.imread(path)

    global imagee
    imagee = img;
    height, width, c = img.shape
    if height > 500:
        img = cv2.resize(img, (800, 550))
    if width > 800:
        img = cv2.resize(img, (800, 550))

    image = Image.fromarray(img)
    image = ImageTk.PhotoImage(image)

    if panelA is None:
        # the first panel will store our original image
        panelA = Label(image=image)
        panelA.image = image
        panelA.pack(side="left", padx=10, pady=10)
    else:
        # update the pannels
        panelA.configure(image=image)

        panelA.image = image


# -------------------------------------------------------------------------------------------------------------
import tkinter as tk
import tkinter.font as tkFont

app = tk.Tk()
Label(app, text='Color Recognition', font=(
    'Verdana', 30)).pack(side=TOP, pady=10)
Label(app, text='Select an image and press enter button to start colour recognition in Image', font=(
    'Verdana', 15)).pack(side=TOP, pady=10)
app.title("Color_Recognition By SG")
app.geometry("1000x800")
panelA = None

buttonExample1 = tk.Button(app,
                           text="Select an Image",
                           width=25,
                           height=10, command=select_image)

buttonExample2 = tk.Button(app,
                           text="Enter",
                           width=20,
                           height=10, command=startt)
buttonExample1.pack(side=tk.LEFT)
buttonExample2.pack(side=tk.RIGHT)

app.mainloop()
# -------------------------------------------------------------------------------------------------------------
img = imagee;
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)
clicked = False
r = g = b = xpos = ypos = 0


def getColorName(R, G, B):
    minimum = 1000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if (d < minimum):
            minimum = d
            color_name = csv.loc[i, "color_name"]
    return color_name


def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


cv2.namedWindow('color detection')
cv2.setMouseCallback('color detection', draw_function)
# -------------------------------------------------------------------------------------------------------------
while (1):

    cv2.imshow("color detection", img)
    if (clicked):
        # cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        color_name = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, color_name, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        # For very light colours we will display text in black colour
        if (r + g + b >= 600):
            cv2.putText(img, color_name, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False
    # when user hit esc
    if cv2.waitKey(20) & 0xFF == 27:
        break
# -------------------------------------------------------------------------------------------------------------
cv2.destroyAllWindows()

# kick off the GUI




