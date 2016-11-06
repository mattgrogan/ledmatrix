import Tkinter as tk


class LED_Gui(object):

  def __init__(self, master):

    frame = tk.Frame(master)
    frame.pack()

    self.button = tk.Button(frame, text="Quit", command=frame.quit)
    self.button.pack(side=tk.LEFT)
