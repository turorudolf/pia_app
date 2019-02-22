from kivy.app import App
#from kivy.app import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from functools import partial
from kivy.storage.dictstore import DictStore
import re
from datetime import date
import calendar
from kivy.config import Config
from kivy.core.window import Window



Config.set('kivy', 'keyboard_mode', 'dock')


class MainScreen(BoxLayout):
	def __init__(self, **kwargs):
		super(MainScreen, self).__init__(orientation='vertical')
		try:
			self.loadData()
			#self.resetData()
			#self.initData()
		except KeyError as err:
			self.resetData("error: {}".format(repr(err)) )
			print ("KIVY, 2, error: {}".format(repr(err)))
		print ("startDate=",self.startDate_str)
		#print self.wsum
		if self.startDate_str == '':
			print "startDate empty! setting it to today"
			self.startDate = date.today()
			self.startDate_str = date.today().strftime('%Y-%m-%d')
			self.store = DictStore(filename='app_data/data')
			self.store.put('startDate', val=self.startDate_str)
		else:
			yr,m,d = map(int,self.startDate_str.split("-"))
			self.startDate = date(yr,m,d) # date object
		self.alc_cont = {'beer':0.05, 'wine':0.12, 'cider':0.04, 'spirit':0.4, 'champagne':0.12}
		
		# DRINK BUTTONS 
		self.btn1 = Button(text='Wine', font_size='63sp', background_color=(3,0.1,.1,.3))
		self.btn1.bind(on_press=partial(self.addDrink, alc_type="wine"))
		self.add_widget(self.btn1)
		
		self.btn2 = Button(text='Beer', font_size='63sp', background_color=(2,20,2,.8))
		self.btn2.bind(on_press=partial(self.addDrink, alc_type="beer"))
		self.add_widget(self.btn2)
		
		self.btn3 = Button(text='Cider', font_size='63sp', background_color=(240,230,140,.8))
		self.btn3.bind(on_press=partial(self.addDrink, alc_type="cider"))
		self.add_widget(self.btn3)
		
		self.btn4 = Button(text='Champagne', font_size='63sp', background_color=(1,25,50,.5))
		self.btn4.bind(on_press=partial(self.addDrink, alc_type="champagne"))
		self.add_widget(self.btn4)
		
		self.btn5 = Button(text='Spirit', font_size='63sp', background_color=(5.,1.,1.,1))
		self.btn5.bind(on_press=partial(self.addDrink, alc_type="spirit"))
		self.add_widget(self.btn5)
		
		self.btn = Button(text='Stat', font_size='63sp')
		self.btn.bind(on_press=self.showStats)
		self.add_widget(self.btn)
		 
	def loadData(self):
		self.store = DictStore(filename='app_data/data')
		self.total = self.store.get("total")['val']
		self.calYrTotal = self.store.get("calYrTotal")['val']
		self.log = self.store.get("log")['val']
		self.wsum = self.store.get("wsum")['val']
		self.monthTotals = self.store.get("monthTotals")['val']
		self.startDate_str = self.store.get("startDate")['val']
		print "\t\t\t KIVY 2: DictStore Succeeded"
	def resetData(self):
		dictionary = {'total': 0, "calYrTotal":0, "log": [], 'monthTotals':{}, 'startDate':'', 'wsum':{0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0} }
		self.store = DictStore(filename='app_data/data')
		self.firstRun = True
		self.store.put('total',val=0)
		self.store.put('calYrTotal',val=0)
		self.store.put('log',val=dictionary['log'])
		self.store.put('wsum',val=dictionary['wsum'])
		self.store.put('monthTotals',val=dictionary['monthTotals'])
		self.store.put('startDate', val=dictionary['startDate'])
		self.total = 0
		self.calYrTotal = 0
		self.log = []
		self.wsum = dictionary['wsum']
		self.monthTotals = {}
		self.startDate_str = ""
	# add data and serialize it 
	def initData(self):
		dictionary = {'total': 0, "calYrTotal":0, "log": [], 'monthTotals':{1:5.93, 2:5.93, 3:7.5, 4:7.213, 5:6.4, 6:1.5}, 'startDate':'2018-01-01'}
		dictionary['log'] = [{'date': 'm\xc3\xa1j-12', 'alc_type': 'wine', 'qt': 10},
							 {'date': 'm\xc3\xa1j-12', 'alc_type': 'beer', 'qt': 22},
							 {'date': 'm\xc3\xa1j-12', 'alc_type': 'spirit', 'qt': 0.5},
							 {'date': 'm\xc3\xa1j-12', 'alc_type': 'cider', 'qt': 6.66},
							 {'date': 'm\xc3\xa1j-12', 'alc_type': 'champagne', 'qt': 3},
							 
							 {'date': 'm\xc3\xa1j-13', 'alc_type': 'beer', 'qt': 1},
							 {'date': 'm\xc3\xa1j-13', 'alc_type': 'beer', 'qt': 8},
							 {'date': 'm\xc3\xa1j-17', 'alc_type': 'cider', 'qt': 3.3},
							 {'date': 'm\xc3\xa1j-18', 'alc_type': 'wine', 'qt': 1.5},
							 {'date': 'm\xc3\xa1j-19', 'alc_type': 'beer', 'qt': 2},
							 {'date': 'm\xc3\xa1j-19', 'alc_type': 'wine', 'qt': 2},
							 {'date': 'm\xc3\xa1j-19', 'alc_type': 'beer', 'qt': 3},
							 
							 {'date': 'm\xc3\xa1j-19', 'alc_type': 'champagne', 'qt': 3.5},
							 {'date': 'm\xc3\xa1j-20', 'alc_type': 'wine', 'qt': 1},
							 {'date': 'm\xc3\xa1j-21', 'alc_type': 'wine', 'qt': 1},
							 {'date': 'm\xc3\xa1j-25', 'alc_type': 'wine', 'qt': 4},
							
							 {'date': 'may-26', 'alc_type': 'cider', 'qt':3.3 },
							 {'date': 'may-26', 'alc_type': 'beer', 'qt':10 },
							 {'date': 'may-27', 'alc_type': 'wine', 'qt':1 },
							 {'date': 'may-27', 'alc_type': 'spirit', 'qt':0.4 },
							 
							 {'date': 'jun-02', 'alc_type': 'cider', 'qt':3.3 },
							 {'date': 'jun-02', 'alc_type': 'wine', 'qt':3 },
							 {'date': 'jun-07', 'alc_type': 'beer', 'qt':5 },
							 {'date': 'jun-08', 'alc_type': 'cider', 'qt':4 },
							 {'date': 'jun-08', 'alc_type': 'wine', 'qt':2 },
							 {'date': 'jun-08', 'alc_type': 'beer', 'qt':5 },
							 {'date': 'jun-09', 'alc_type': 'wine', 'qt':1 }
							 ]
		dictionary['wsum'] = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
		for m in dictionary['monthTotals']:
			dictionary['total'] += dictionary['monthTotals'][m]
			dictionary['calYrTotal'] = dictionary['total']
		self.store = DictStore(filename='app_data/data')
		self.store.put('total',val=dictionary['total'])
		self.store.put('calYrTotal',val=dictionary['calYrTotal'])
		self.store.put('log',val=dictionary['log'])
		self.store.put('wsum',val=dictionary['wsum'])
		self.store.put('monthTotals',val=dictionary['monthTotals'])
		self.store.put('startDate', val=dictionary['startDate'])
		self.total = dictionary['total']
		self.calYrTotal = dictionary['calYrTotal']
		self.log = dictionary['log']
		self.wsum = dictionary['wsum']
		self.monthTotals = dictionary['monthTotals']
		self.startDate_str = dictionary['startDate']
		pass
	def addDrink(self, *args, **kwargs):
		layout = GridLayout(cols=1, padding=10)
		self.inputWidget = TextInput(multiline=False, input_type='number', input_filter='float', font_size='100sp')
		layout.add_widget(self.inputWidget)
		self.inputWidget.bind(text=partial(self.on_text, alc_type=kwargs['alc_type']))
		saveButton = Button(text = "Save", font_size='63sp')
		layout.add_widget(saveButton)       
		self.popup = Popup(title='Add ' + kwargs['alc_type'] + ' amount in dl', content=layout)    
		#self.popup.bind(on_dismiss=self.saveInput)
		saveButton.bind(on_press=self.saveInput)
		self.popup.open()
		
	def on_text(self, *args, **kwargs):
		print kwargs['alc_type']
		if len(args[0].text) > 0:
			print args[0].text
			self.newDrink = {'alc_type':kwargs['alc_type'], 'qt':float(args[0].text), 'date':date.today().strftime('%Y-%b-%d')}
			
	def saveInput(self,instance):
		print "Input saved :" 
		print self.newDrink
		amount = self.newDrink['qt'] * self.alc_cont[self.newDrink['alc_type']]
		today = date.today()
		self.calYrTotal += amount
		self.total += amount
		self.log.append(self.newDrink)
		self.store.put('calYrTotal', val=self.calYrTotal)
		self.store.put('total', val=self.total)
		self.store.put('log', val=self.log)
		print today.weekday()
		self.wsum[today.weekday()] += amount
		self.store.put('wsum', val=self.wsum )
		print self.wsum
		month = today.month
		if month in self.monthTotals:
			self.monthTotals[month] += amount
		else:
			self.monthTotals[month] = amount
		self.store.put('monthTotals', val=self.monthTotals)
		self.popup.dismiss()
		
	def showStats(self,instance):
		layout_popup = BoxLayout( size_hint_y=None, orientation='vertical' )
		layout_popup.bind(minimum_height=layout_popup.setter('height'))
		
		today = date.today()
		year = today.year
		month = today.month
		
		calYrTotal_str = "{0:.2f}".format(0.1 * self.calYrTotal) 
		btn1 = Button(text="CalYrTotal: " + calYrTotal_str ,size_hint_y=None, size_y=69, font_size='36sp')
		btn1.bind(on_press=self.statDoc)
		layout_popup.add_widget(btn1)
		
		expCalYrTotal_str = "{0:.2f}".format(0.1 * self.calYrTotal*365./self.calcDaysBetween(date(today.year,1,1), today))
		layout_popup.bind(minimum_height=layout_popup.setter('height'))
		btn2 = Button(text="ExpCalYrTotal: " + expCalYrTotal_str ,size_hint_y=None, size_y=69, font_size='36sp')
		btn2.bind(on_press=self.statDoc)
		layout_popup.add_widget(btn2)
		
		expFwdYrTotal_str = "{0:.2f}".format(0.1 * self.total*365./self.calcDaysBetween(self.startDate, today))
		layout_popup.bind(minimum_height=layout_popup.setter('height'))
		btn3 = Button(text="ExpFwdYrTotal: " + expFwdYrTotal_str ,size_hint_y=None, size_y=69, font_size='36sp')
		btn3.bind(on_press=self.statDoc)
		layout_popup.add_widget(btn3)
		
		print self.monthTotals
		if month not in self.monthTotals:
			self.monthTotals[month] = 0
		monthTotal_str = "{0:.2f}".format(0.1 * self.monthTotals[month])
		layout_popup.bind(minimum_height=layout_popup.setter('height'))
		btn4 = Button(text="MnthTotal: " + monthTotal_str ,size_hint_y=None, size_y=69, font_size='36sp')
		btn4.bind(on_press=self.statDoc)
		layout_popup.add_widget(btn4)
		
		expMonthTotal_str = "{0:.2f}".format(0.1 * self.monthTotals[month]*calendar.monthrange(year,month)[1]/self.calcDaysBetween(date(today.year,month,1), today))
		layout_popup.bind(minimum_height=layout_popup.setter('height'))
		btn5 = Button(text="ExpMnthTotal: " + expMonthTotal_str ,size_hint_y=None, size_y=69, font_size='36sp')
		btn5.bind(on_press=self.statDoc)
		layout_popup.add_widget(btn5)
		
		btn_list = Button(text="List of Drinks", size_hint_y=None, size_y=69, font_size='36sp')
		btn_list.bind(on_press=self.show_log)
		layout_popup.add_widget(btn_list)
		
		root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height*0.9))
		root.add_widget(layout_popup)
		popup = Popup(title='Totals in litre', content=root, size_hint=(1, 1))
		popup.open()
	def show_log(self,instance):
		layout = BoxLayout( size_hint_y=None, orientation='vertical' )
		layout.bind(minimum_height=layout.setter('height'))
		
		# list of the drinks
		for item in reversed(self.log):
			btn_ = Button(text=str(item['qt']) + ' dl  ' + item['alc_type'] + '     ' + item['date'] ,size_hint_y=None, size_y='20sp', font_size='22sp', color=(40,5,5,.7))
			layout.add_widget(btn_)
		btn_ = Button(text='Startdate : '+self.startDate_str ,size_hint_y=None, size_y='20sp', font_size='22sp', color=(40,5,5,.7))
		layout.add_widget(btn_)
		root_log = ScrollView(size_hint=(1, None), size=(Window.width, Window.height*0.9))
		root_log.add_widget(layout)
		popup_log = Popup(title='List of Drinks', content=root_log, size_hint=(1, 1))
		popup_log.open()

	def calcExpFwMonth(self):
		pass
	def calcWeekDaysPassed(self):
		yr0 = int(self.startDate_str.split("-")[0])
		mnth0 = int(self.startDate_str.split("-")[1])
		day0 = int(self.startDate_str.split("-")[2])
		print (yr0,mnth0,day0)
		today = date.today()
		yr1 = today.year
		mnth1 = today.month
		day1 = today.day
		yr = yr0
		mnth = mnth0
		day = day0
		daysPassed = 0
		stop = False
		weekDaysPassed = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
		while yr <= yr1:
			while mnth <= 12:
				while day < calendar.monthrange(yr,mnth)[1] :
					day += 1
					daysPassed += 1
					weekDaysPassed[date(yr,mnth,day).weekday()] +=1
					if yr == yr1 and mnth == mnth1 and day == day1:
						stop = True
						break
				if stop:
					break
				else: 
					mnth += 1
					day = 1
			if stop:
				break
			else:
				yr += 1
				mnth = 1
		return weekDaysPassed
		
	def statDoc(self,instance):
		layout = GridLayout( size_hint_y=None, orientation='vertical' )
		stat_type = instance.text.split(":")[0]
		if stat_type == "CalYrTotal":
			text = "Alcohol consumption\n in the current calendar year up to today."
		elif stat_type == "ExpCalYrTotal":
			text = "Expected total alcohol consumption in the current calendar year.\nLinear extrapolation."
		elif stat_type == "ExpFwdYrTotal":
			text = "Expected total alcohol consumption\nfor the next year(365 days) on.\nLinear extrapolation based on the average until today."
		elif stat_type == "MnthTotal":
			text = "Alcohol consumption\n in the current calendar month up to today."
		elif stat_type == "ExpMnthTotal":
			text = "Expected total alcohol consumption\n in the current calendar month.\nLinear extrapolation from the amount consumed this month."
		else:
			text = stat_type
		label = Label(text=text)
		popup = TextPopup(title='Details',
			content=label,
			size_hint=(Window.width*0.75, Window.height*0.75),font_size='36sp' )
		popup.open()
		pass
		
	def calcDaysBetween(self, date1, date2):
		daysPassed = (date2 - date1).days + 1
		return daysPassed
"""
class FloatInput(TextInput):

    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)        
"""
class TextPopup(Popup): 
	def __init__(self,**kwargs):
		self.window= Window
		super(TextPopup,self).__init__(**kwargs)
		self.size=(min(0.95 * self.window.width, 500),500)
class PiaApp(App):
	def build(self):
		return MainScreen()
		
if __name__== '__main__':
	PiaApp().run()


