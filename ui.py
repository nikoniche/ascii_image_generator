import json
import os
import time
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from image_to_ascii import convert_image_to_text
from ascii_to_image import generate_image

WIDTH, HEIGHT = 1600, 900
FRAME_SIZE = 600
BG_COLOR = "#303030"
FONT = "Consolas"

with open("config.json", "r") as r:
    config = json.load(r)
    DOWNLOAD_DIR = config["download_path"]

DOWNLOAD_NAME = "output-onlineasciitools.png"

DOWNLOAD = f"{DOWNLOAD_DIR}\{DOWNLOAD_NAME}"


def _bind_hover(widget):
    def darken(event: tk.Event) -> None:
        event.widget.config(bg="darkgray")

    def revert(event: tk.Event) -> None:
        event.widget.config(bg="gray")

    widget.bind("<Enter>", darken)
    widget.bind("<Leave>", revert)


class UI(tk.Tk):

    def __init__(self):
        super().__init__()

        self.template_path = None
        self.current_result = None

        self.image_references = []

        self.title("Image Substitution")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.config(bg=BG_COLOR)

        # centering widgets in row
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # generating title labels
        self._generate_label(0, "Original image")
        self._generate_label(2, "Result")

        # generating image placeholders
        self.original_placeholder = self._generate_image_placeholder(0)
        self.result_placeholder = self._generate_image_placeholder(2)

        # generate browse buttons
        self._generate_button("Open image", 0, 2, self._save_browsed_path)

        self.invert_var = tk.BooleanVar()
        check_button = tk.Checkbutton(self, text="Invert background", variable=self.invert_var, font=(FONT, 14),
                                      bg="gray", height=1, relief="ridge", width=20)
        check_button.grid(column=1, row=3)
        _bind_hover(check_button)

        # generate _show button
        self._generate_button("Show", 2, 2, self._show)

        # main button
        self.execute_button = self._generate_button("Generate", 1, 2, lambda: self.after(1, self._generate_result))

        # frame for settings placement
        settings_frame = tk.Frame(self, bg=BG_COLOR, width=20)
        settings_frame.grid(column=1, row=4)

        # generating description labels
        width_label = tk.Label(settings_frame, text="Width: ", font=(FONT, 15), bg=BG_COLOR)
        width_label.grid(column=0, row=0, sticky="w")
        font_label = tk.Label(settings_frame, text="Font size: ", font=(FONT, 15), bg=BG_COLOR)
        font_label.grid(column=0, row=1, sticky="w")

        # generating entries for settings
        self.width_entry = tk.Entry(settings_frame, width=11, bg="gray", font=(FONT, 15), relief="solid")
        self.width_entry.grid(column=1, row=0, sticky="e")
        self.font_entry = tk.Entry(settings_frame, width=11, bg="gray", font=(FONT, 15), relief="solid")
        self.font_entry.grid(column=1, row=1, sticky="e")

        # generate save as button
        self._generate_button("Save as", 2, 3, self._save_result)

        self.mainloop()

    def _display_image(self, path: str, placeholder: tk.Label, image=None) -> None:
        """Displays an image in a placeholder. Automatically rescales the image to fit the placeholder."""

        # calculates new width for the image, so it fits well into the frame
        scale = FRAME_SIZE - 12

        image = Image.open(path) if image is None else image

        # calculates new dimensions for rescaling the image
        img_width, img_height = image.size
        if img_width > img_height:
            new_dimensions = scale, round(img_height / img_width * scale)
        else:
            new_dimensions = round(img_width / img_height * scale), scale

        image = image.resize(new_dimensions)

        # applies the changes
        photo_image = ImageTk.PhotoImage(image)
        placeholder.config(image=photo_image)

        # saves the photo image reference
        self.image_references.append(photo_image)

    def _generate_image_placeholder(self, column: int) -> tk.Label:
        """Generates a placeholder and with it its parent frame."""

        frame = tk.Frame(self, borderwidth=3, bg="black", relief="ridge",
                         width=FRAME_SIZE, height=FRAME_SIZE)

        padding = (30, 0) if column == 0 else (0, 30)
        frame.grid(column=column, row=1, padx=padding)
        frame.grid_propagate(False)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        placeholder = tk.Label(frame, bg="gray")
        placeholder.grid(sticky="nsew")
        self._display_image("neutral_image.jpg", placeholder)
        return placeholder

    def _generate_label(self, column: int, text: str) -> None:
        """Generates a title label."""

        label = tk.Label(self, text=text, font=(FONT, 19), bg=BG_COLOR, fg="white")
        label.grid(column=column, row=0, pady=(40, 10))

    def _save_browsed_path(self) -> None:
        """Asks the user for a path to a directory and saves it to a set variable depending on the index argument."""

        filepath = filedialog.askopenfilename()

        self.template_path = filepath

        self._display_image(filepath, self.original_placeholder)

    def _generate_button(self, text: str, column: int, row: int, func, *args) -> tk.Button:
        """Generates a button."""

        button = tk.Button(self, text=text, relief="ridge", bg="gray", width=20, height=1,
                           font=(FONT, 15),
                           command=lambda: func(*args))
        button.grid(column=column, row=row, pady=(10, 0))

        _bind_hover(button)

        return button

    def _generate_result(self):
        width_str = self.width_entry.get()
        font_size_str = self.font_entry.get()

        width = None if width_str == "" else int(width_str)
        if font_size_str == "":
            print("No font size selected")
            return
        font_size = int(font_size_str)
        invert = self.invert_var.get()

        self.execute_button.config(text="Generating..")

        convert_image_to_text(self.template_path, font_size, width, inverted=invert)
        self.current_result = generate_image(font_size)

        self.execute_button.config(text="Displaying..")
        self._display_image("none", self.result_placeholder, image=self.current_result)

        self.execute_button.config(text="Generate")

    def _show(self):
        """Shows the current result in a separate window."""

        if self.current_result is not None:
            self.current_result.show()

    def _save_result(self):
        """Asks the user for a save location and saves the result."""

        dialog = filedialog.asksaveasfile(mode="w", defaultextension=".png", filetypes=[("PNG files", ".png")])
        if dialog is not None:
            save_path = dialog.name

            if self.current_result is not None:
                try:
                    self.current_result.save(save_path)
                except OSError:
                    jpg_path = save_path.replace(".png", ".jpg")
                    self.current_result.save(jpg_path)
                finally:
                    os.remove(DOWNLOAD)
