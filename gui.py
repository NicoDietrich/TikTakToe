import tkinter as tk


class Gameframe(tk.Frame):

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-ancestors

    def __init__(self, Steuer, Startwindow, master=None):

        self.message = tk.StringVar()
        self.master = master
        self.steuerung = Steuer
        self.player1 = self.steuerung.settings.get_player1()
        self.player2 = self.steuerung.settings.get_player2()
        self.startwindow = Startwindow
        self.canvas = None

        tk.Frame.__init__(self, master)
        # self.config(bg="grey")

        self.pack(expand=True, fill="both")
        # self.init_start_UI()
        self.init_spielfeld_ui()

    def init_spielfeld_ui(self):
        header = tk.Frame(self)
        header.pack(side="top")
        title = tk.Label(header,
                         text="Tik Tak To",
                         fg="black",
                         # bg = "grey",
                         font="Helvetica 24 bold italic")
        title.pack(padx=10, pady=10)

#   Messages
        self.messagebox = tk.Frame(self)
        self.messagebox.pack()

        self.messages = tk.Label(self.messagebox,
                                 textvariable=self.message,
                                 fg="red",
                                 # bg = "light green",
                                 font="Helvetica 14 italic")
        self.messages.pack(padx=10, pady=10)

#   GameFrame

        self.gameframe = tk.Frame(self)
        self.gameframe.pack()
        # self.gameframe.config(background="red")

#   Set up Game
        self.canvas = tk.Canvas(self.gameframe, width=216, height=216)
        self.canvas.pack(side="left", padx=10, pady=10)
        self.canvas.create_line(70, 0, 70, 216, width=3)
        self.canvas.create_line(143, 0, 143, 216, width=3)
        self.canvas.create_line(0, 70, 216, 70, width=3)
        self.canvas.create_line(0, 143, 216, 143, width=3)

#   bind klick events
        self.canvas.bind('<Button-1>', self.canv_click)

        self.gameinfo = tk.Frame(self.gameframe)
        self.gameinfo.pack(side="left", padx=10, pady=10)
        # self.gameinfo.config(background="pink")

        self.player1_display = tk.Label(self.gameinfo,
                                        text='Player 1: %s' % self.player1)
        self.player1_display.pack(padx=10, pady=10)

        self.player2_display = tk.Label(self.gameinfo,
                                        text='Player 2: %s' % self.player2)
        self.player2_display.pack(padx=10, pady=10)


#   BACK/QUITE
        self.quitbuttons = tk.Frame(self)
        # self.quitbuttons.config(background="green")
        self.quitbuttons.pack(side="bottom", expand=False, fill="x")

        self.quit_button = tk.Button(self.quitbuttons)
        self.quit_button["text"] = "Quit"
        self.quit_button["command"] = self.beenden
        self.quit_button.pack(side="right")

    def beenden(self):
        self.startwindow.show()
        self.master.destroy()

    def print_msg(self, msg):
        """msg = string"""

        self.message.set(msg)
        self.messages.pack(padx=10, pady=10)

    def rem_msg(self):
        self.messages.pack_forget()
        self.pack()

    @staticmethod
    def coord2index(coord):
        xcoord = coord[0]
        ycoord = coord[1]

        j = xcoord // 74
        i = ycoord // 74

        if xcoord % 74 > 60 or ycoord % 74 > 60:
            i = -1
            j = -1

        return [i, j]

    def canv_click(self, event):
        index = self.coord2index([event.x, event.y])
        # print('Klicked : (%d,%d)' % (index[0], index[1]))
        self.steuerung.move(index)

    def draw_circle(self, position):
        """position is given by [i,j] """

        i, j = position[0], position[1]
        self.canvas.create_oval(j*73 + 20, i*73 + 20,
                                j*73 + 50, i*73 + 50,
                                width=3)

    def draw_cross(self, position):
        """position is given by [i,j]"""

        i, j = position[0], position[1]
        self.canvas.create_line(j*73 + 20, i*73 + 20,
                                j*73 + 50, i*73 + 50,
                                width=3)
        self.canvas.create_line(j*73 + 20, i*73 + 50,
                                j*73 + 50, i*73 + 20,
                                width=3)

    def choose_player(self, player):
        if player == 1:
            self.player1_display.config(bg="grey")
            self.player2_display.config(bg=self["bg"])
        else:
            self.player2_display.config(bg="grey")
            self.player1_display.config(bg=self["bg"])


class Mainframe(tk.Frame):

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-ancestors

    def __init__(self, Steuer, master=None):

        self.steuerung = Steuer
        self.master = master

        tk.Frame.__init__(self, master)
        self.menubar = tk.Menu(master)
        master.config(menu=self.menubar)
        self.fill_menubar()
        # self.config(bg="grey")

        self.pack(expand=True, fill="both")
        self.init_start_gui()

    def fill_menubar(self):
        self.menu_file = tk.Menu(self.menubar, tearoff=False)
        self.menu_file.add_command(label="Einstellungen",
                                   command=self.settings)
        # self.menuFile.add_seperator()
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Beenden",
                                   command=self.quit)
        self.menubar.add_cascade(label="Menü",
                                 menu=self.menu_file)

    def settings(self):
        self.steuerung.load_settings()
        self.hide()

    def init_start_gui(self):

        self.header = tk.Frame(self)
        self.header.pack(side="top")
        self.title = tk.Label(self.header,
                              text="Tik Tak To",
                              fg="black",
                              # bg="grey",
                              font="Helvetica 24 bold italic")
        self.title.pack()

        self.gamebuttons = tk.Frame(self)
        # self.gamebuttons.config(background="red")
        self.gamebuttons.pack(expand=True, fill="both")

        self.singleplayer = tk.Button(self.gamebuttons)
        self.singleplayer["text"] = "Single Player"
        self.singleplayer["command"] = self.start2p_local
        self.singleplayer.pack(side="left", expand=True, fill="x")

        self.multiplayer = tk.Button(self.gamebuttons)
        self.multiplayer["text"] = "Multi Player"
        self.multiplayer.pack(side="left", expand=True, fill="x")

        self.quitbuttons = tk.Frame(self)
        # quitbuttons.config(background="green")
        self.quitbuttons.pack(side="bottom", expand=False, fill="x")

        self.quit_button = tk.Button(self.quitbuttons)
        self.quit_button["text"] = "Quit"
        self.quit_button["command"] = self.beenden
        self.quit_button.pack(side="right")

    def beenden(self):
        # self.master.destroy()
        self.steuerung.save_settings()
        self.master.quit()

    def hide(self):
        self.master.withdraw()

    def show(self):
        self.master.update()
        self.master.deiconify()

    def start2p_local(self):
        self.steuerung.setup_local_2player()
        self.hide()


class Settingsframe(tk.Frame):

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-ancestors

    def __init__(self, Steuer, Startwindow, Settings, master=None):

        self.settings = Settings
        self.master = master
        self.steuerung = Steuer
        self.startwindow = Startwindow

        tk.Frame.__init__(self, master)

        self.pack(expand=True, fill="both")
        # self.init_start_UI()
        self.init_settings_gui()

    def init_settings_gui(self):

        self.header = tk.Frame(self)
        self.header.pack(side="top")
        self.title = tk.Label(self.header,
                              text="Settings",
                              fg="black",
                              # bg = "grey",
                              font="Helvetica 24 bold italic")
        self.title.pack(padx=10, pady=10)

        self.nameframe = tk.Frame(self)
        self.nameframe.pack()

        self.namelabel = tk.Frame(self.nameframe)
        self.namelabel.pack(side="left")

        self.nameinput = tk.Frame(self.nameframe)
        self.nameinput.pack(side="right")

        self.p1_label = tk.Label(self.namelabel,
                                 text="Player 1",
                                 fg="black",
                                 font="Helvetica 10 italic")
        self.p2_label = tk.Label(self.namelabel,
                                 text="Player 2",
                                 fg="black",
                                 font="Helvetica 10 italic")
        self.p1_label.pack(side="top")
        self.p2_label.pack(side="bottom")

        self.p1_entry = tk.Entry(self.nameinput)
        self.p2_entry = tk.Entry(self.nameinput)
        self.p1_entry.pack(side="top")
        self.p2_entry.pack(side="bottom")

        self.name_p1 = tk.StringVar()
        self.name_p2 = tk.StringVar()

        self.name_p1.set(self.settings.get_player1())
        self.name_p2.set(self.settings.get_player2())

        # self.name_p1.set("nicolas")
        # self.name_p2.set("mirjam")

        self.p1_entry["textvariable"] = self.name_p1
        self.p2_entry["textvariable"] = self.name_p2

        self.quitbuttons = tk.Frame(self)
        self.quitbuttons.pack(side="bottom", expand=False, fill="x")

        self.quit_button = tk.Button(self.quitbuttons)
        self.quit_button["text"] = "Save"
        self.quit_button["command"] = self.beenden
        self.quit_button.pack(side="right")

    def beenden(self):
        self.steuerung.settings.set_player1(self.name_p1.get())
        self.steuerung.settings.set_player2(self.name_p2.get())
        self.startwindow.show()
        self.master.destroy()
