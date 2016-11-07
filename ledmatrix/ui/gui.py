import Tkinter as tk

import PIL.Image as Image
import PIL.ImageTk as ImageTk

GUI_WIDTH = 512
GUI_HEIGHT = 512


class Gui(tk.Tk):

  def __init__(self, controller):

    tk.Tk.__init__(self, None, None)

    self.controller = controller
    self.controller.matrix = self

    from remote_control import Mock_Remote_Control
    self.rc = Mock_Remote_Control()

    frame = tk.Frame(self)
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

    self.blank_image = Image.new(
        "RGB", (GUI_WIDTH, GUI_HEIGHT), color="#000000")
    self.blank_image = ImageTk.PhotoImage(self.blank_image)

    self.img_label = tk.Label(frame, image=self.blank_image)
    self.img_label.image = self.blank_image
    self.img_label.pack(side=tk.RIGHT)

    self.after(0, self.start)

  def set_image(self, image):

    image = image.resize((GUI_WIDTH, GUI_HEIGHT))
    image = ImageTk.PhotoImage(image)

    self.img_label.image = image
    self.img_label.configure(image=image)
    self.update()

  def clear(self):
    self.img_label.image = self.blank_image
    self.img_label.configure(image=self.blank_image)
    self.update()

  def start(self):

    requested_delay_ms = self.controller.run()
    self.after(requested_delay_ms, self.start)
