import pygame as pg
from misc import ControlCheats, event_append, Sounds
from misc import LevelLoader, Font, EvenType
from misc.cheat_codes import Cheat
from misc.constants.skin_names import SkinsNames
from objects import SeedContainer, Text, Pacman, Health
from objects.characters.ghosts import *
from objects.characters.ghosts.ghost_states import GhostState
from objects.fruits import Fruit
from objects.map import Map
from objects.score import Score
from scenes.base import BaseScene


class MainScene(BaseScene):

    def start_logic(self):
        self.__load_from_map()
        self.__create_sounds()
        self.__create_start_anim()

        self.hp = Health(self.game, 3)
        self.score = Score(self.game)
        self.__seeds = SeedContainer(self.game, self.__seed_data, self.__energizer_data)

        self.__timer_reset_pacman = 0
        self.__seeds_eaten = 0
        self.__max_seeds_eaten_to_prefered_ghost = 7
        self.fruit = Fruit(self.game, self.__fruit_position)
        self.ghost_text_timer = pg.time.get_ticks()
        self.ghost_text_flag = False

    def create_title(self) -> None:
        self.objects += [*self.__get_static_text, self.__get_hud]

    @property
    def __get_static_text(self):
        scores_label_text = Text(
            self.game, f'{"MEMORY" if self.game.skins.current.name == SkinsNames.chrome else "SCORE"}',
            Font.MAIN_SCENE_SIZE, rect=pg.Rect(10, 0, 20, 20)
        )

        high_scores_label_text = Text(
            self.game, 'HIGHSCORE', Font.MAIN_SCENE_SIZE, rect=pg.Rect(130, 0, 20, 20)
        )
        return [scores_label_text, high_scores_label_text]

    @property
    def __get_hud(self):
        return Text(self.game, str(self.game.records.data[0]), Font.MAIN_SCENE_SIZE, rect=pg.Rect(130, 8, 20, 20))

    def __load_from_map(self):
        self.__loader = LevelLoader(self.game.maps.levels[self.game.maps.cur_id])
        self.__map_data = self.__loader.get_map_data()
        self.__seed_data = self.__loader.get_seed_data()
        self.__energizer_data = self.__loader.get_energizer_data()
        self.__movements_data = self.__loader.get_movements_data()
        self.__player_position = self.__loader.get_player_position()
        self.__ghost_positions = self.__loader.get_ghost_positions()
        self.__fruit_position = self.__loader.get_fruit_position()
        self.slow_ghost_rect = self.__loader.get_slow_ghost_rect()
        self.cant_up_ghost_rect = self.__loader.get_cant_up_ghost_rect()
        self.__map = Map(self.game, self.__map_data)

    def __create_sounds(self):
        self.timer = 0
        self.intro_sound = self.game.sounds.intro
        self.state_text = True

    def __create_start_anim(self):
        def creator():
            for i in ['READY', 'GO!']:
                text = Text(self.game, i, 30, font=Font.TITLE, rect=pg.Rect(20, 0, 20, 20))
                text.move_center(self.game.width // 2, self.game.height // 2)
                text.surface.set_alpha(0)
                self.objects.append(text)
                yield text
        self.text = list(creator())

    def create_objects(self) -> None:
        self.game.sounds.siren.unpause()
        hp_cheat = ControlCheats([Cheat(self.game, 'aezakmi', lambda: event_append(EvenType.HealthInc))])
        self.text[-1].surface.set_alpha(0)
        self.pacman = Pacman(self.game, self.__player_position)
        self.objects += [hp_cheat, self.__map, self.__seeds, self.fruit, self.pacman, self.hp, self.score]
        self.__create_ghost()
        self.on_reset()

    def __create_ghost(self):
        self.blinky = Blinky(self.game, self.__ghost_positions[3])
        self.pinky = Pinky(self.game, self.__ghost_positions[1])
        self.inky = Inky(self.game, self.__ghost_positions[0])
        self.clyde = Clyde(self.game, self.__ghost_positions[2])

        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

        for ghost in self.ghosts:
            ghost.set_difficult(self.game.settings.DIFFICULTY)

        # todo prefered ghost 1
        self.__not_prefered_ghosts = self.ghosts.copy()
        self.__prefered_ghost = self.pinky
        self.__count_prefered_ghost = 0

        self.objects += self.ghosts

    @property
    def movements_data(self):
        return self.__movements_data

    def additional_event_check(self, event: pg.event.Event) -> None:
        data = {
            EvenType.GameOver: lambda: self.scene_manager.reset(self.scenes.GAMEOVER(self.game, self.score)),
            EvenType.Win: lambda: self.scene_manager.reset(self.scenes.ENDGAME(self.game, self.score)),
        }
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.mixer.pause()
            self.game.scene_manager.append(self.scenes.PAUSE(self.game))
        elif event.type in data:
            data[event.type]()

    def __process_collision(self) -> None:
        self.fruit.process_collision(self.pacman)
        self.__seeds.process_collision(self.pacman)
        for ghost in self.ghosts:
            if not ghost.collision_check(self.pacman)[0]:
                continue
            if ghost.collision_check(self.pacman)[1]:
                self.__timer_reset_pacman = pg.time.get_ticks()
                if not self.pacman.dead:
                    event_append(EvenType.HealthDec)
                    self.pacman.death()
                for ghost2 in self.ghosts:
                    ghost2.invisible()
            else:
                if ghost.mode == GhostState.frightened:
                    ghost.invisible()
                    event_append(EvenType.EatGhost)
                    self.ghost_text_flag = True
                    self.ghost_text_timer = pg.time.get_ticks()
                ghost.toggle_mode_to_eaten()

    def __start_label(self) -> None:
        current_time = pg.time.get_ticks() / 1000

        if pg.time.get_ticks() - self.game.animate_timer > self.game.time_out:
            self.state_text = not self.state_text

        if self.state_text:
            if current_time - self.timer < self.intro_sound.sound.get_length() / 4 * 3:
                self.text[0].surface.set_alpha(255)
            else:
                self.text[0].surface.set_alpha(0)
                self.text[1].surface.set_alpha(255)
        else:
            if current_time - self.timer < self.intro_sound.sound.get_length() / 4 * 3:
                self.text[0].surface.set_alpha(0)
            else:
                self.text[1].surface.set_alpha(0)

    def __check_ghosts(self):
        for ghost in self.ghosts:
            if ghost.mode == GhostState.frightened:
                break
        else:
            self.game.sounds.siren.pause()
            if not self.game.sounds.pellet.get_busy():
                self.game.sounds.pellet.play()
            return
        self.game.sounds.siren.unpause()
        self.game.sounds.pellet.stop()

    def select_ghost_go(self):
        # todo prefered ghost 2
        if self.__prefered_ghost and self.__prefered_ghost.can_leave_home:
            # меняет призрака который будет выходить следующим
            self.__count_prefered_ghost += 1
            self.__not_prefered_ghosts.pop(0)
            if self.__count_prefered_ghost < len(self.ghosts):
                self.__prefered_ghost = self.ghosts[self.__count_prefered_ghost]
            else:
                self.__prefered_ghost = None

        for ghost in self.__not_prefered_ghosts:
            if ghost != self.__prefered_ghost:
                ghost.update_timer()

    def process_logic(self) -> None:
        if not self.game.sounds.intro.get_busy():
            super().process_logic()
            if not self.game.sounds.siren.get_busy():
                self.game.sounds.siren.play()
            self.__process_collision()
            if self.pacman.animator != self.pacman.dead_anim:
                self.__check_ghosts()
            if pg.time.get_ticks() - self.__timer_reset_pacman >= 3000 and self.pacman.animator.anim_finished:
                self.create_objects()
                self.__seeds_eaten = 0
                self.__max_seeds_eaten_to_prefered_ghost = 7
                for ghost in self.ghosts:
                    ghost.work_counter = False
            if self.__seeds_eaten == self.__max_seeds_eaten_to_prefered_ghost and self.__prefered_ghost is not None:
                self.__prefered_ghost.is_can_leave_home = True
                if self.__max_seeds_eaten_to_prefered_ghost == 7:
                    self.__max_seeds_eaten_to_prefered_ghost = 17
                elif self.__max_seeds_eaten_to_prefered_ghost == 17:
                    self.__max_seeds_eaten_to_prefered_ghost = 32
        else:
            self.__start_label()
            for ghost in self.ghosts:
                ghost.update_ai_timer()
                ghost.update_timer()
        self.select_ghost_go()
        if not self.ghost_text_flag:
            return
        if pg.time.get_ticks() - self.ghost_text_timer >= 1000:
            # включить призраков обратно
            for ghost in self.ghosts:
                ghost.visible()
                ghost.gg_text.text = ' '
            self.ghost_text_flag = False

    def on_reset(self) -> None:
        self.game.sounds.intro.play()
        self.game.sounds.reload_sounds()

