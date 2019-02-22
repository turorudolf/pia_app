from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window


Config.set('kivy', 'keyboard_mode', 'dock')


class IntegerInput(TextInput):

    def __init__(self, **kwargs):
        super(IntegerInput, self).__init__(**kwargs)
        keyboard = Window.request_keyboard(
            self._keyboard_close, self)
        if keyboard.widget:
            vkeyboard = keyboard.widget

            vkeyboard.layout = 'numeric.json'

    def _keyboard_close(self):
        pass

    def insert_text(self, substring, from_undo=False):
        if substring.isnumeric():
            if hasattr(self, "maxdigits"):
                if len(self.text) < self.maxdigits:
                    return super(IntegerInput, self).insert_text(substring, from_undo=from_undo)
                else:
                    return super(IntegerInput, self).insert_text(substring, from_undo=from_undo)


class TestApp(App):
    def build(self):
        box = BoxLayout()
        box.add_widget(IntegerInput())
        box.add_widget(BoxLayout())
        return box


TestApp().run()
 
