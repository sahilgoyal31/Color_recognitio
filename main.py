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
    print(height,width)
    if height > 500:
        img = cv2.resize(img, (800, 550))
    if width > 800:
        img = cv2.resize(img, (800, 550))

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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
import tkinter.font as font

app = tk.Tk()
app.configure(bg='cyan')

Label(app, text='Color Recognition ', borderwidth = 2,relief="ridge",font=(
    'Monotype Corsiva', 38,'bold'),fg="green",bg="yellow").pack(side=TOP, pady=10)
Label(app, text='Select an image and press enter button to start colour recognition in Image ', font=(
    'Verdana', 15)).pack(side=TOP, pady=10)
Label(app, text='( Press Esc to close colour recognition application)', font=(
    'Verdana', 11),fg="red").pack(side=TOP, pady=10)
app.title("Color_Recognition By SG(1810992075)")
app.geometry("1000x800")
panelA = None

buttonExample1 = tk.Button(app,
                           text="Select an Image",width=12,height=10,
                            command=select_image,bg='#32CD32')
buttonExample1['font'] = font.Font(weight="bold")
buttonExample2 = tk.Button(app,width=10,height=10,
                           text="Enter", command=startt,bg='#32CD32')
buttonExample2['font'] = font.Font(weight="bold")
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
       
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        color_name = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        
        cv2.putText(img, color_name, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        
        if (r + g + b >= 600):
            cv2.putText(img, color_name, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False
    
    if cv2.waitKey(20) & 0xFF == 27:
        break
# -------------------------------------------------------------------------------------------------------------
cv2.destroyAllWindows()






