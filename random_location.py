"""Prints a string within terminal bounds"""
from blessed import Terminal
from random import randint
from time import sleep



term = Terminal()
def location(text):
    
    text_len = term.length(text)
    width, height = term.width, term.height
    if width - text_len < 5:
        width += text_len
    with term.location(randint(5, width-text_len), randint(0, height)):
        print(text)
        

