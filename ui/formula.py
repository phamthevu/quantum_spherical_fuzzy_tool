import tkinter as tk
from PIL import Image, ImageTk
from core.resource import resource_path

_formula_cache = {}

def add_formula_image(parent, img_path, width=700):
    img = Image.open(resource_path(img_path))
    w, h = img.size
    scale = width / w
    img = img.resize((int(w * scale), int(h * scale)))

    photo = ImageTk.PhotoImage(img)
    _formula_cache[img_path] = photo

    lbl = tk.Label(parent, image=photo)
    lbl.pack(pady=10)