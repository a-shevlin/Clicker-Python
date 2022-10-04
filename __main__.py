import json, sys, threading
from pyclbr import Function
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

player = FirstPersonController(
	position=(0, 2, -5)
)

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
wall5 = duplicate(wall1, position=(0, 2, .3), scale=(20, 8, .5), color=color.cyan)

# game logic

master = Tk()

doughnut = doughnut_data
counter = Text(text = "Click to Start", y=.25, z=-1)
counter.text = doughnut

class Doughnut(Button):
	def __init__(self):
		super().__init__(
			parent = scene,
			scale = 1, 
			x = 0, 
			y = 2,
			cps = 1,
			icon = './assets/doughnut.png', 
		)
	
	def input(self, key):
		if self.hovered:
			if key == 'left mouse down':
				global doughnut
				doughnut += 1
				self.animate_scale(1 * 1.1)
				self.animate_scale(1)
				counter.text = str(f'{doughnut} Doughnuts')

button = Doughnut()

def update():
	global doughnut
	for b in (e_fryer, mw_emp, trees, pond):
		if doughnut >= b.cost:
			b.disabled = False
			b.color = color.light_gray
			b.text_color = color.white
		else:
			b.disabled = True
			b.color = color.gray
			b.text_color = color.light_gray
		# while b.level > 0:
		# 	auto_run.start()
	# for b in (mw_emp, ):
	# 	if doughnut >= b.cost:
	# 		b.disabled = False
	# 		b.color = color.light_gray
	# 	else:
	# 		b.disabled = True
	# 		b.color = color.gray

def cps(self):
	global doughnut
	doughnut += self.amt
	self.animate_scale(.125 * 1.1)
	counter.text = str(f'{doughnut} Doughnuts')

auto_run = Sequence(1, Func(cps, duration=1), loop=True)
class Building(Button):
	def __init__(self, y, cost, level, speed, amt, version, icon):
		super().__init__(
			parent=scene,
			scale = 1.25,
			color = color.gray,
			disabled = True,
			text_origin=(-0.5, -0.5, -.2),
			text_color = color.light_gray,
			cost = cost,
			u_cost = cost * 3,
			x = 1.5,
			y = y,
			tooltip = Tooltip(f'<doughnuts>Electric fryer\n <default>Generates {amt} doughnut every {speed} seconds!'),
			level = level,
			speed = speed,
			amt = amt,
			version = version,
			icon = icon,
			text = str(f'{cost} to buy')
		)
		
		self.text_entity.world_scale = .4

	def input(self, key):
		if self.hovered:
			if key == 'left mouse down':
				global doughnut
				if doughnut >= self.cost:
					doughnut -= self.cost
					self.cost += math.floor(self.cost/3)
					self.level += 1
					counter.text = str(f'{doughnut} Doughnuts')
					self.text = str(f'{self.cost} to buy\n\n\n{self.u_cost} to upgrade')
					self.text_entity.world_scale = .4
			if key == 'u':
				if doughnut >= self.u_cost:
					doughnut -= self.u_cost
					self.amt += math.floor(self.amt * 1.5)
					self.u_cost += math.floor(self.cost/2.5)
					self.version += 1
					counter.text = str(f'{doughnut} Doughnuts')
					self.text = str(f'{self.cost} to buy\n\n\n{self.u_cost} to upgrade')
					self.text_entity.world_scale = .4

e_fryer = Building(
	cost = ef_price, 
	y = 1.5, 
	level = ef_level,
	speed = ef_speed,
	amt = ef_doughnuts,
	version = ef_version,
	icon = './assets/e_fryer.png'
	)

mw_emp = Building(
	cost = 50, 
	y = 0, 
	level = 1,
	speed = 2,
	amt = 1,
	version = 1,
	icon = './assets/mw_emp.png'
)

trees = Building(
	cost = 150,
	y = -1.5,
	level = 1,
	speed = 1,
	amt = 1,
	version = 1,
	icon = './assets/d_tree.png'
	)

pond = Building(
	cost = 225,
	y = -3,
	level = 1,
	speed = 1,
	amt = 3,
	version = 1,
	icon = './assets/pond.png'
	)

# def auto_generate_fryer1(value=1):
# 	global doughnut
# 	doughnut += value
# 	counter.text = str(f'{doughnut} Doughnuts')
# 	e_fryer.animate_scale(.125 * 1.1)
# 	e_fryer.animate_scale(.124, delay=.2)
	# invoke(auto_generate_fryer1, value, delay=interval)

# def buy_mw_emp():
# 	global doughnut
# 	if doughnut >= mw_emp.cost:
# 		doughnut -= mw_emp.cost
# 		mw_emp.cost += math.floor(mw_emp.cost/3)
# 		counter.text = str(f'{doughnut} Doughnuts')
# 		mw_emp.text = str(mw_emp.cost)
# 		invoke(auto_generate_mw_emp, 1, 1)

# mw_emp.on_click = buy_mw_emp

# def auto_generate_mw_emp(value=1, interval=2):
# 	global doughnut
# 	doughnut += 1
# 	counter.text = str(f'{doughnut} Doughnuts')
# 	mw_emp.animate_scale(.125 * 1.1)
# 	mw_emp.animate_scale(.124, delay=.2)
# 	invoke(auto_generate_mw_emp, value, delay=interval)

# end game logic

def quitApp():
	data2 = json.load(open("data/data.json"))
	data2["doughnuts"] = doughnut
	data2["e_fryer_price"] = e_fryer.cost
	data2["e_fryer_level"] = e_fryer.level
	data2["e_fryer_doughnuts"] = e_fryer.amt
	data2["e_fryer_speed"] = e_fryer.speed
	# data2["songplaying"] = songPlaying
	# data2["sfxplaying"] = sfxPlaying
	# data2["playedbefore"] = True
	json.dump(data2, open("data/data.json", "w"))
	quit()

def input(key):
	if key == 'escape':
		quitApp()

app.run()