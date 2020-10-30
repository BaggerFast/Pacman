from random import randint

from constants import Color
from objects.ball import BallObject
from objects.text import Text
from scenes.base import BaseScene


class MainScene(BaseScene):
    MAX_COLLISIONS = 15
    balls_count = 3

    def create_objects(self):
        self.text_count = Text(self.game, text='', color=Color.RED, x=400, y=550)
        self.balls = [BallObject(self.game) for _ in range(MainScene.balls_count)]
        self.objects = self.balls + [self.text_count]
        self.reset_balls_position()
        self.set_random_unique_position()

    def additional_logic(self):
        self.process_ball_collisions()
        self.text_count.update_text(
            'Коллизии со стенами: {}/{}'.format(
                self.game.wall_collision_count,
                self.MAX_COLLISIONS
            )
        )
        if self.game.wall_collision_count >= self.MAX_COLLISIONS:
            self.game.set_scene(self.game.GAMEOVER_SCENE_INDEX)

    def process_ball_collisions(self):
        for i in range(len(self.balls) - 1):
            for j in range(i + 1, len(self.balls)):
                if self.balls[i].collides_with(self.balls[j]):
                    print('Мячи {} и {} столкнулись'.format(i, j))
                    self.balls[i].bounce(self.balls[j])

    def reset_balls_position(self):
        for ball in self.balls:
            ball.move(self.game.width, self.game.height)

    def get_random_position(self, radius):
        return randint(10, self.game.width - radius*2 - 10), randint(10, self.game.height - radius*2 - 10)

    def set_random_position(self, ball):
        pos = self.get_random_position(ball.radius)
        ball.move(*pos)

    def set_random_unique_position(self):
        for index in range(len(self.balls)):
            other_rects = [self.balls[i].rect for i in range(len(self.balls)) if i != index]
            self.set_random_position(self.balls[index])
            while self.balls[index].rect.collidelist(other_rects) != -1:
                self.set_random_position(self.balls[index])