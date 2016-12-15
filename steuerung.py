#! /usr/bin/env python3
from os.path import isfile, isdir
from os import makedirs
import tkinter as tk
import shelve
from gui import Gameframe, Mainframe, Settingsframe
from data import EinstellungDaten, SpielDaten


class Steuerung(object):
    """
    Controll Class
        -Initializes GUIS
        -Sets up Games
    """

    def __init__(self):
        self.data = None
        self.start_gui = None
        self.game_gui = None
        self.new_window = None
        self.setting_gui = None
        self.setting_window = None
        self.settings = None

    def init_settings(self):

        if not isdir('./.settings'):
            makedirs('./.settings')

        if isfile('./.settings/tiktaktoe.db.dat'):
            settings_file = shelve.open('./.settings/tiktaktoe.db')
            self.settings = settings_file["lastsettings"]
            settings_file.close()
        else:
            settings_file = shelve.open('./.settings/tiktaktoe.db')
            self.settings = EinstellungDaten("Plyer1", "Plyer2")
            settings_file["lastsettings"] = self.settings
            settings_file.close()

    def init_gui(self):

        root_start = tk.Tk()
        root_start.title('TikTakTo')

        self.start_gui = Mainframe(master=root_start, Steuer=self)

        self.start_gui.mainloop()

    def save_settings(self):

        settings_file = shelve.open('./.settings/tiktaktoe.db')
        settings_file["lastsettings"] = self.settings
        settings_file.close()

    def setup_local_2player(self):

        init_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        game_sums = [0, 0, 0, 0, 0, 0, 0, 0]
        self.data = SpielDaten(spielermatrix=init_matrix, spieler=1,
                               sums=game_sums)

        self.new_window = tk.Toplevel()
        self.game_gui = Gameframe(master=self.new_window,
                                  Startwindow=self.start_gui,
                                  Steuer=self)

        self.game_gui.choose_player(1)

    def load_settings(self):

        self.setting_window = tk.Toplevel()
        self.setting_gui = Settingsframe(master=self.setting_window,
                                         Startwindow=self.start_gui,
                                         Steuer=self,
                                         Settings=self.settings)

    def move(self, point):
        currp = self.data.get_spieler()

        legal_move = self.test_move(point)

        if legal_move > 0:
            matrix = self.data.get_spielermatrix()
            sums = self.data.get_sums()
            if currp == 1:
                self.game_gui.draw_circle(point)
                matrix[point[0]][point[1]] = 1
                add_term = 1
            else:
                self.game_gui.draw_cross(point)
                matrix[point[0]][point[1]] = -1
                add_term = -1

            sums[point[0]] = sums[point[0]] + add_term
            sums[3 + point[1]] = sums[3 + point[1]] + add_term
            if point[0] == point[1]:
                sums[6] = sums[6] + add_term
            if point[0] + point[1] == 2:
                sums[7] = sums[7] + add_term

            # print(m)
            # print(s)

            self.data.set_spielermatrix(matrix)
            self.data.set_sums(sums)
            self.game_gui.rem_msg()

            winner = self.test_if_over(sums)

            if winner > 0:
                if winner == 1:
                    winnername = self.settings.get_player1()
                else:
                    winnername = self.settings.get_player2()
                self.game_gui.print_msg('The winner is %s' % winnername)
                self.data.set_winner(winner)
            else:
                nextp = currp % 2 + 1
                self.data.set_spieler(nextp)
                self.game_gui.choose_player(nextp)

        else:
            if legal_move == -1:
                self.game_gui.print_msg("To near to the boundary!")
            elif legal_move == -2:
                self.game_gui.print_msg("Square already used!")
            elif legal_move == -3:
                winner = self.data.get_winner()
                if winner == 1:
                    winnername = self.settings.get_player1()
                else:
                    winnername = self.settings.get_player2()
                self.game_gui.print_msg("GAME OVER! WINNER: %s" % winnername)

    def test_move(self, coords):
        """
        Returns:
        1  : move is legit
        -1 : to near to grid
        -2 : already filled
        -3 : game already over
        """

        if self.data.get_winner() > 0:
            return -3
        if coords[0] < 0:
            return -1
        else:
            matrix = self.data.get_spielermatrix()
            i, j = int(coords[0]), int(coords[1])

            if not matrix[i][j] == 0:
                return -2
            else:
                return 1

    @staticmethod
    def test_if_over(sums):
        if 3 in sums:
            return 1
        elif -3 in sums:
            return 2
        else:
            return 0

def main():
    # root.geometry("300x300+300+300")
    steuer = Steuerung()
    steuer.init_settings()
    steuer.init_gui()

if __name__ == '__main__':
    main()
