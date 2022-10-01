import json, sys, threading
from json import tool
from tkinter import messagebox, Tk
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

if not os.path.isdir("data/"):
	os.makedirs("data")


if not os.path.isfile("data/data.json"):
	open("data/data.json", "w").write(r"{}")
	data = json.load(open("data/data.json"))
	data["doughnuts"] = 0
	data["e_fryer_price"] = 10
	data["e_fryer_level"] = 0
	data["e_fryer_doughnuts"] = 1
	data["e_fryer_speed"] = 4
	data["e_fryer_version"] = 1
	# data["songplaying"] = True
	# data["sfxplaying"] = True
	# data["playedbefore"] = False
	json.dump(data, open("data/data.json", "w"))

def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)

data = json.load(open("data/data.json"))

doughnut_data = data["doughnuts"]
ef_price = data["e_fryer_price"]
ef_level = data["e_fryer_level"]
ef_doughnuts = data["e_fryer_doughnuts"]
ef_speed = data["e_fryer_speed"]
ef_version = data["e_fryer_version"]

app = Ursina(borderless=False)

# world logic

Sky()

ground = Entity(
	model='plane',
	texture='grass',
	collider='mesh',
	scale=(100, 1, 100)
)

# player = FirstPersonController(
# 	position=(0, 2, -5)
# )

wall1 = Entity(
	model='cube',
	texture='brick',
	collider='cube',
	scale=(100, 10, 5),
	position=(0, 5, 50),
	color=color.dark_gray
)

wall2 = duplicate(wall1, z=-50)
wall3 = duplicate(wall1, rotation_y=90, x=-50, z=0)
wall4 = duplicate(wall3, x=50)
wall5 = duplicate(wall1, position=(0, 2, 0), scale=(20, .5, 0.5), color=color.white)

# game logic

master = Tk()

doughnut = doughnut_data
counter = Text(text = "Click to Start", y=.25, z=-1, origin=(0, 0))
counter.text = doughnut
button = Button(scale=.125, model='mesh')
button.icon = './assets/doughnut.png'
button.pressed_color = button.color.tint(-.2)

def button_click():
	global doughnut
	doughnut += 1
	button.animate_scale(.125 * 1.1)
	
	counter.text = str(f'{doughnut} Doughnuts')

button.on_click = button_click

def update():
	global doughnut
	for b in (e_fryer, ):
		if doughnut >= b.cost:
			b.disabled = False
			b.color = color.light_gray
			b.text_color = color.white
		else:
			b.disabled = True
			b.color = color.gray
			b.text_color = color.light_gray
		# while b.level > 0:
		# 	master.after(b.speed, button_click)
	for b in (mw_emp, ):
		if doughnut >= b.cost:
			b.disabled = False
			b.color = color.light_gray
		else:
			b.disabled = True
			b.color = color.gray


class Building(Button):
	def __init__(self, y, cost, tooltip, level, speed, amt, version):
		super().__init__(
			parent=scene,
			scale = 1,
			color = color.gray,
			disabled = True,
			text = str(cost),
			text_origin=(-0.5, -0.5, -.5),
			text_color = color.light_gray,
			cost = cost,
			x = 1.5,
			y = y,
			tooltip = tooltip,
			level = level,
			speed = speed,
			amt = amt,
			version = version,
		)

	def input(self, key):
		if self.hovered:
			if key == 'left mouse down':
				global doughnut
				if doughnut >= self.cost:
					doughnut -= self.cost
					self.cost += math.floor(self.cost/3)
					self.level += 1
					counter.text = str(f'{doughnut} Doughnuts')
					self.text = str(self.cost)


e_fryer = Building(
	cost = ef_price, 
	y = 1.2, 
	level = ef_level,
	speed = ef_speed,
	amt = ef_doughnuts,
	version = ef_version,
	tooltip=Tooltip(f'<doughnuts>Electric fryer\n <default>Generates 1 doughnut every 4 seconds!')
	)

e_fryer.icon = './assets/e_fryer.png'

mw_emp = Building(
	cost = 50, 
	y = 0.1, 
	level = 1,
	speed = 2,
	amt = 1,
	version = 1,
	tooltip = Tooltip(f'<doughnuts>Minimum Wage Employee\n <default>Generates 1 doughnut every 2 seconds!')
)
mw_emp.icon = './assets/mw_emp.png'

trees = Building(
	cost = 150,
	y = -1,
	level = 1,
	speed = 1,
	amt = 1,
	version = 1,
	tooltip = Tooltip(f'<doughnuts>Doughnut Tree\n <default>Grows 1 doughnut every second!')
	)
trees.icon = './assets/d_tree.png'

pond = Building(
	cost = 225,
	y = -2.1,
	level = 1,
	speed = 1,
	amt = 3,
	version = 1,
	tooltip = Tooltip(f'<doughnuts>Minimum Wage Employee\n <default>Generates 1 doughnut fish every 2 seconds!')
	)
pond.icon = './assets/pond.png'
# def auto_generate_fryer1(value=1):
# 	global doughnut
# 	doughnut += value
# 	counter.text = str(f'{doughnut} Doughnuts')
# 	e_fryer.animate_scale(.125 * 1.1)
# 	e_fryer.animate_scale(.124, delay=.2)
	# invoke(auto_generate_fryer1, value, delay=interval)

def buy_mw_emp():
	global doughnut
	if doughnut >= mw_emp.cost:
		doughnut -= mw_emp.cost
		mw_emp.cost += math.floor(mw_emp.cost/3)
		counter.text = str(f'{doughnut} Doughnuts')
		mw_emp.text = str(mw_emp.cost)
		invoke(auto_generate_mw_emp, 1, 1)

mw_emp.on_click = buy_mw_emp

def auto_generate_mw_emp(value=1, interval=2):
	global doughnut
	doughnut += 1
	counter.text = str(f'{doughnut} Doughnuts')
	mw_emp.animate_scale(.125 * 1.1)
	mw_emp.animate_scale(.124, delay=.2)
	invoke(auto_generate_mw_emp, value, delay=interval)

# end game logic

def quitApp():
	data2 = json.load(open("data/data.json"))
	data2["doughnuts"] = doughnut
	data2["e_fryer_price"] = e_fryer.cost
	data2["e_fryer_level"] = ef_level
	data2["e_fryer_doughnuts"] = ef_doughnuts
	data2["e_fryer_speed"] = ef_speed
	# data2["songplaying"] = songPlaying
	# data2["sfxplaying"] = sfxPlaying
	# data2["playedbefore"] = True
	json.dump(data2, open("data/data.json", "w"))
	quit()

def input(key):
	if key == 'escape':
		quitApp()

app.run()