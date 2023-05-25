from functools import wraps
from random import choice, randrange

from pygame import Rect, Surface, time
from pygame.event import Event

from pacman.animator import Animator, SpriteSheetAnimator, advanced_sprite_slice, sprite_slice
from pacman.data_core import EvenType, IEventful
from pacman.data_core.data_classes import GhostDifficult
from pacman.data_core.enums import GhostStateEnum, SoundCh
from pacman.misc import CellUtil
from pacman.objects import Text
from pacman.sound import SoundController, Sounds

from ..character_base import Character


def ghost_state(state: GhostStateEnum):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self: Base = args[0]
            if self.state is state:
                return func(*args, **kwargs)

        return wrapper

    return decorator


class Base(Character, IEventful):
    love_point_in_scatter_mode = (0, 0)
    seed_percent_in_home = 0
    direction2 = {0: (1, 0, 0), 1: (0, 1, 1), 2: (-1, 0, 2), 3: (0, -1, 3)}
    PEACEFULL_STATES = (GhostStateEnum.EATEN, GhostStateEnum.HIDDEN, GhostStateEnum.INDOOR)

    def __init__(self, loader, seed_count):
        self.__seed_count = seed_count
        self.process_logic_iterator = 0
        self.deceleration_multiplier = 1
        self.acceleration_multiplier = 1
        self.deceleration_multiplier_with_rect = 1

        self.walk_anim = SpriteSheetAnimator(advanced_sprite_slice(f"ghost/{self.name}/walk", (14, 14)))
        self.eatten_anim = SpriteSheetAnimator(advanced_sprite_slice("ghost/eaten", (12, 12)))

        self.frightened_walk_anim_1 = Animator(sprite_slice("ghost/frightened_1", (14, 14)))
        self.frightened_walk_anim_2 = Animator(sprite_slice("ghost/frightened_2", (14, 14)))

        super().__init__(self.walk_anim, loader, f"ghost/{self.name}/aura")
        self.ai_timer = time.get_ticks()

        self.love_cell = (0, 0)
        self.state = GhostStateEnum.INDOOR
        self.gg_text = Text(" ", 10)
        self.ghost_entered_home = False

        self.door_room_pos = CellUtil.get_center_pos(self.hero_pos["blinky"])
        self.room_center_pos = CellUtil.get_center_pos(self.hero_pos["pinky"])
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

        if isinstance(self.animator, SpriteSheetAnimator):
            self.animator.rotate(self.rotate)
        self.animator.update()

        if not self.process_logic_iterator % self.deceleration_multiplier_with_rect:
            for _ in range(self.acceleration_multiplier):
                if self.state in self.__states_ai.keys():
                    self.__states_ai[self.state]()
        self.process_logic_iterator += 1

    def collision_check(self, rect: Rect):
        return self.two_cells_dis(self.rect.center, rect.center) < 3 and self.state not in self.PEACEFULL_STATES

    def can_leave_home(self, eaten_seed) -> bool:
        percent_of_seeds = (self.__seed_count / 100) * self.seed_percent_in_home
        return eaten_seed > percent_of_seeds or time.get_ticks() - self.ai_timer >= 10000

    def update_ai_timer(self):
        self.ai_timer = time.get_ticks()

    # region States Ai

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
        if self.check_ai_timer(500):
            self.state = GhostStateEnum.EATEN

    @ghost_state(GhostStateEnum.EATEN)
    def eaten_ai(self):
        self.go_to_cell(self.hero_pos["blinky"])
        self.deceleration_multiplier = 1
        self.acceleration_multiplier = 2
        match self.rect.center:
            case self.door_room_pos if not self.ghost_entered_home:
                self.ghost_entered_home = True
                self.set_direction("down")
            case self.door_room_pos:
                self.ghost_entered_home = False
                self.acceleration_multiplier = 1
                self.state = GhostStateEnum.SCATTER
                self.set_direction(choice(("left", "right")))
                self.update_ai_timer()
            case self.room_center_pos:
                self.animator = self.walk_anim
                self.deceleration_multiplier = 2
                self.set_direction("up")

    @ghost_state(GhostStateEnum.FRIGHTENED)
    def frightened_ai(self):
        self.go_to_random_cell()
        if self.check_ai_timer(self.diffucult_settings.frightened):
            self.deceleration_multiplier = 1
            self.state = GhostStateEnum.SCATTER
            self.animator = self.walk_anim
        elif time.get_ticks() - self.ai_timer >= self.diffucult_settings.frightened - 2000:
            self.animator = self.frightened_walk_anim_2

    @ghost_state(GhostStateEnum.CHASE)
    def chase_ai(self):
        raise NotImplementedError

    @ghost_state(GhostStateEnum.SCATTER)
    def scatter_ai(self):
        raise NotImplementedError

    # endregion

    def go_to_cell(self, cell):
        if CellUtil.is_in_cell_center(self.rect):
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

    def go_to_random_cell(self):
        if CellUtil.is_in_cell_center(self.rect):
            if self.can_rotate_to(self.rotate):
                self.go()
            cell = self.movement_cell(CellUtil.get_cell(self.rect))
            cell[(self.rotate + 2) % 4] = False
            if not any(cell):
                cell[(self.rotate + 2) % 4] = True
            rand = 0
            while not cell[rand]:
                rand = randrange(len(cell))
            self.shift_x, self.shift_y, self.rotate = self.direction2[rand]
        self.step()

    def toggle_mode_to_frightened(self):
        if self.state not in self.PEACEFULL_STATES:
            self.update_ai_timer()
            self.state = GhostStateEnum.FRIGHTENED
            self.animator = self.frightened_walk_anim_1
            self.deceleration_multiplier = 2

    def toggle_to_hidden(self, score: int):
        self.gg_text.text = f"{score}"
        self.update_ai_timer()
        SoundController.reset_play(SoundCh.PLAYER, Sounds.GHOST)
        self.state = GhostStateEnum.HIDDEN
        self.animator = self.eatten_anim

    def check_ai_timer(self, timer) -> bool:
        if time.get_ticks() - self.ai_timer >= timer:
            self.update_ai_timer()
            return True
        return False

    def generate_difficulty_settings(self) -> GhostDifficult:
        raise NotImplementedError

    def draw(self, screen: Surface) -> None:
        if self.state is GhostStateEnum.HIDDEN:
            self.gg_text.rect = self.rect
            self.gg_text.draw(screen)
            return
        super().draw(screen)

    def event_handler(self, event: Event):
        if event.type == EvenType.GHOST_FRIGHTENED:
            self.toggle_mode_to_frightened()

    @property
    def name(self) -> str:
        return type(self).__name__.lower()
