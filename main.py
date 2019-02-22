from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import serialize


class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 4
        
        self.wineBtn = Button(text="Wine",font_size=30, background_color=(250, 0, 0, 0.32))
        self.wineBtn.bind(on_press=self.wineCallback)
        self.add_widget(self.wineBtn)
        self.add_widget(Button(text="cider"))
        self.add_widget(Button(text="champagne"))
        self.add_widget(Button(text="spirit"))
        self.saveBtn = Button(text="Save",font_size=30)
        self.saveBtn.bind(on_press=self.callback)
        self.add_widget(self.saveBtn)
        self.showBtn = Button(text="Show",font_size=30)
        self.showBtn.bind(on_press=self.showCallback)
        self.add_widget(self.showBtn)
        self.pkl_path = "data/kivy1.pkl"
        self.wine = 0
        
    def saveData(self):
        self.data = {'wine':self.wine}
    def callback(self,instance):
        print('The button <%s> is being pressed' % instance.text)
        self.saveData()
    def showCallback(self,instance):
        print('wine:',self.wine)
    def wineCallback(self,instance):
		print("Wine = ", self.wine)
		self.plusWine = TextInput(multiline=False)
		self.plusWine.bind(on_text_validate=self.on_enter)
		self.add_widget(self.plusWine)
		print self.plusWine
    def on_enter(self,instance):
		print('User pressed enter in', instance)
		print('%s' % instance.text)
		self.winePlus = float(instance.text)
		self.wine += self.winePlus
		instance.text = ''
    def calculate(self):
		# total + this month + expected this year
		self.totalAlc = self.wine * 0.12

class MyApp(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
