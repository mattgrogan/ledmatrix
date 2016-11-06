import Tkinter as tk

import PIL.Image as Image
import PIL.ImageTk as ImageTk


class LED_Gui(object):

  def __init__(self, root, controller, rc):

    self.root = root
    self.controller = controller
    self.rc = rc

    frame = tk.Frame(root)
    frame.pack()

    up_button = tk.Button(frame, text="Up", command=controller.handle_up)
    down_button = tk.Button(frame, text="Down", command=controller.handle_down)
    left_button = tk.Button(frame, text="Left", command=controller.handle_left)
    right_button = tk.Button(
        frame, text="Right", command=controller.handle_right)
    stop_button = tk.Button(frame, text="Stop", command=controller.handle_stop)
    quit_button = tk.Button(frame, text="Quit", command=frame.quit)

    up_button.pack(side=tk.LEFT)
    down_button.pack(side=tk.LEFT)
    left_button.pack(side=tk.LEFT)
    right_button.pack(side=tk.LEFT)
    stop_button.pack(side=tk.LEFT)
    quit_button.pack(side=tk.LEFT)

    self.blank_image = Image.new("RGB", (128, 128), color="#000000")
    self.blank_image = ImageTk.PhotoImage(self.blank_image)

    self.img_label = tk.Label(frame, image=self.blank_image)
    self.img_label.image = self.blank_image
    self.img_label.pack(side=tk.RIGHT)

  def set_image(self, image):

    image = image.resize((128, 128))
    image = ImageTk.PhotoImage(image)

    self.img_label.image = image
    self.img_label.configure(image=image)
    self.root.update()

  def clear(self):
    self.img_label.image = self.blank_image
    self.img_label.configure(image=self.blank_image)
    self.root.update()

  def start(self):

    self.controller.run(self.rc)
    self.root.after(1, self.start)
