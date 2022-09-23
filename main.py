import json
import sys
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

app = Ursina(borderless=False)

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

doughnut = doughnut_data
counter = Text(text=doughnut, y=.25, z=-1, origin=(0, 0))
button = Button(scale=.125, model='mesh')
button.icon = './assets/doughnut.png'
button.pressed_color = button.color.tint(-.2)

def button_click():
	global doughnut
	doughnut += 1
	counter.text = str(f'{doughnut} Doughnuts')

button.on_click = button_click

e_fryer = Button(cost=ef_price, x=.2, y=.15, scale=.124, color=color.gray, disabled=True)
e_fryer.icon = './assets/e_fryer.png'
e_fryer.text = str(e_fryer.cost)
e_fryer.tooltip = Tooltip(f'<doughnuts>Electric fryer\n <default>Generates 1 doughnut every 4 seconds!')

mw_emp = Button(cost=50, y=0, x=.2, scale=.124, color=color.gray, disabled=True)
mw_emp.icon = './assets/mw_emp.png'
mw_emp.text = str(mw_emp.cost)
mw_emp.tooltip = Tooltip(f'<doughnuts>Minimum Wage Employee\n <default>Generates 1 doughnut every 2 seconds!')

trees = Button(cost=100, y=-.15, x=.2, scale=.124, color=color.gray, disabled=True)
trees.icon = './assets/d_tree.png'
trees.text = str(trees.cost)
trees.tooltip = Tooltip(f'<doughnuts>Doughnut Tree\n <default>Grows 1 doughnut every second!')

pond = Button(cost=150, y=-.3, x=.2, scale=.124, color=color.gray, disabled=True)
pond.icon = './assets/pond.png'
pond.text = str(mw_emp.cost)
pond.tooltip = Tooltip(f'<doughnuts>Minimum Wage Employee\n <default>Generates 1 doughnut fish every 2 seconds!')

# on click buy functions and button automation
def buy_fryer1():
	global doughnut
	global ef_level
	if doughnut >= e_fryer.cost:
		doughnut -= e_fryer.cost
		e_fryer.cost += math.floor(e_fryer.cost/2)
		ef_level += 1
		counter.text = str(f'{doughnut} Doughnuts')
		e_fryer.text = str(e_fryer.cost)
		invoke(auto_generate_fryer1, 1, 1)

e_fryer.on_click = buy_fryer1

def auto_generate_fryer1(value=1, interval=4):
	global doughnut
	doughnut += 1
	counter.text = str(f'{doughnut} Doughnuts')
	e_fryer.animate_scale(.125 * 1.1)
	e_fryer.animate_scale(.124, delay=.2)
	invoke(auto_generate_fryer1, value, delay=interval)

def buy_mw_emp():
	global doughnut
	if doughnut >= mw_emp.cost:
		doughnut -= mw_emp.cost
		mw_emp.cost += math.floor(mw_emp.cost/2)
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


def update():
	global doughnut
	for b in (e_fryer, ):
		if doughnut >= b.cost:
			b.disabled = False
			b.color = color.light_gray
		else:
			b.disabled = True
			b.color = color.gray
	for b in (mw_emp, ):
		if doughnut >= b.cost:
			b.disabled = False
			b.color = color.light_gray
		else:
			b.disabled = True
			b.color = color.gray



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