import Tkinter as tk

import PIL.Image as Image
import PIL.ImageTk as ImageTk

from device import Tk_Image

GUI_WIDTH = 512
GUI_HEIGHT = 512


class Gui(tk.Tk):

  def __init__(self, controller):

    tk.Tk.__init__(self, None, None)

    self.controller = controller
    #self.controller.matrix = self

    from remote_control import Mock_Remote_Control
    from zmq_control import ZeroMQ_Control
    self.rc = ZeroMQ_Control()
    self.rc.register(u"KEY_STOP", controller, controller.handle_mode)
    self.rc.register(u"KEY_UP", controller, controller.handle_up)
    self.rc.register(u"KEY_DOWN", controller, controller.handle_down)
    self.rc.register(u"KEY_LEFT", controller, controller.handle_left)
    self.rc.register(u"KEY_RIGHT", controller, controller.handle_right)

    frame = tk.Frame(self)
    frame.grid(row=0, column=0, sticky=tk.W)

    # Row 1
    voldown_btn = tk.Button(frame, text="Vol-")
    playpause_btn = tk.Button(
        frame, text="Play/Pause", command=controller.handle_playpause)
    volup_btn = tk.Button(frame, text="Vol+")

    voldown_btn.grid(row=1, column=1)
    playpause_btn.grid(row=1, column=2)
    volup_btn.grid(row=1, column=3)

    # Row 2
    setup_btn = tk.Button(frame, text="Setup", command=controller.handle_setup)
    up_btn = tk.Button(frame, text="Up", command=controller.handle_up)
    mode_btn = tk.Button(frame, text="Mode", command=controller.handle_mode)

    setup_btn.grid(row=2, column=1)
    up_btn.grid(row=2, column=2)
    mode_btn.grid(row=2, column=3)

    # Row 3
    left_btn = tk.Button(frame, text="Left", command=controller.handle_left)
    enter_btn = tk.Button(frame, text="Enter", command=controller.handle_enter)
    right_btn = tk.Button(frame, text="Right", command=controller.handle_right)

    left_btn.grid(row=3, column=1)
    enter_btn.grid(row=3, column=2)
    right_btn.grid(row=3, column=3)

    # Row 4
    zero_btn = tk.Button(frame, text="0/10+")
    down_btn = tk.Button(frame, text="Down", command=controller.handle_down)
    back_btn = tk.Button(frame, text="Back", command=controller.handle_back)

    zero_btn.grid(row=4, column=1)
    down_btn.grid(row=4, column=2)
    back_btn.grid(row=4, column=3)

    # Bind the keys
    self.bind("<Left>", controller.handle_left)
    self.bind("<Right>", controller.handle_right)
    self.bind("<Up>", controller.handle_up)
    self.bind("<Down>", controller.handle_down)

    self.blank_image = Image.new(
        "RGB", (GUI_WIDTH, GUI_HEIGHT), color="#000000")
    self.blank_image = ImageTk.PhotoImage(self.blank_image)

    self.img_label = tk.Label(self, image=self.blank_image)
    self.img_label.image = self.blank_image
    self.img_label.grid(row=0, column=1, sticky=tk.E)

    #self.image = Tk_Image(self.img_label, zoom=10)

    self.controller.matrix = Tk_Image(label=self.img_label, zoom=10)

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

    self.rc.read_command()
    requested_delay_ms = self.controller.run()
    self.after(requested_delay_ms, self.start)
