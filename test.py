from kivy.config import Config
Config.set('graphics', 'maxfps', '60')
Config.write()

from kivy.app import App
from kivy.core.window import Window
from block import Block
from field import Field
from random import randint

Window.size = 1440, 890


class MyField(Field):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for _ in range(100):
            self.add_widget(Block(vel_x=randint(50, 100),
                                  vel_y=randint(50, 100),
                                  size_hint=(None, None),
                                  size=(35, 35),
                                  x=randint(0, Window.width),
                                  y=randint(0, Window.height),
                                  rigid=False))


class TestApp(App):
    pass


TestApp().run()
