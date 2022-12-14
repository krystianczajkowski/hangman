from project import get_word, find_lttr, select_language
import pytest

def test_get_word_supported():
    assert get_word('test_language') == 'test'


def test_get_word_unsupported():
    with pytest.raises(FileNotFoundError) as FNFE:
        get_word('enmglish') 
    assert "No such file or directory" in str(FNFE)

def test_select_language_unsuppported():
    assert select_language('piglatin') == 'english'
    assert select_language('en') == 'english'
    assert select_language('german') == 'english'


def test_select_language_supported():
    assert select_language('english') == 'english'
    assert select_language('polish') == 'polish'


def test_find_lttr_correct():
    assert find_lttr('word', ['_', '_', '_', '_'], 'u') == ['_', '_', '_', '_']
    assert find_lttr('word', ['_', '_', '_', '_'], 'word') == 'word'
    assert find_lttr('word', ['w', '_', 'r', '_'], 'w') == ['w', '_', 'r', '_']
    assert find_lttr('word', ['w', 'o', 'r', '_'], 'd') == ['w', 'o', 'r', 'd']


def test_find_lttr_incorrect():
    assert find_lttr('word', ['_', '_', '_', '_'], 'p') == ['_', '_', '_', '_']
    assert find_lttr('word', ['_', 'o', 'r', 'd'], 'a') == ['_', 'o', 'r', 'd']


def test_find_lttr_special_chars():
    assert find_lttr('word', ['w', '_', 'r', '_'],
                     '{;[]') == ['w', '_', 'r', '_']
    assert find_lttr('word', ['w', '_', 'r', '_'],
                     '\\') == ['w', '_', 'r', '_']


def test_find_lttr_more_chars():
    assert find_lttr('word', ['_', '_', '_', '_'],
                     'wa s') == ['w', '_', '_', '_']
    assert find_lttr('word', ['_', '_', '_', '_'],
                     'abcde j') == ['_', '_', '_', '_']


def test_find_lttr_with_space():
    assert find_lttr('word with space', ['_', '_', '_', '_', ' ', '_', '_', '_', '_', ' ', '_', '_', '_', '_', '_'], 'w') == [
        'w', '_', '_', '_', ' ', 'w', '_', '_', '_', ' ', '_', '_', '_', '_', '_']
