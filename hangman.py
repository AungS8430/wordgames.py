import random
import enchant
import pytermgui as ptg
import time

def add_window(mgr, win):
    mgr.add(win.set_title("[210 bold]WordGames.py").center())


hangman_stages = [
    '''
      +---+
      |   |
          |
          |
          |
     ======''',
    '''
      +---+
      |   |
      O   |
          |
          |
     ======''',
    '''
      +---+
      |   |
      O   |
      |   |
          |
     ======''',
    '''
      +---+
      |   |
      O   |
     /|   |
          |
     ======''',
    '''
      +---+
      |   |
      O   |
     /|\  |
          |
     ======''',
    '''
      +---+
      |   |
      O   |
     /|\  |
     /    |
     ======''',
    '''
      +---+
      |   |
      O   |
     /|\  |
     / \  |
     ======'''
]


class Hangman:
    def __init__(self, num_players):
        self.players = num_players
        self.scores = [0] * num_players
        self.guessed_words = set()
        self.rounds = 0
        self.curr_round = 0


    def main(self, mgr):
        self.get_rounds(mgr)

    def get_rounds(self, mgr):
        round_win = ptg.Window(
            "",
            "Hangman",
            ptg.Splitter(
                ptg.KeyboardButton("3", lambda *_: self.set_rounds(mgr, 3, round_win)),
                ptg.KeyboardButton("5", lambda *_: self.set_rounds(mgr, 5, round_win)),
                ptg.KeyboardButton("7", lambda *_: self.set_rounds(mgr, 7, round_win))
            ),
            width=60,
            height=5
        )
        add_window(mgr, round_win)

    def set_rounds(self, mgr, rounds, win):
        self.rounds = rounds
        mgr.remove(win)
        self.start(mgr)

    def start(self, mgr, curr=0):
        if (self.curr_round == 0):
            curr = random.randint(0, self.players - 1)
        self.play_round(mgr, curr)
        self.curr_round += 1

    def play_round(self, mgr, curr):
        word = self.get_word(curr, mgr)
        return curr

    def get_word(self, player, mgr):
        d = enchant.Dict("en_US")
        error_label = ptg.Label("")
        scoreboard = ptg.Label("\n".join(f"Player {i+1} Score: {score}" for i, score in enumerate(self.scores)))

        def submit_word(mgr, win, input_field):
            user_word = input_field.value
            if user_word == "":
                return
            elif d.check(user_word):
                mgr.remove(win)
                self.get_guesses(mgr, player, (player + 1) % self.players, 0, user_word.lower(), "_" * len(user_word))
            else:
                error_label.value = "Invalid word."
                time.sleep(1)
                error_label.value = ""
                input_field.delete_back(len(user_word))

        input_field = ptg.InputField("", prompt="Enter a word: ")
        word_win = ptg.Window(
            f"[210 bold]Player {player + 1}",
            ptg.Splitter(
                ptg.Container(
                    scoreboard
                ),
                ptg.Container(
                    input_field,
                    error_label,
                    ptg.Button("Submit", lambda *_: submit_word(mgr, word_win, input_field)),
                    width=60,
                    height=20
                ),
            ),
            width=80,
            height=6
        )
        add_window(mgr, word_win)


    def get_guesses(self, mgr, host, player, stage, correct_word, o_word):
        error_label = ptg.Label("")
        hangman_status = ptg.Label(hangman_stages[stage])
        scoreboard = ptg.Label("\n".join(f"Player {i+1} Score: {score}" for i, score in enumerate(self.scores)))

        def submit_guess(mgr, win, input_field):
            nonlocal o_word
            user_guess = input_field.value
            if user_guess == "" or len(user_guess) > 1:
                error_label.value = "Invalid guess."
                time.sleep(1)
                error_label.value = ""
                input_field.delete_back(len(user_guess))
            elif user_guess in self.guessed_words and user_guess != "":
                error_label.value = "You already guessed that letter."
                time.sleep(1)
                error_label.value = ""
                input_field.delete_back(len(input_field.value))
            else:
                user_guess = user_guess.lower()
                self.guessed_words.add(user_guess)
                if user_guess in correct_word:
                    self.scores[player] += 5
                    for i in range(len(correct_word)):
                        if correct_word[i] == user_guess:
                            o_word = o_word[:i] + user_guess + o_word[i+1:]
                    hangman_status.value = hangman_stages[stage]
                    error_label.value = "Correct guess."
                    time.sleep(1)
                    if o_word == correct_word:
                        self.scores[player] += 30
                        error_label.value = "You win!"
                        self.guessed_words = set()
                        scoreboard.value = "\n".join(f"Player {i+1} Score: {score}" for i, score in enumerate(self.scores))
                        time.sleep(1)
                        mgr.remove(win)
                        self.curr_round += 1
                        self.get_word(player, mgr)
                    elif stage == len(hangman_stages) - 1:
                        self.scores[host] += 30
                        error_label.value = "You lose! The answer is " + correct_word
                        time.sleep(1)
                        self.guessed_words = set()
                        scoreboard.value = "\n".join(f"Player {i+1} Score: {score}" for i, score in enumerate(self.scores))
                        mgr.remove(win)
                        self.curr_round += 1
                        self.get_word((host + 1) % self.players + 1, mgr)
                    else:
                        mgr.remove(win)
                        if (player + 1) % self.players == host:
                            self.get_guesses(mgr, host, (player + 2) % self.players, stage, correct_word, o_word)
                        else:
                            self.get_guesses(mgr, host, (player + 1) % self.players, stage, correct_word, o_word)
                else:
                    self.scores[player] -= 5
                    scoreboard.value = "\n".join(f"Player {i+1} Score: {score}" for i, score in enumerate(self.scores))
                    hangman_status.value = hangman_stages[min(stage + 1, len(hangman_stages) - 1)]
                    error_label.value = "Incorrect guess."
                    time.sleep(1)
                    mgr.remove(win)
                    if stage == len(hangman_stages) - 1:
                        self.curr_round += 1
                        self.get_word((host + 1) % self.players + 1, mgr)
                    else:
                        if (player + 1) % self.players == host:
                            self.get_guesses(mgr, host, (player + 2) % self.players, min(stage + 1, len(hangman_stages) - 1), correct_word, o_word)
                        else:
                            self.get_guesses(mgr, host, (player + 1) % self.players, min(stage + 1, len(hangman_stages) - 1), correct_word, o_word)
                if self.curr_round == self.rounds:
                    mgr.remove(win)
                    self.show_score(mgr)                

        input_field = ptg.InputField("", prompt="Enter a guess: ")
        guess_win = ptg.Window(
            f"[210 bold]Player {player + 1}",
            ptg.Splitter(
                ptg.Container(
                    hangman_status,
                    scoreboard
                ),
                ptg.Container(
                    input_field,
                    error_label,
                    ptg.Button("Submit", lambda *_: submit_guess(mgr, guess_win, input_field)),
                    width=60,
                    height=5
                )
            ),
            width=80,
            height=6
        )
        add_window(mgr, guess_win)

    def show_score(self, mgr):
        scoreboard = ptg.Label("\n".join(f"Player {i+1} Score: {score}" for i, score in enumerate(self.scores)))
        score_win = ptg.Window(
            "Game Over",
            scoreboard,
            ptg.Button("Quit", lambda *_: exit()),
            width=80,
            height=6
        )
        add_window(mgr, score_win)

