from ursina import *

app = Ursina(borderless=False)

doughnut = 0
counter = Text(text='0 Doughnuts',y=.25, z=-1, origin=(0, 0), background=True, )
button = Button(text='doughnut', scale=.125)

def button_click():
	global doughnut
	doughnut += 1
	counter.text = str(f'{doughnut} Doughnuts')

button.on_click = button_click

e_fryer = Button(cost=10, x=.2, scale=.124, color=color.gray, disabled=True)
e_fryer.texture = './assets/e_fryer.png'
e_fryer.text = str(e_fryer.cost)
e_fryer.tooltip = Tooltip(f'<doughnuts>Electric fryer\n <default>Generates 1 doughnut every 4 seconds!')


mw_emp = Button(cost=50, y=-.15, x=.2, scale=.124, color=color.gray, disabled=True)
mw_emp.texture = './assets/mw_emp.png'
mw_emp.text = str(mw_emp.cost)
mw_emp.tooltip = Tooltip(f'<doughnuts>Minimum Wage Employee\n <default>Generates 1 doughnut every 2 seconds!')


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

app.run()