import pygame
from pathlib import Path
import sys

def getImage():
    root = Path(__file__).resolve().parent.parent
    print(root)
    return pygame.image.load(root / "assets/item_04.png")
