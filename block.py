from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import BooleanProperty, DictProperty, ListProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector

Builder.load_file("block.kv")


# directional constants
COLLIDED = 0
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4
HORIZONTAL = (RIGHT, LEFT)
VERTICAL = (UP, DOWN)


class Block(Widget):

    vel_x = NumericProperty()
    vel_y = NumericProperty()

    force_x = DictProperty()
    force_y = DictProperty()

    mass = NumericProperty(1)
    rigid = BooleanProperty()
    bounce = NumericProperty(.8)
    friction = NumericProperty(.05)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.rigid:
            self.update_schedule = Clock.schedule_interval(self._update, 0)

    @property
    def acc_x(self):
        return sum(self.force_x.values()) / self.mass

    @property
    def acc_y(self):
        return sum(self.force_y.values()) / self.mass

    def on_rigid(self, instance, value):
        if value:
            self.update_schedule.cancel()
        else:
            self.update_schedule = Clock.schedule_interval(self._update, 0)

    def direction_widget(self, wid):
        if self.collide_widget(wid):
            return COLLIDED
        elif self.x > wid.right:
            return RIGHT
        elif self.right < wid.x:
            return LEFT
        elif self.y > wid.top:
            return UP
        elif self.top < wid.y:
            return DOWN

    def _update(self, dt):

        self.vel_x += self.acc_x * dt
        self.vel_y += self.acc_y * dt

        move_x = self.vel_x * dt
        move_y = self.vel_y * dt

        self.x += move_x
        self.y += move_y

        # reset force
        self.force_x.clear()
        self.force_y.clear()

        for other in self.parent.children:
            if other is not self and self.collide_widget(other):

                move_vector = Vector(move_x, move_y)
                move_normal = move_vector.normalize()
                move_x_normal, move_y_normal = move_normal

                # gradually move back to position where it is not collided with other
                while self.collide_widget(other):
                    self.x -= move_x_normal
                    self.y -= move_y_normal

                # recalculate velocity upon collision
                direction = self.direction_widget(other)
                if direction in HORIZONTAL:
                    self.vel_x = -self.vel_x * self.bounce
                    self.vel_y = self.vel_y * (1 - self.friction)
                elif direction in VERTICAL:
                    self.vel_x = self.vel_x * (1 - self.friction)
                    self.vel_y = -self.vel_y * self.bounce
                    if direction is DOWN:
                        if "normal" not in self.force_y:
                            self.force_y["normal"] = -self.force_y.get("gravity", 0)

                # prevent glitch when a block is stuck between multiple blocks
                break  # todo: a better solution for minor trembling


Factory.register("Block", Block)
