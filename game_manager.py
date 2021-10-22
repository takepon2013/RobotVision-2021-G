import pygame
from bullet import Bullet
from typing import List


class GameManager:
    first_bullets: List[Bullet] = []
    second_bullets: List[Bullet] = []

    def __init__(self):
        self.first_bullets = []
        self.second_bullets = []