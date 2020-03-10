from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.factory import Factory

GRAVITATIONAL_CONST = -98


class Field(RelativeLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self._update, 0)

    def _update(self, dt):
        for child in self.children:
            if "gravity" not in child.force_y:
                child.force_y["gravity"] = GRAVITATIONAL_CONST


Factory.register("Field", Field)
