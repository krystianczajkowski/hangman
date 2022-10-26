from hangman_game import play_game

def test_play_game():
    assert play_game('word', 'definition') == None
    