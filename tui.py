import pytermgui as ptg

CONFIG = """
config:
    InputField:
        styles:
            prompt: dim italic
            cursor: '@72'
    Label:
        styles:
            value: bold

    Window:
        styles:
            border: '60'
            corner: '60'

    Container:
        styles:
            border: '96'
            corner: '96'
"""

def add_window(mgr, win):
    mgr.add(win.set_title("[210 bold]WordGames.py").center())

class TUI:
    def __init__(self, game, players):
        self.game = game
        self.players = players

    def main(self):
        with ptg.YamlLoader() as loader:
            loader.load(CONFIG)

        with ptg.WindowManager() as mgr:
            if self.game == 0:
                self.get_game(mgr)
            if self.players == 0:
                self.get_players(mgr)
            self.start(mgr)

    def get_game(self, mgr):
        game_win = ptg.Window(
            "",
            "Welcome to WordGames.py",
            "Please select a game to play",
            ptg.Splitter(
                ptg.KeyboardButton("Wordle", lambda *_: self.set_game(mgr, 1, game_win)),
                ptg.KeyboardButton("Hangman", lambda *_: self.set_game(mgr, 2, game_win))
            ),
            width=60,
            height=5
        )
        add_window(mgr, game_win)

    def get_players(self, mgr):
        players_win = ptg.Window(
            "",
            "Welcome to WordGames.py",
            "Please choose the number of players",
            ptg.Splitter(
                ptg.KeyboardButton("1", lambda *_: self.set_players(mgr, 1, players_win)),
                ptg.KeyboardButton("2", lambda *_: self.set_players(mgr, 2, players_win)),
                ptg.KeyboardButton("3", lambda *_: self.set_players(mgr, 3, players_win))
            ),
            width=60,
            height=5
        )
        add_window(mgr, players_win)

    def set_game(self, mgr, game_choice, win):
        self.game = game_choice
        mgr.remove(win)

    def set_players(self, mgr, player_count, win):
        self.players = player_count
        mgr.remove(win)

    def start(self, mgr):
        print(f"Starting game {self.game} with {self.players} players!")
        #self.stop(mgr)

    def stop(self, mgr):
        mgr.stop()