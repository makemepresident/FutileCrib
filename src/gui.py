import tkinter as tk

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master # Tk() subsystem
        self.master.geometry("500x500") # top, right, bot, left
        self.pack()
        # self.create_widgets()
        self.initLayout()
        self.mockHand(self.ply)
        self.mockHand(self.opp)

        self.mockHand(self.gam)

    def initLayout(self):
        # init player hand frame
        # init playing frame
        # init opp hand frame
        # position bot, mid, top of above
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        self.opp = tk.Frame(width=width, height=height)
        # self.gam = tk.Frame(width=width - ((width / 6) * 2), height=height - ((height / 6) * 2), background="red")
        self.gam = tk.Frame(background="red")
        self.ply = tk.Frame(width=width, height=height)

        self.opp.pack(side="top")
        self.gam.pack(fill="x")
        self.ply.pack(side="bottom")

    def mockHand(self, pane):
        self.hand = []
        for i in range(6):
            obj = tk.Button(pane, text="Card "+str(i + 1), height=8, width=5)
            obj.pack(side="left")
            self.hand.append(obj)

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()