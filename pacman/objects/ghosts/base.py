import random
from functools import wraps

import pygame as pg
from pacman.data_core import PathManager, Dirs
from pacman.data_core.data_classes import GhostDifficult
from pacman.data_core.enums import GhostStateEnum
from pacman.misc import Animator
from pacman.misc.cell_util import CellUtil
from pacman.objects import Character, Text
from pacman.scene_manager import SceneManager


def ghost_state(state: GhostStateEnum):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self: Base = args[0]
            if self.state is state:
                return func(*args, **kwargs)

        return wrapper

    return decorator


class Base(Character):
    love_point_in_scatter_mode = (0, 0)
    seed_percent_in_home = 0
    direction2 = {0: (1, 0, 0), 1: (0, 1, 1), 2: (-1, 0, 2), 3: (0, -1, 3)}
    PEACEFULL_STATES = (GhostStateEnum.EATEN, GhostStateEnum.HIDDEN, GhostStateEnum.INDOOR)

    def __init__(self, game, loader, seed_count):
        self.__seed_count = seed_count
        self.process_logic_iterator = 0
        self.deceleration_multiplier = 1
        self.acceleration_multiplier = 1
        self.deceleration_multiplier_with_rect = 1

        # Обычные Анимация
        self.left_walk_anim = Animator(
            PathManager.get_list_path(f"{Dirs.IMAGE}/ghost/{type(self).__name__.lower()}/left", ext="png"),
            is_rotation=False,
        )
        self.right_walk_anim = Animator(
            PathManager.get_list_path(f"{Dirs.IMAGE}/ghost/{type(self).__name__.lower()}/right", ext="png"),
            is_rotation=False,
        )
        self.top_walk_anim = Animator(
            PathManager.get_list_path(f"{Dirs.IMAGE}/ghost/{type(self).__name__.lower()}/top", ext="png"),
            is_rotation=False,
        )
        self.bottom_walk_anim = Animator(
            PathManager.get_list_path(f"{Dirs.IMAGE}/ghost/{type(self).__name__.lower()}/bottom", ext="png"),
            is_rotation=False,
        )

        # Анимации страха
        self.frightened_walk_anim1 = Animator(
            PathManager.get_list_path(f"{Dirs.IMAGE}/ghost/fear1", ext="png"),
            is_rotation=False,
            aura=PathManager.get_image_path("ghost/aura_blue"),
        )
        self.frightened_walk_anim2 = Animator(
            PathManager.get_list_path(f"{Dirs.IMAGE}/ghost/fear2", ext="png"),
            is_rotation=False,
            aura=PathManager.get_image_path("ghost/aura_white"),
        )

        # Анимации съедения
        self.eaten_left_walk_anim = Animator(
            PathManager.get_list_path(f"{Dirs.IMAGE}/ghost/eaten/left", ext="png"), is_rotation=False
        )
        self.eaten_right_walk_anim = Animator(
            PathManager.get_list_path(f"{Dirs.IMAGE}/ghost/eaten/right", ext="png"), is_rotation=False
        )
        self.eaten_top_walk_anim = Animator(
            PathManager.get_list_path(f"{Dirs.IMAGE}/ghost/eaten/top", ext="png"), is_rotation=False
        )
        self.eaten_bottom_walk_anim = Animator(
            PathManager.get_list_path(f"{Dirs.IMAGE}/ghost/eaten/bottom", ext="png"),
            is_rotation=False,
        )

        self.normal_animations = [
            self.right_walk_anim,
            self.bottom_walk_anim,
            self.left_walk_anim,
            self.top_walk_anim,
        ]

        self.eaten_animations = [
            self.eaten_right_walk_anim,
            self.eaten_bottom_walk_anim,
            self.eaten_left_walk_anim,
            self.eaten_top_walk_anim,
        ]

        self.animations = self.normal_animations

        super().__init__(
            game, self.top_walk_anim, loader, PathManager.get_image_path(f"ghost/{type(self).__name__.lower()}/aura")
        )
        self.ai_timer = pg.time.get_ticks()
        self.invisible_anim = Animator(
            PathManager.get_list_path(f"{Dirs.IMAGE}/ghost/invisible", ext="png"), is_rotation=False
        )
        self.love_cell = (0, 0)
        self.state = GhostStateEnum.INDOOR
        self.gg_text = Text(" ", 10)
        self.ghost_entered_home = False

        self.blinky_start_pos = CellUtil.center_pos_from_cell(self.hero_pos["blinky"])
        self.pinky_start_pos = CellUtil.center_pos_from_cell(self.hero_pos["pinky"])
        self.diffucult_settings = self.generate_difficulty_settings()
        self.go()

        self.__states_ai = {
            GhostStateEnum.CHASE: self.chase_ai,
            GhostStateEnum.EATEN: self.eaten_ai,
            GhostStateEnum.HIDDEN: self.hidden_ai,
            GhostStateEnum.SCATTER: self.scatter_ai,
            GhostStateEnum.FRIGHTENED: self.frightened_ai,
        }

    def update(self) -> None:
        self.deceleration_multiplier_with_rect = 1
        for rect in self.level_loader.slow_ghost_rect:
            if self.in_rect(rect):
                self.deceleration_multiplier_with_rect = 2
        self.deceleration_multiplier_with_rect *= self.deceleration_multiplier

        if self.rotate is None:
            self.rotate = 0

        if self.state is not GhostStateEnum.FRIGHTENED:
            self.animator = self.animations[self.rotate]

        if not self.process_logic_iterator % self.deceleration_multiplier_with_rect:
            for _ in range(self.acceleration_multiplier):
                if self.state in self.__states_ai.keys():
                    self.__states_ai[self.state]()

        self.animator.timer_check()
        self.process_logic_iterator += 1

    def collision_check(self, rect: pg.Rect):
        return self.two_cells_dis(self.rect.center, rect.center) < 3 and self.state not in self.PEACEFULL_STATES

    def can_leave_home(self, eaten_seed) -> bool:
        percent_of_seeds = (self.__seed_count / 100) * self.seed_percent_in_home
        return eaten_seed > percent_of_seeds or pg.time.get_ticks() - self.ai_timer >= 10000

    def update_ai_timer(self):
        self.ai_timer = pg.time.get_ticks()

    # region States

    @ghost_state(GhostStateEnum.EATEN)
    def eaten_ai(self):
        self.go_to_cell(self.hero_pos["blinky"])
        self.deceleration_multiplier = 1
        self.acceleration_multiplier = 2
        if self.rect.center == self.blinky_start_pos:
            if not self.ghost_entered_home:
                self.ghost_entered_home = True
                self.set_direction("down")
                return
            self.ghost_entered_home = False
            self.acceleration_multiplier = 1
            self.state = GhostStateEnum.SCATTER
            self.set_direction(random.choice(("left", "right")))
            self.update_ai_timer()
        elif self.rect.center == self.pinky_start_pos:
            self.animations = self.normal_animations
            self.deceleration_multiplier = 2
            self.set_direction("up")

    @ghost_state(GhostStateEnum.FRIGHTENED)
    def frightened_ai(self):
        self.go_random_cell()
        if pg.time.get_ticks() - self.ai_timer >= self.diffucult_settings.frightened - 2000:
            self.animator = self.frightened_walk_anim2
        if self.check_ai_timer(self.diffucult_settings.frightened):
            SceneManager().current.score.deactivate_fear_mode()
            self.deceleration_multiplier = 1
            self.animations = self.normal_animations
            self.game.sounds.pellet.stop()
            self.state = GhostStateEnum.SCATTER

    @ghost_state(GhostStateEnum.INDOOR)
    def home_ai(self, eaten_seed):
        self.step()
        if self.can_leave_home(eaten_seed):
            return
        match self.rect.centery:
            case y if y >= self.start_pos[1] + 5:
                self.set_direction("up")
            case y if y <= self.start_pos[1] - 5:
                self.set_direction("down")

    @ghost_state(GhostStateEnum.HIDDEN)
    def hidden_ai(self):
        self.gg_text.rect = pg.Rect(self.rect.x, self.rect.y, 0, 0)
        if self.check_ai_timer(500):
            self.state = GhostStateEnum.EATEN

    @ghost_state(GhostStateEnum.SCATTER)
    def scatter_ai(self):
        raise NotImplementedError

    @ghost_state(GhostStateEnum.CHASE)
    def chase_ai(self):
        raise NotImplementedError

    # endregion

    def go_to_cell(self, cell):
        if CellUtil.in_cell_center(self.rect):
            if self.can_rotate_to(self.rotate):
                self.go()
            available_dirs = self.movement_cell(CellUtil.get_cell(self.rect))
            available_dirs[(self.rotate + 2) % 4] = False
            if not any(available_dirs):
                available_dirs[(self.rotate + 2) % 4] = True
            min_dis = float("inf")
            for i, c in enumerate(available_dirs):
                if not c:
                    continue
                cell2 = CellUtil.get_cell(self.rect)
                tmp_cell = (
                    cell2[0] + self.direction2[i][0],
                    cell2[1] + self.direction2[i][1],
                )
                diff_dis = self.two_cells_dis(cell, tmp_cell)
                if min_dis > diff_dis:
                    min_dis = diff_dis
                    self.shift_x, self.shift_y, self.rotate = self.direction2[i]
        self.step()

    def go_random_cell(self):
        if CellUtil.in_cell_center(self.rect):
            if self.can_rotate_to(self.rotate):
                self.go()
            cell = self.movement_cell(CellUtil.get_cell(self.rect))
            cell[(self.rotate + 2) % 4] = False
            if not any(cell):
                cell[(self.rotate + 2) % 4] = True
            rand = 0
            while not cell[rand]:
                rand = random.randrange(len(cell))
            self.shift_x, self.shift_y, self.rotate = self.direction2[rand]
        self.step()

    def toggle_mode_to_frightened(self):
        if self.state not in self.PEACEFULL_STATES:
            self.update_ai_timer()
            self.state = GhostStateEnum.FRIGHTENED
            self.animator = self.frightened_walk_anim1
            self.deceleration_multiplier = 2

    def toggle_to_hidden(self, score: int):
        self.gg_text.text = f"{score}"
        self.update_ai_timer()
        if self.state is not GhostStateEnum.HIDDEN:
            self.game.sounds.ghost.play()
        self.state = GhostStateEnum.HIDDEN
        self.animator = self.invisible_anim
        self.animations = self.eaten_animations

    def check_ai_timer(self, time) -> bool:
        if pg.time.get_ticks() - self.ai_timer >= time:
            self.update_ai_timer()
            return True
        return False

    def generate_difficulty_settings(self) -> GhostDifficult:
        raise NotImplementedError

    def draw(self, screen: pg.Surface) -> None:
        if self.state is GhostStateEnum.HIDDEN:
            self.gg_text.draw(screen)
            return
        super().draw(screen)
