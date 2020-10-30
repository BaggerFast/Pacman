class BaseScene:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.objects = []
        self.create_objects()

    def create_objects(self):
        pass

    def on_activate(self):
        pass

    def process_event(self, event):
        for item in self.objects:
            item.process_event(event)
        self.additional_event_check(event)

    def additional_event_check(self, event):
        pass

    def process_logic(self):
        for item in self.objects:
            item.process_logic()
        self.additional_logic()

    def additional_logic(self):
        pass

    def process_draw(self):
        for item in self.objects:
            item.process_draw()
        self.additional_draw()

    def additional_draw(self):
        pass

    def on_deactivate(self):
        pass
