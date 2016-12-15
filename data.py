"""
dummy
"""

class SpielDaten():
    """
    dummy
    """
    def __init__(self, spielermatrix, spieler, sums):
        """
        dummy
        """
        self.spieler = spieler
        self.spielermatrix = spielermatrix
        self.sums = sums
        self.winner = 0

    def get_winner(self):
        """
        dummy
        """
        return self.winner

    def set_winner(self, winner):
        """
        dummy
        """
        self.winner = winner

    def get_sums(self):
        """
        dummy
        """
        return self.sums

    def set_sums(self, summe):
        """
        dummy
        """
        self.sums = summe

    def get_spieler(self):
        """
        dummy
        """
        return self.spieler

    def set_spieler(self, player_number):
        """
        dummy
        """
        self.spieler = player_number

    def get_spielermatrix(self):
        """
        dummy
        """
        return self.spielermatrix

    def set_spielermatrix(self, matrix):
        """
        dummy
        """
        self.spielermatrix = matrix


class EinstellungDaten():
    """
    dummy
    """
    def __init__(self, player1, player2):
        """
        dummy
        """
        self.__player1 = player1
        self.__player2 = player2

    def get_player1(self):
        """
        dummy
        """
        return self.__player1

    def get_player2(self):
        """
        dummy
        """
        return self.__player2

    def set_player1(self, player1):
        """
        dummy
        """
        self.__player1 = player1

    def set_player2(self, player2):
        """
        dummy
        """
        self.__player2 = player2
