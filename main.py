from wordgames import Wordgames

game = Wordgames()
game.set_players(1)
game.select_game(3)
game.start()

print(game.score())