import random
import pygame as pg
from pacman.data_core import PathManager, Dirs
from pacman.data_core.enums import GhostStateEnum
from pacman.misc import Animator, DISABLE_GHOSTS_MOVING, DISABLE_GHOSTS_COLLISION
from pacman.misc.cell_util import CellUtil
from pacman.objects import Character, Text
from pacman.scene_manager import SceneManager


class Base(Character):
    love_point_in_scatter_mode = (0, 0)
    seed_percent_in_home = 0
    direction2 = {0: (1, 0, 0), 1: (0, 1, 1), 2: (-1, 0, 2), 3: (0, -1, 3)}

    def __init__(self, game, loader, seed_count, frightened_time, chase_time, scatter_time):
        self.__seed_count = seed_count
        self.process_logic_iterator = 0
        self.deceleration_multiplier = 1
        self.acceleration_multiplier = 1
        self.deceleration_multiplier_with_rect = 1

        self.frightened_time = frightened_time
        self.chase_time = chase_time
        self.scatter_time = scatter_time

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
        self.collision = False
        self.timer = pg.time.get_ticks()
        self.ai_timer = pg.time.get_ticks()
        self.invisible_anim = Animator(
            PathManager.get_list_path(f"{Dirs.IMAGE}/ghost/invisible", ext="png"), is_rotation=False
        )
        self.love_cell = (0, 0)
        self.is_invisible = False
        self.is_in_home = True
        self.work_counter = True
        self.set_direction("left")
        self.state = GhostStateEnum.SCATTER
        self.gg_text = Text(" ", 10)

        # Временное решение
        self.tmp_flag1 = False
        self.tmp_flag2 = False

        self.blinky_start_pos = CellUtil.center_pos_from_cell(self.hero_pos["blinky"])
        self.pinky_start_pos = CellUtil.center_pos_from_cell(self.hero_pos["pinky"])

        self.text_timer = 0

    def update(self) -> None:
        if self.is_invisible:
            return
        self.deceleration_multiplier_with_rect = 1
        for rect in self.level_loader.slow_ghost_rect:
            if self.in_rect(rect):
                self.deceleration_multiplier_with_rect = 2
        self.deceleration_multiplier_with_rect *= self.deceleration_multiplier
        if self.state is not GhostStateEnum.EATEN:
            self.gg_text.rect = pg.Rect(self.rect.x, self.rect.y, 0, 0)
        if self.rotate is None:
            self.rotate = 0
        if not self.is_invisible and self.state is not GhostStateEnum.FRIGHTENED:
            self.animator = self.animations[self.rotate]
        if not self.process_logic_iterator % self.deceleration_multiplier_with_rect:
            for _ in range(self.acceleration_multiplier):
                self.ghosts_ai()
                self.step()
        self.animator.timer_check()
        self.process_logic_iterator += 1

    def collision_check(self, rect: pg.Rect):
        return self.two_cells_dis(self.rect.center, rect.center) < 3 and self.collision and \
            (not DISABLE_GHOSTS_COLLISION and self.state is not GhostStateEnum.EATEN)

    def can_leave_home(self, eaten_seed) -> bool:
        return (
            eaten_seed > (self.__seed_count / 100) * self.seed_percent_in_home
            or pg.time.get_ticks() - self.timer >= 10000
        )

    def home_ai(self, eaten_seed):
        if self.is_in_home and not self.can_leave_home(eaten_seed):
            self.go()
            if self.rect.centery >= self.start_pos[1] + 5:
                self.set_direction("up")
            elif self.rect.centery <= self.start_pos[1] - 5:
                self.set_direction("down")

    def update_timer(self) -> None:
        self.timer = pg.time.get_ticks()

    def update_ai_timer(self):
        self.ai_timer = pg.time.get_ticks()

    def invisible(self) -> None:
        self.animator = self.invisible_anim
        # self.state = GhostStateEnum.HIDDEN
        self.is_invisible = True
        self.collision = False

    def visible(self) -> None:
        if pg.time.get_ticks() - self.text_timer >= 500:
            self.gg_text.text = f" "
            self.is_invisible = False
            self.collision = True

    def eaten_ai(self):
        if self.state is not GhostStateEnum.EATEN:
            return
        self.deceleration_multiplier = 1
        self.love_cell = tuple(self.hero_pos["blinky"])
        if not self.tmp_flag1 and self.rect.center == self.blinky_start_pos:
            self.collision = False
            self.set_direction("down")
            self.tmp_flag1 = True
        if self.tmp_flag1 and not self.tmp_flag2 and self.rect.y == self.pinky_start_pos[1]:
            self.animations = self.normal_animations
            self.acceleration_multiplier = 1
            self.deceleration_multiplier = 2
            self.set_direction("up")
            self.tmp_flag2 = True
        if self.tmp_flag2 and self.rect.centery == self.blinky_start_pos[1]:
            self.deceleration_multiplier = 1
            self.set_direction("left")
            self.state = GhostStateEnum.SCATTER
            self.collision = True
            self.update_ai_timer()
            self.tmp_flag1 = False
            self.tmp_flag2 = False

    def frightened_ai(self):
        if self.state is not GhostStateEnum.FRIGHTENED:
            return
        if pg.time.get_ticks() - self.ai_timer >= self.frightened_time - 2000:
            self.animator = self.frightened_walk_anim2
        if pg.time.get_ticks() - self.ai_timer >= self.frightened_time:
            SceneManager().current.score.deactivate_fear_mode()
            self.update_ai_timer()
            self.deceleration_multiplier = 1
            self.animations = self.normal_animations
            self.game.sounds.pellet.stop()
            self.state = GhostStateEnum.SCATTER

    def ghosts_ai(self) -> None:
        if CellUtil.in_cell_center(self.rect) and self.collision:
            if self.move_to(self.rotate):
                self.go()
            cell = self.movement_cell(CellUtil.get_cell(self.rect))
            cell[(self.rotate + 2) % 4] = False
            if not any(cell):
                cell[(self.rotate + 2) % 4] = True

            if self.state is not GhostStateEnum.FRIGHTENED:
                min_dis = float("inf")
                for i, c in enumerate(cell):
                    if not c:
                        continue
                    cell2 = CellUtil.get_cell(self.rect)
                    tmp_cell = (
                        cell2[0] + self.direction2[i][0],
                        cell2[1] + self.direction2[i][1],
                    )
                    diff_dis = self.two_cells_dis(self.love_cell, tmp_cell)
                    if min_dis > diff_dis:
                        min_dis = diff_dis
                        self.shift_x, self.shift_y, self.rotate = self.direction2[i]
            else:
                rand = 0
                while not cell[rand]:
                    rand = random.randrange(len(cell))
                self.shift_x, self.shift_y, self.rotate = self.direction2[rand]
        self.eaten_ai()
        self.frightened_ai()

    def step(self) -> None:
        if not DISABLE_GHOSTS_MOVING:
            super().step()

    def toggle_mode_to_frightened(self):
        if self.state is not GhostStateEnum.EATEN and self.frightened_time != 0:
            self.update_ai_timer()
            self.state = GhostStateEnum.FRIGHTENED
            self.animator = self.frightened_walk_anim1
            self.deceleration_multiplier = 2

    def toggle_mode_to_eaten(self, score: int):
        self.gg_text.text = f"{score}"
        self.text_timer = pg.time.get_ticks()
        self.invisible()
        if self.state is not GhostStateEnum.EATEN:
            self.game.sounds.ghost.play()
        self.state = GhostStateEnum.EATEN
        self.animations = self.eaten_animations
        self.acceleration_multiplier = 2
