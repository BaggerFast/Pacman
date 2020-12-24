import pygame as pg
from misc import ControlCheats
from misc import LevelLoader, Font, get_path, Health
from objects import SeedContainer, Map, ImageObject, Text, Pacman
from objects.fruits import Fruit
from objects.ghosts import *
from scenes import base


class Scene(base.Scene):
    def create_static_objects(self):
        self.__load_from_map()
        self.__create_sounds()
        self.__create_static_text()
        self.__create_start_anim()
        self.__create_hud()
        self.__create_health()
        self.__pre_init()
        self.create_objects()

    def __pre_init(self):
        self.__timer_reset_pacman = 0
        self.__seeds_eaten = 0
        self.__max_seeds_eaten_to_prefered_ghost = 7
        self.__work_ghost_counters = True
        self.__first_run_ghost = True
        self.fruit = Fruit(self.game, self.__fruit_position)
        self.ghost_text_timer = pg.time.get_ticks()
        self.ghost_text_flag = False
        self.is_active = False

    def __create_health(self):
        self.hp = Health(3, 4)
        self.__hp_hud = []
        self.__prepare_lives_meter()

    def __create_static_text(self):
        self.__scores_label_text = Text(
            self.game, 'MEMORY' if self.game.skins.current.name == "chrome" else 'SCORE', Font.MAIN_SCENE_SIZE,
            rect=pg.Rect(10, 0, 20, 20)
        )

        self.__high_scores_label_text = Text(
            self.game, 'HIGHSCORE', Font.MAIN_SCENE_SIZE, rect=pg.Rect(130, 0, 20, 20)
        )
        self.static_objects.append(self.__scores_label_text)
        self.static_objects.append(self.__high_scores_label_text)

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

    def __prepare_lives_meter(self) -> None:
        self.__hp_hud = []
        for i in range(int(self.hp) - 1):
            hp_image = ImageObject(self.game,
                                   get_path('1', 'png', 'images', 'pacman', self.game.skins.current.name, 'walk'),
                                   (5 + i * 20, 270))
            hp_image.image = pg.transform.flip(hp_image.image, True, False)
            self.__hp_hud.append(hp_image)

    def __create_sounds(self):
        self.timer = 0
        self.intro_sound = self.game.sounds.intro

    def __create_start_anim(self):
        self.text = ['READY', 'GO!']
        for i in range(2):
            self.text[i] = Text(self.game, self.text[i], 30, font=Font.TITLE, rect=pg.Rect(20, 0, 20, 20))
            self.text[i].move_center(self.game.width // 2, self.game.height // 2)
            self.text[i].surface.set_alpha(0)
            self.static_objects.append(self.text[i])
        self.state_text = 1

    def create_objects(self) -> None:
        self.objects = []
        self.game.sounds.siren.unpause()

        self.hp_cheat = ControlCheats(self.game, [['aezakmi', self.add_hp]])
        self.objects.append(self.hp_cheat)

        self.text[len(self.text) - 1].surface.set_alpha(0)
        self.__create_map()
        self.objects.append(self.fruit)
        self.__create_ghost()
        self.pacman = Pacman(self.game, self.__player_position)
        self.objects.append(self.pacman)

    def add_hp(self):
        self.hp += 1

    def __create_map(self):
        self.__seeds = SeedContainer(self.game, self.__seed_data, self.__energizer_data)
        self.objects.append(self.__map)
        self.objects.append(self.__seeds)

    def __create_ghost(self):
        if self.game.settings.DIFFICULTY == 0:
            self.blinky = Blinky(self.game, self.__ghost_positions[3], 8000, 20000, 7000)
            self.pinky = Pinky(self.game, self.__ghost_positions[1], 8000, 20000, 7000)
            self.inky = Inky(self.game, self.__ghost_positions[0], 8000, 20000, 5000)
            self.clyde = Clyde(self.game, self.__ghost_positions[2], 8000, 0, 0)
        elif self.game.settings.DIFFICULTY == 1:
            self.blinky = Blinky(self.game, self.__ghost_positions[3], 4000, 40000, 5000)
            self.pinky = Pinky(self.game, self.__ghost_positions[1], 4000, 40000, 5000)
            self.inky = Inky(self.game, self.__ghost_positions[0], 4000, 40000, 3000)
            self.clyde = Clyde(self.game, self.__ghost_positions[2], 4000, 0, 0)
        elif self.game.settings.DIFFICULTY == 2:
            self.blinky = Blinky(self.game, self.__ghost_positions[3], 2000, 80000, 3000)
            self.pinky = Pinky(self.game, self.__ghost_positions[1], 2000, 80000, 3000)
            self.inky = Inky(self.game, self.__ghost_positions[0], 2000, 80000, 1000)
            self.clyde = Clyde(self.game, self.__ghost_positions[2], 2000, 0, 0)

        self.ghosts = [
            self.blinky,
            self.pinky,
            self.inky,
            self.clyde
        ]

        self.__not_prefered_ghosts = self.ghosts.copy()
        self.__prefered_ghost = self.pinky
        self.__count_prefered_ghost = 0

        for ghost in self.ghosts:
            self.objects.append(ghost)
            self.objects.append(ghost.gg_text)

    def __create_hud(self):
        self.__high_scores_value_text = Text(self.game,
                                             str(self.game.records.data[-1]),
                                             Font.MAIN_SCENE_SIZE,
                                             rect=pg.Rect(130, 8, 20, 20))
        self.static_objects.append(self.__high_scores_value_text)

        self.__scores_value_text = Text(
            self.game,
            str(self.game.score) + " Mb" if self.game.skins.current.name == "chrome" else str(self.game.score),
            Font.MAIN_SCENE_SIZE,
            rect=pg.Rect(10, 8, 20, 20))
        self.static_objects.append(self.__scores_value_text)

    @property
    def movements_data(self):
        return self.__movements_data

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.mixer.pause()
            self.template = self.screen.copy()
            self.game.timer = pg.time.get_ticks() / 1000
            self.game.scenes.PAUSE()

    def __change_prefered_ghost(self) -> None:
        self.__count_prefered_ghost += 1
        self.__not_prefered_ghosts.pop(0)
        if self.__count_prefered_ghost < 4:
            self.__prefered_ghost = self.ghosts[self.__count_prefered_ghost]
        else:
            self.__prefered_ghost = None
            self.__count_prefered_ghost = 0

    def __process_collision(self) -> None:
        self.fruit.process_collision(self.pacman)
        seed_eaten = self.__seeds.process_collision(self.pacman)
        for ghost in self.ghosts:
            if ghost.collision_check(self.pacman)[0]:
                if ghost.collision_check(self.pacman)[1]:
                    self.__timer_reset_pacman = pg.time.get_ticks()
                    if not self.pacman.dead:
                        self.pacman.death()
                        self.__prepare_lives_meter()
                    for ghost2 in self.ghosts:
                        ghost2.invisible()
                else:
                    if ghost.mode == 'Frightened':
                        ghost.gg_text.text = str((200 * self.game.difficulty ** 2) * 2 ** self.game.score.fear_count)
                        ghost.invisible()
                        self.game.score.eat_ghost()
                        self.ghost_text_flag = True
                        self.ghost_text_timer = pg.time.get_ticks()
                    ghost.toggle_mode_to_eaten()

        if seed_eaten == 1:
            if self.__prefered_ghost is not None and self.__work_ghost_counters:
                self.__prefered_ghost.counter()
                self.__prefered_ghost.update_timer()
            elif not self.__work_ghost_counters and self.__prefered_ghost is not None:
                self.__seeds_eaten += 1
                self.__prefered_ghost.update_timer()
        elif seed_eaten == 2:
            self.game.score.activate_fear_mode()
            for ghost in self.ghosts:
                ghost.toggle_mode_to_frightened()

    def __start_label(self) -> None:
        current_time = pg.time.get_ticks() / 1000
        if pg.time.get_ticks() - self.game.animate_timer > self.game.time_out:
            self.state_text *= -1
        if self.state_text == 1:
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

    def __play_music(self):
        if not self.game.sounds.siren.get_busy():
            self.game.sounds.siren.play()

    def __check_ghosts(self):
        flag = False
        for ghost in self.ghosts:
            if ghost.mode == 'Frightened':
                flag = True
        if flag:
            self.game.sounds.siren.pause()
            if not self.game.sounds.pellet.get_busy():
                self.game.sounds.pellet.play()
        else:
            self.game.sounds.siren.unpause()
            self.game.sounds.pellet.stop()

    def process_logic(self) -> None:
        if not self.game.sounds.intro.get_busy():
            self.text[0].surface.set_alpha(0)
            self.text[1].surface.set_alpha(0)
            if self.pacman.dead_anim.anim_finished and int(self.hp) < 1 \
                and not self.game.sounds.pacman.get_busy():
                self.template = self.screen.copy()
                self.game.timer = pg.time.get_ticks() / 1000
                self.game.scenes.set(self.game.scenes.GAMEOVER)
            super(Scene, self).process_logic()
            self.__play_music()
            self.__process_collision()
            if self.pacman.animator != self.pacman.dead_anim:
                self.__check_ghosts()
            self.text[0].surface.set_alpha(0)
            self.text[1].surface.set_alpha(0)
            if pg.time.get_ticks() - self.__timer_reset_pacman >= 3000 and self.pacman.animator.anim_finished:
                self.create_objects()
                self.__seeds_eaten = 0
                self.__work_ghost_counters = False
                self.__max_seeds_eaten_to_prefered_ghost = 7
                for ghost in self.ghosts:
                    ghost.work_counter = False
            if self.__seeds_eaten == self.__max_seeds_eaten_to_prefered_ghost and self.__prefered_ghost is not None:
                self.__prefered_ghost.is_can_leave_home = True
                if self.__max_seeds_eaten_to_prefered_ghost == 7:
                    self.__max_seeds_eaten_to_prefered_ghost = 17
                elif self.__max_seeds_eaten_to_prefered_ghost == 17:
                    self.__max_seeds_eaten_to_prefered_ghost = 32
            if self.__seeds.is_field_empty():
                self.template = self.screen.copy()
                self.game.timer = pg.time.get_ticks() / 1000
                self.game.scenes.ENDGAME()
        else:
            self.__start_label()
            for ghost in self.ghosts:
                ghost.update_ai_timer()
                ghost.update_timer()
        if self.__prefered_ghost is not None and self.__prefered_ghost.can_leave_home():
            self.__change_prefered_ghost()
        if self.__prefered_ghost is not None and self.__prefered_ghost.can_leave_home():
            self.__change_prefered_ghost()
        for ghost in self.__not_prefered_ghosts:
            if ghost != self.__prefered_ghost:
                ghost.update_timer()
        if self.ghost_text_flag:
            if pg.time.get_ticks() - self.ghost_text_timer >= 1000:
                for ghost in self.ghosts:
                    ghost.visible()
                    ghost.gg_text.text = ' '
                self.ghost_text_flag = False

    def additional_draw(self) -> None:
        super().additional_draw()
        for hp in self.__hp_hud:
            hp.process_draw()

    def additional_logic(self) -> None:
        self.__scores_label_text.text = "MEMORY" if self.game.skins.current.name == "chrome" else "SCORE"
        self.__scores_value_text.text = str(
            self.game.score) + " Mb" if self.game.skins.current.name == "chrome" else str(
            self.game.score)
        self.__prepare_lives_meter()

    def on_activate(self) -> None:
        self.is_active = True
        self.game.sounds.intro.unpause()
        self.template = self.screen
        if self.pacman.animator != self.pacman.dead_anim:
            self.game.sounds.siren.unpause()
        for ghost in self.ghosts:
            if ghost.mode == "Frightened":
                if self.game.sounds.pellet.get_busy():
                    self.game.sounds.pellet.play()
                    break
        if self.pacman.animator == self.pacman.dead_anim:
            self.game.sounds.pacman.unpause()

    def on_deactivate(self) -> None:
        self.is_active = False

    def on_reset(self) -> None:
        pg.mixer.stop()
        self.game.timer = pg.time.get_ticks() // 1000
        self.game.sounds.reload_sounds(self.game)
        self.game.score.reset()
        self.game.scenes.MAIN.recreate()
        self.game.sounds.intro.play()

    def Continue(self):
        self.game.scenes.set(self)

    def __call__(self, *args, **kwargs):
        self.game.scenes.set(self,reset=True,loading=True)
