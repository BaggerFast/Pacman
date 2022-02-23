import random
from abc import ABC
from typing import Tuple

import pygame as pg

from misc import Animator, EvenType, event_append
from misc.animator import SpriteSheetAnimator
from misc.interfaces.object_interfaces import IEventful
from misc.path import get_image_path
from misc.sprite_sheet import SpriteSheet
from objects import Pacman, Text
from objects.characters.character_base import Character
from objects.characters.ghosts.ghost_states import GhostState


class Base(Character, IEventful, ABC):
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
           SpriteSheet(get_image_path(f'ghost/{type(self).__name__.lower()}/walk.png'), (14, 14))
        )
        self.frightened_walk_anim1 = Animator(
           SpriteSheet(get_image_path('ghost/fear1.png'), (14, 14))[0], aura=get_image_path('ghost/aura_blue.png')
        )
        self.frightened_walk_anim2 = Animator(
           SpriteSheet(get_image_path('ghost/fear2.png'), (14, 14))[0], aura=get_image_path('ghost/aura_white.png')
        )

        self.eaten_walk_anim = SpriteSheetAnimator(SpriteSheet(get_image_path('ghost/eaten.png'), (12, 14)))

        aura_path = get_image_path(f'ghost/{type(self).__name__.lower()}/aura.png')
        Character.__init__(self, game, self.walk_anim, start_pos, aura_path)

        self.is_can_leave_home = False
        self.count_eat_seeds_in_home = 0

        self.collision = False

        self.timer = pg.time.get_ticks()
        self.ai_timer = pg.time.get_ticks()
        self.love_cell = (0, 0)

        self.is_invisible = False
        self.is_in_home = True

        self.work_counter = True

        self.mode = GhostState.scatter

        self.gg_text = Text(
            self.game, '100',
            10, pg.Rect(0, 0, 0, 0),
        )

        self.tmp_flag1 = False
        self.tmp_flag2 = False

        self.old_timer = pg.time.get_ticks()
        self.old_ai_timer = pg.time.get_ticks()

    def behaviour_in_the_house(self):
        # если он внутри дома и не может выйти то бегать вверх вниз
        self.go()
        if self.rect.centery >= self.start_pos[1] + 5:
            self.set_direction('up')
        elif self.rect.centery <= self.start_pos[1] - 5:
            self.set_direction('down')

    def slow_corridor(self):
        for rect in self.game.scene_manager.current.slow_ghost_rect:
            if self.in_rect(rect):
                self.deceleration_multiplier_with_rect = 2

    def process_logic(self) -> None:
        self.deceleration_multiplier_with_rect = 1
        self.slow_corridor()
        self.deceleration_multiplier_with_rect *= self.deceleration_multiplier

        if self.is_in_home and not self.can_leave_home:
            self.behaviour_in_the_house()

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
        self.is_invisible = True
        self.collision = False

    def visible(self) -> None:
        self.is_invisible = False
        self.collision = True

    def update_ai_timer(self):
        self.ai_timer = pg.time.get_ticks()

    def frightened_ai(self):
        if pg.time.get_ticks() - self.ai_timer >= self.frightened_time - 2000:
            self.animator = self.frightened_walk_anim2
        if pg.time.get_ticks() - self.ai_timer >= self.frightened_time:
            event_append(EvenType.StopFearMode)
            self.update_ai_timer()
            self.deceleration_multiplier = 1
            self.animator = self.walk_anim
            self.game.sounds.pellet.stop()
            self.mode = GhostState.scatter

    def eaten_ai(self):
        self.deceleration_multiplier = 1
        self.love_cell = (self.game.current_scene.blinky.start_pos[0] // 8,
                          (self.game.current_scene.blinky.start_pos[1] - 20) // 8)

        if not self.tmp_flag1 and self.rect.center == self.game.current_scene.blinky.start_pos:
            self.set_direction('down')
            self.collision = False
            self.tmp_flag1 = True

        if self.tmp_flag1 and not self.tmp_flag2 and self.rect.y == self.game.current_scene.pinky.start_pos[1]:
            self.set_direction('up')
            self.animator = self.walk_anim
            self.acceleration_multiplier = 1
            self.deceleration_multiplier = 2
            self.tmp_flag2 = True

        if self.tmp_flag2 and self.rect.centery == self.game.current_scene.blinky.start_pos[1]:
            self.set_direction('left')
            self.mode = GhostState.scatter

            self.deceleration_multiplier = 1
            self.collision = True
            self.update_ai_timer()
            self.tmp_flag1 = False
            self.tmp_flag2 = False

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

        ghost_states = {
            GhostState.frightened: self.frightened_ai,
            GhostState.eaten: self.eaten_ai,
        }
        if self.mode in ghost_states:
            ghost_states[self.mode]()

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

    def process_event(self, event: pg.event.Event) -> None:
        events = {
            EvenType.FrightenedMode: self.toggle_mode_to_frightened
        }
        if event.type in events:
            events[event.type]()

    def process_draw(self) -> None:
        if self.mode == GhostState.eaten:
            self.gg_text.text = f'{200 * self.game.difficulty ** 2}' # * 2 ** self.game.score.fear_count2
            self.gg_text.process_draw()
        if not self.is_invisible:
            super().process_draw()

    def set_power(self, frightened_time: int, chase_time: int, scatter_time: int):
        self.frightened_time = frightened_time
        self.chase_time = chase_time
        self.scatter_time = scatter_time
