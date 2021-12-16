def scenes_available(func):
    def wrapped(*args, **kwargs):
        self = args[0]
        if not self.is_empty:
            return func(*args, **kwargs)
    return wrapped


class SceneManager:

    def __init__(self, game):
        self.scenes = []
        self.game = game

    @property
    @scenes_available
    def current(self):
        return self.scenes[-1]

    @property
    def previous(self):
        if len(self.scenes) > 1:
            return self.scenes[-2]

    @property
    def is_empty(self):
        return len(self.scenes) <= 0

    @scenes_available
    def enter_scene(self):
        self.scenes[-1].on_enter()

    @scenes_available
    def exit_scene(self):
        self.scenes[-1].on_exit()

    @scenes_available
    def process_logic(self) -> None:
        self.scenes[-1].process_logic()

    @scenes_available
    def process_event(self, event) -> None:
        self.scenes[-1].process_event(event)

    @scenes_available
    def process_draw(self):
        self.scenes[-1].process_draw()

    def push(self, scene):
        self.exit_scene()
        self.scenes.append(scene)
        self.enter_scene()

    def pop(self):
        self.exit_scene()
        self.scenes.pop()
        self.enter_scene()

    def set(self, scene):
        self.scenes = []
        self.push(scene)
