from ursina import *

app = Ursina(borderless=False)

doughnut = 0
counter = Text(text='0 Doughnuts',y=.25, z=-1, origin=(0, 0), background=True, )
button = Button(text='doughnut click', color=color.brown, scale=.125)

def button_click():
	global doughnut
	doughnut += 1
	counter.text = str(f'{doughnut} Doughnuts')

button.on_click = button_click

e_fryer = Button(cost=10, x=.2, scale=.124, color=color.dark_gray, disabled=True)
e_fryer.text = str(e_fryer.cost)
e_fryer.tooltip = Tooltip(f'<doughnuts>Electric fryer\n <default>Generates 1 doughnut every 4 seconds!')

def buy_fryer1():
	global doughnut
	if doughnut >= e_fryer.cost:
		doughnut -= e_fryer.cost
		e_fryer.cost += math.floor(e_fryer.cost/2)
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

def update():
	global doughnut
	for b in (e_fryer, ):
		if doughnut >= b.cost:
			b.disabled = False
			b.color = color.green
		else:
			b.disabled = True
			b.color = color.gray
	# for b in (mw_emp, ):
	# 	if doughnut >= b.cost:
	# 		b.disabled = False
	# 		b.color = color.green
	# 	else:
	# 		b.disabled = True
	# 		b.color = color.gray

app.run()