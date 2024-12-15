from tui import TUI

class Wordgames:
    # Internal variable initialization
    def __init__(self):
        self.game = 0
        self.n_players = 0
        self.scores = []

    def select_game(self, game):
        if 0 < game <= 3:
            self.game = game
        else:
            print("Invalid game selection. Please choose a valid game.")
            return 1

    def set_players(self, n_players):
        if 0 < n_players < 3:
            self.n_players = n_players
        else:
            print("Invalid number of players. Please choose between 1 and 3.")
            return 1


    def i_give_up(self):
        print("Game over. Better luck next time!")
        exit()

    def auto(self):
        self.game = 0
        self.n_players = 0
        self.start()

    def start(self):
        tui = TUI(self.game, self.n_players)  # Assumes TUI accepts these arguments
        tui.main()
        self.scores = tui.get_score()

    def score(self):
        return self.scores