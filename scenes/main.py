from random import randint
from typing import Tuple

import pygame

from constants import Color
from objects import BallObject, TextObject
from scenes import BaseScene


class MainScene(BaseScene):
    MAX_COLLISIONS = 15
    BALLS_COUNT = 3

    def create_objects(self) -> None:
        self.balls = [BallObject(self.game) for _ in range(MainScene.BALLS_COUNT)]
        self.collision_count = 0
        self.status_text = TextObject(self.game, text=self.get_collisions_text(), color=Color.RED, x=0, y=0)
        self.status_text.move(10, 10)
        self.objects += self.balls
        self.objects.append(self.status_text)
        self.reset_balls_position()
        self.set_random_unique_position()

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.set_scene(self.game.PAUSE_SCENE_INDEX)

    def get_random_position(self, radius: int) -> Tuple[int, int]:
        return randint(10, self.game.WIDTH - radius * 2 - 10), randint(10, self.game.HEIGHT - radius * 2 - 10)

    def set_random_position(self, ball: BallObject) -> None:
        pos = self.get_random_position(ball.radius)
        ball.move(*pos)

    def reset_balls_position(self) -> None:
        for ball in self.balls:
            ball.move(self.game.WIDTH, self.game.HEIGHT)

    def set_random_unique_position(self) -> None:
        for index in range(len(self.balls)):
            other_rects = [self.balls[i].rect for i in range(len(self.balls)) if i != index]
            self.set_random_position(self.balls[index])
            while self.balls[index].rect.collidelist(other_rects) != -1:
                self.set_random_position(self.balls[index])

    def on_activate(self) -> None:
        self.collision_count = 0
        self.reset_balls_position()
        self.set_random_unique_position()
        self.status_text.update_text(self.get_collisions_text())
        self.status_text.move(10, 10)

    def check_ball_intercollisions(self) -> None:
        for i in range(len(self.balls) - 1):
            for j in range(i + 1, len(self.balls)):
                if self.balls[i].collides_with(self.balls[j]):
                    self.balls[i].bounce(self.balls[j])

    def get_collisions_text(self) -> str:
        return 'Wall collisions: {}/{}'.format(self.collision_count, MainScene.MAX_COLLISIONS)

    def check_ball_edge_collision(self) -> None:
        for ball in self.balls:
            if ball.edge_collision():
                self.collision_count += 1
                self.status_text.update_text(self.get_collisions_text())
                self.status_text.move(10, 10)

    def check_game_over(self) -> None:
        if self.collision_count >= MainScene.MAX_COLLISIONS:
            self.game.set_scene(self.game.GAMEOVER_SCENE_INDEX)

    def additional_logic(self) -> None:
        self.check_ball_intercollisions()
        self.check_ball_edge_collision()
        self.check_game_over()
