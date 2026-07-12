import cv2
import numpy as np
import imageio
import matplotlib.pyplot as plt
import sys
import os

import tkinter as tk
from tkinter import filedialog, Label, Button, TOP, messagebox

from PIL import Image, ImageTk


# -------------------- GUI --------------------
top = tk.Tk()
top.geometry("400x400")
top.title("Cartoonify Your Image!")
top.configure(background="white")

label = Label(
    top,
    background="#CDCDCD",
    font=("calibri", 20, "bold")
)


# -------------------- Upload Image --------------------
def upload():
    image_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif"),
            ("All Files", "*.*")
        ]
    )

    if image_path:
        cartoonify(image_path)


# -------------------- Cartoonify Function --------------------
def cartoonify(image_path):

    # Read image
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    if original_image is None:
        print("Cannot find any image. Choose an appropriate file.")
        sys.exit()

    resized1 = cv2.resize(original_image, (960, 540))

    # Grayscale
    gray = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)
    resized2 = cv2.resize(gray, (960, 540))

    # Blur
    smooth = cv2.medianBlur(gray, 5)
    resized3 = cv2.resize(smooth, (960, 540))

    # Edge Detection
    edges = cv2.adaptiveThreshold(
        smooth,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        9,
        9
    )

    resized4 = cv2.resize(edges, (960, 540))

    # Bilateral Filter
    color = cv2.bilateralFilter(original_image, 9, 300, 300)
    resized5 = cv2.resize(color, (960, 540))

    # Cartoon Effect
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    resized6 = cv2.resize(cartoon, (960, 540))

    # Display Results
    images = [
        resized1,
        resized2,
        resized3,
        resized4,
        resized5,
        resized6
    ]

    titles = [
        "Original",
        "Gray",
        "Blur",
        "Edges",
        "Color",
        "Cartoon"
    ]

    fig, axes = plt.subplots(
        3,
        2,
        figsize=(10, 8),
        subplot_kw={"xticks": [], "yticks": []}
    )

    for i, ax in enumerate(axes.flat):
        if i in [1, 2, 3]:
            ax.imshow(images[i], cmap="gray")
        else:
            ax.imshow(images[i])

        ax.set_title(titles[i])

    plt.tight_layout()
    plt.show()

    save_btn = Button(
        top,
        text="Save Cartoon Image",
        command=lambda: save(resized6, image_path),
        padx=30,
        pady=5,
        background="#364156",
        foreground="white",
        font=("calibri", 10, "bold")
    )

    save_btn.pack(side=TOP, pady=20)


# -------------------- Save Image --------------------
def save(cartoon_image, image_path):

    new_name = "cartoonified_Image"

    folder = os.path.dirname(image_path)
    extension = os.path.splitext(image_path)[1]

    save_path = os.path.join(folder, new_name + extension)

    cv2.imwrite(
        save_path,
        cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR)
    )

    messagebox.showinfo(
        "Success",
        f"Image saved successfully!\n\n{save_path}"
    )


# -------------------- Upload Button --------------------
upload_btn = Button(
    top,
    text="Cartoonify an Image",
    command=upload,
    padx=10,
    pady=5,
    background="#364156",
    foreground="white",
    font=("calibri", 10, "bold")
)

upload_btn.pack(side=TOP, pady=50)

top.mainloop()