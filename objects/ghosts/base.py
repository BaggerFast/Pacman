import pygame as pg
from misc import Animator, get_path, GHOSTS_MOVING, EvenType
from misc.animator import SpriteSheetAnimator
from misc.sprite_sheet import SpriteSheet
from objects import Character, Pacman, Text
from typing import Tuple
import random

from objects.ghosts.ghost_states import GhostState


class Base(Character):
    love_point_in_scatter_mode = (0, 0)
    max_count_eat_seeds_in_home = 0
    direction2 = {
        0: (1, 0, "right"),
        1: (0, 1, "down"),
        2: (-1, 0, "left"),
        3: (0, -1, "up")
    }

    def __init__(self, game, start_pos: Tuple[int, int], frightened_time, chase_time, scatter_time) -> None:
        self.process_logic_iterator = 0
        self.deceleration_multiplier = 1
        self.acceleration_multiplier = 1
        self.deceleration_multiplier_with_rect = 1

        self.frightened_time = frightened_time
        self.chase_time = chase_time
        self.scatter_time = scatter_time

        self.walk_anim = SpriteSheetAnimator(
           SpriteSheet(get_path(f'images/ghost/{type(self).__name__.lower()}/walk.png'), (14, 14))
        )
        self.frightened_walk_anim1 = Animator(
           SpriteSheet(get_path('images/ghost/fear1.png'), (14, 14))[0], aura=get_path('images/ghost/aura_blue.png')
        )
        self.frightened_walk_anim2 = Animator(
           SpriteSheet(get_path('images/ghost/fear2.png'), (14, 14))[0], aura=get_path('images/ghost/aura_white.png')
        )

        self.eaten_walk_anim = SpriteSheetAnimator(SpriteSheet(get_path('images/ghost/eaten.png'), (12, 14)))

        super().__init__(
            game,
            self.walk_anim,
            start_pos,
            get_path(f'images/ghost/{type(self).__name__.lower()}/aura.png'))

        self.is_can_leave_home = False
        self.count_eat_seeds_in_home = 0

        self.collision = False
        self.set_direction("left")

        self.timer = pg.time.get_ticks()
        self.ai_timer = pg.time.get_ticks()
        self.invisible_anim = Animator(SpriteSheet(get_path('images/ghost/invisible.png'))[0])
        self.love_cell = (0, 0)

        self.is_invisible = False
        self.is_in_home = True

        self.work_counter = True

        self.mode = GhostState.scatter
        self.gg_text = Text(
            self.game, ' ',
            10, pg.Rect(0, 0, 0, 0),
        )

        self.tmp_flag1 = False
        self.tmp_flag2 = False

        self.old_timer = pg.time.get_ticks()
        self.old_ai_timer = pg.time.get_ticks()

    def process_logic(self) -> None:
        self.deceleration_multiplier_with_rect = 1
        for rect in self.game.current_scene.slow_ghost_rect:
            if self.in_rect(rect):
                self.deceleration_multiplier_with_rect = 2
        self.deceleration_multiplier_with_rect *= self.deceleration_multiplier
        if self.is_in_home and not self.can_leave_home:
            self.go()
            if self.rect.centery >= self.start_pos[1] + 5:
                self.set_direction('up')
            elif self.rect.centery <= self.start_pos[1] - 5:
                self.set_direction('down')
        if self.mode != GhostState.eaten:
            self.gg_text.rect = pg.Rect(self.rect.x, self.rect.y, 0, 0)
        if self.rotate is None:
            self.rotate = 0
        if not self.process_logic_iterator % self.deceleration_multiplier_with_rect:
            for i in range(self.acceleration_multiplier):
                self.ghosts_ai()
                self.step()
                self.animator.timer_check()
        self.process_logic_iterator += 1

    def collision_check(self, pacman: Pacman):
        return (self.two_cells_dis(self.rect.center, pacman.rect.center) < 3 and
                self.collision and not self.game.cheats_var.GHOSTS_COLLISION,
                self.mode not in [GhostState.frightened, GhostState.eaten])

    def counter(self) -> None:
        if self.work_counter:
            self.count_eat_seeds_in_home += 1

    @property
    def can_leave_home(self) -> bool:
        return (self.count_eat_seeds_in_home >= self.max_count_eat_seeds_in_home and self.work_counter) \
               or pg.time.get_ticks() - self.timer >= 4000 or self.is_can_leave_home

    def update_timer(self) -> None:
        self.timer = pg.time.get_ticks()

    def invisible(self) -> None:
        self.animator = self.invisible_anim
        self.is_invisible = True
        self.collision = False

    def visible(self) -> None:
        self.is_invisible = False
        self.collision = True

    def update_ai_timer(self):
        self.ai_timer = pg.time.get_ticks()

    def ghosts_ai(self) -> None:
        if self.in_center() and self.collision and not self.is_invisible:
            if self.move_to(self.rotate):
                self.go()
            cell = self.movement_cell(self.get_cell())
            cell[(self.rotate + 2) % 4] = False
            for rect in self.game.current_scene.cant_up_ghost_rect:
                if self.in_rect(rect):
                    cell[3] = False
            if self.mode != GhostState.frightened:
                min_dis = 10000000000000
                for i in range(4):
                    if cell[i]:
                        tmp_cell = (
                            self.get_cell()[0] + self.direction2[i][0],
                            self.get_cell()[1] + self.direction2[i][1]
                        )
                        if min_dis > self.two_cells_dis(self.love_cell, tmp_cell):
                            min_dis = self.two_cells_dis(self.love_cell, tmp_cell)
                            self.set_direction(self.direction2[i][2])
            else:
                self.set_direction(self.direction2[random.choice([i for i, v in enumerate(cell) if v])][2])

        if self.mode == GhostState.frightened:
            if pg.time.get_ticks() - self.ai_timer >= self.frightened_time-2000:
                self.animator = self.frightened_walk_anim2
            if pg.time.get_ticks() - self.ai_timer >= self.frightened_time:
                pg.event.post(pg.event.Event(EvenType.StopFearMode))
                self.update_ai_timer()
                self.deceleration_multiplier = 1
                self.animator = self.walk_anim
                self.game.sounds.pellet.stop()
                self.mode = GhostState.scatter

        if self.mode == GhostState.eaten:
            self.deceleration_multiplier = 1
            self.love_cell = (self.game.current_scene.blinky.start_pos[0] // 8,
                              (self.game.current_scene.blinky.start_pos[1]-20) // 8)
            if not self.tmp_flag1 and self.rect.center == self.game.current_scene.blinky.start_pos:
                self.collision = False
                self.set_direction('down')
                self.tmp_flag1 = True
            if self.tmp_flag1 and not self.tmp_flag2 and self.rect.y == self.game.current_scene.pinky.start_pos[1]:
                self.animator = self.walk_anim
                self.acceleration_multiplier = 1
                self.deceleration_multiplier = 2
                self.set_direction('up')
                self.tmp_flag2 = True
            if self.tmp_flag2 and self.rect.centery == self.game.current_scene.blinky.start_pos[1]:
                self.deceleration_multiplier = 1
                self.set_direction('left')
                self.mode = GhostState.scatter
                self.collision = True
                self.update_ai_timer()
                self.tmp_flag1 = False
                self.tmp_flag2 = False

    def step(self) -> None:
        if not GHOSTS_MOVING:
            super().step()

    def toggle_mode_to_frightened(self):
        if self.mode != GhostState.eaten and self.frightened_time:
            self.update_ai_timer()
            self.mode = GhostState.frightened
            self.animator = self.frightened_walk_anim1
            self.deceleration_multiplier = 2

    def toggle_mode_to_eaten(self):
        if self.mode != GhostState.eaten:
            self.game.sounds.ghost.play()
        self.mode = GhostState.eaten
        self.animator = self.eaten_walk_anim
        self.acceleration_multiplier = 2
