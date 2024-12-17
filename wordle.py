import pytermgui as ptg
import random
from functools import reduce
import enchant
import time

def add_window(mgr, win):
    mgr.add(win.set_title("[210 bold]WordGames.py").center())

class Wordle:
    def __init__(self, num_players):
        self.players = num_players
        self.curr_stage = 0
        self.word = None
        self.alpha_count = {}
        self.inputs = [[["[white]■" for i in range(5)] for i in range(5)] for i in range(num_players)]
        self.winner = []

    def start(self, mgr):
        with open("./wordle-answers-alphabetical.txt") as f:
            words = [line.strip() for line in f]
        self.word = random.choice(words)
        self.alpha_count = {letter: self.word.count(letter) for letter in set(self.word)}
        self.play_stage(mgr)

    def get_status(self, player):
        return reduce(lambda x, y: "".join(x) + "\n" + "".join(y), self.inputs[player])

    def process_answers(self, stage, mgr):
        for i in range(self.players):
            if "".join(self.inputs[i][stage]).replace("[white]", "") == self.word:
                self.winner.append(i)
            else:
                curr_alpha_count = self.alpha_count.copy()
                for j in range(5):
                    if self.inputs[i][stage][j].replace("[white]", "") == self.word[j]:
                        self.inputs[i][stage][j] = self.inputs[i][stage][j].replace("[white]", "[lime]")
                        curr_alpha_count[self.word[j]] -= 1
                for j in range(5):                
                    if self.inputs[i][stage][j].replace("[white]", "") in self.word and curr_alpha_count[self.inputs[i][stage][j].replace("[white]", "")] > 0:
                        self.inputs[i][stage][j] = self.inputs[i][stage][j].replace("[white]", "[yellow]")
                        curr_alpha_count[self.inputs[i][stage][j].replace("[yellow]", "")] -= 1
                    else:
                        self.inputs[i][stage][j] = self.inputs[i][stage][j].replace("[white]", "[grey]")
        if len(self.winner) == 1:
            self.show_score(mgr, self.winner[0])
            return 1
        elif len(self.winner) > 1:
            self.show_score(mgr, None)
            return 1
                

    def play_stage(self, mgr):
        if self.curr_stage == 5:
            return self.show_score(mgr, -1)
        else:
            if self.curr_stage > 0:
                ret = self.process_answers(self.curr_stage - 1, mgr)
                if ret == 1:
                    return
            self.get_answer(mgr, 0)
            self.curr_stage += 1

    def get_answer(self, mgr, player):
        error_label = ptg.Label("")
        status_label = ptg.Label(self.get_status(player))
        d = enchant.Dict("en_US")
        def submit_word(mgr, win, input_field):
            user_word = input_field.value.lower().strip()
            if user_word == "":
                return
            elif d.check(user_word) and len(user_word) == 5:
                self.inputs[player][self.curr_stage - 1] = ["[white]" + user_word[i] for i in range(5)]
                status_label.value = self.get_status(player)
                time.sleep(1)
                mgr.remove(win)
                if (player + 1 == self.players):
                    self.play_stage(mgr)
                else:
                    self.get_answer(mgr, player + 1)
            else:
                error_label.value = "Invalid word."
                time.sleep(1)
                error_label.value = ""
                input_field.delete_back(len(user_word))
        input_field = ptg.InputField("", prompt="Enter a word: ")
        game_win = ptg.Window(
            "",
            "Wordle",
            "[210 bold] Player " + str(player + 1) + "'s turn.",
            status_label,
            "",
            input_field,
            error_label,
            ptg.Button("Submit", lambda *_: submit_word(mgr, game_win, input_field)),
            width=30,
            height=6
        )
        add_window(mgr, game_win)

    def show_score(self, mgr, player = None):
        if player is None:
            winner = "It's a draw!"
        elif player < 0:
            winner = "This Wordle was unsolved!\nThe word was: " + self.word
        else:
            winner = f"Player {player + 1} won!"
        game_win = ptg.Window(
            "",
            "Wordle",
            "[210 bold] Game Over",
            ptg.Label(winner),
            ptg.Button("Quit", lambda *_: mgr.stop()),
            width=30,
            height=6
        )
        add_window(mgr, game_win)

    def get_score(self):
        if len(self.winner) == 1:
            return [1 if i == self.winner[0] else 0 for i in range(self.players)]
        else:
            return [0 for i in range(self.players)]