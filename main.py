import random
from time import sleep

verboseRunning = True
log_list = []

CRUMB_COLOURS = [
	'red',
	'orange',
	'yellow',
	'green',
	'blue',
	'indigo',
	'violet',
	'black',
	'white'
]
CRUMB_ACTIONS = [
	'breed',
	'attack',
	'heal'
]

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def vprint(str, delay = 0.7):
	if verboseRunning:
		print(str)
		log_list.append(str)
		sleep(delay)
def vsleep(time):
	if verboseRunning:
		sleep(time)
def vsaveLog(list):
	with open('log.txt', 'a') as logfile:
		logfile.write('\n' + '\n'.join(log_list))
		logfile.close()
if verboseRunning:
	with open('log.txt', 'w') as logfile:
		logfile.close()


class Crumb():

	def __init__(self, points):
		self.stats = {
			'base': {
				'speed': 0,
				'strength': 0,
				'smarts': 0,
				'maxhp': 0
			},
			'current': {
				'hp': 0
			},
			'vanity': {
				'colour': None
			}
		}
		self.id = self.generateRandomID()
		self.randomiseStats(points)
		self.turns_survived = 0
		vprint(f'Generated new crumb with ID {self.id}', 0.1)

	def randomiseStats(self, points):
		for stat in self.stats['base']:
			assignStatValue = random.randint(0, points)
			self.stats['base'][stat] = assignStatValue
			points -= assignStatValue
		self.stats['base']['maxhp'] += 1
		self.stats['vanity']['colour'] = CRUMB_COLOURS[random.randint(0, len(CRUMB_COLOURS) - 1)]
		self.stats['current']['hp'] = self.stats['base']['maxhp']

	def generateRandomID(self):
		idResult = ''
		for i in range(5):
			idResult += str(random.randint(0, 9))
		idResult += ALPHABET.upper()[random.randint(0, len(ALPHABET) - 1)]
		return idResult


class PetriDish():

	def __init__(self, crumbAmount, starterPoints = 10):
		self.crumbs = []
		self.generateCrumbs(crumbAmount, starterPoints)

	def generateCrumbs(self, crumbAmount, points = 10):
		for i in range(crumbAmount):
			self.crumbs.append(Crumb(points))

	def performTurn(self, crumb):
		targetCrumb = self.crumbs[random.randint(0, len(self.crumbs) - 1)]
		actionChoice = CRUMB_ACTIONS[random.randint(0, len(CRUMB_ACTIONS) - 1)]
		if actionChoice == 'heal':
			self.healCrumb(crumb)
		elif actionChoice == 'breed':
			self.breedCrumbs(crumb, targetCrumb)
		elif actionChoice == 'attack':
			self.attackCrumbs(crumb, targetCrumb)

	def healCrumb(self, crumb):
		if crumb.stats['base']['smarts'] < 0:
			healAmount = -1
		else:
			healAmount = random.randint(0, round(crumb.stats['base']['smarts']))
		crumb.stats['current']['hp'] += healAmount
		if crumb.stats['current']['hp'] > crumb.stats['base']['maxhp']:
			crumb.stats['current']['hp'] = crumb.stats['base']['maxhp']
		vprint(f'Crumb {crumb.id} healed itself by {healAmount}')
		return crumb

	def attackCrumbs(self, attackerCrumb, victimCrumb):
		fasterCrumb = attackerCrumb.stats['base']['speed'] > victimCrumb.stats['base']['speed']
		slowerCrumb = victimCrumb
		vprint(f'{attackerCrumb.id} has begun a battle with {victimCrumb.id}')
		if fasterCrumb:
			fasterCrumb = attackerCrumb
		else:
			fasterCrumb = victimCrumb
		if fasterCrumb == slowerCrumb:
			slowerCrumb = attackerCrumb
		vprint(f'  {fasterCrumb.id} is faster than {slowerCrumb.id} and thus is attacking first:')
		slowerCrumb.stats['current']['hp'] -= fasterCrumb.stats['base']['strength']
		if slowerCrumb.stats['current']['hp'] <= 0:
			self.crumbs.remove(slowerCrumb)
			vprint(f'  {slowerCrumb.id} has been defeated by {fasterCrumb.id} after surviving {slowerCrumb.turns_survived} turns.')
			return slowerCrumb
		else:
			vprint(f'  {slowerCrumb.id} has survived the attack and is now attacking.')
			fasterCrumb.stats['current']['hp'] -= slowerCrumb.stats['base']['strength']
			if fasterCrumb.stats['current']['hp'] <= 0:
				self.crumbs.remove(fasterCrumb)
				vprint(f'  {fasterCrumb.id} has been defeated by {slowerCrumb.id} after surviving {fasterCrumb.turns_survived} turns.')
				return fasterCrumb
		vprint(f'Battle between {attackerCrumb.id} and {victimCrumb.id} has concluded.')
		return None

	def breedCrumbs(self, crumb1, crumb2):
		resultCrumb = Crumb(0)
		for stat in resultCrumb.stats['base']:
			resultCrumb.stats['base'][stat] = round((crumb1.stats['base'][stat] + crumb2.stats['base'][stat]) / 2)
			if random.randint(0, 9) == 0:
				resultCrumb.stats['base'][stat] += (random.randint(0, 4) - 2)
		resultCrumb.stats['current']['hp'] = resultCrumb.stats['base']['maxhp']
		self.crumbs.append(resultCrumb)
		resultStats = f'  speed: {resultCrumb.stats["base"]["speed"]}\n  strength: {resultCrumb.stats["base"]["strength"]}\n  smarts: {resultCrumb.stats["base"]["smarts"]}\n  maxhp: {resultCrumb.stats["base"]["maxhp"]}'
		vprint(f'{crumb1.id} has bred with {crumb2.id} to create {resultCrumb.id}, here are its stats:\n{resultStats}')
		return resultCrumb
	
	def getHighestReleventStats(self):
		highestCrumbs = [None, None, None, None, None] #spe, str, sma, mhp, turns
		for crumb in self.crumbs: #spe
			if highestCrumbs[0] == None or crumb.stats['base']['speed'] > highestCrumbs[0].stats['base']['speed']:
				highestCrumbs[0] = crumb
		for crumb in self.crumbs: #str
			if highestCrumbs[1] == None or crumb.stats['base']['strength'] > highestCrumbs[1].stats['base']['strength']:
				highestCrumbs[1] = crumb
		for crumb in self.crumbs: #sma
			if highestCrumbs[2] == None or crumb.stats['base']['smarts'] > highestCrumbs[2].stats['base']['smarts']:
				highestCrumbs[2] = crumb
		for crumb in self.crumbs: #mhp
			if highestCrumbs[3] == None or crumb.stats['base']['maxhp'] > highestCrumbs[3].stats['base']['maxhp']:
				highestCrumbs[3] = crumb
		for crumb in self.crumbs: #turn
			if highestCrumbs[4] == None or crumb.turns_survived > highestCrumbs[4].turns_survived:
				highestCrumbs[4] = crumb
			#print(f'{crumb.id} stat = {crumb.turns_survived}')
		return highestCrumbs

	def advanceTime(self):
		currentCrumb = self.crumbs[0]
		self.performTurn(currentCrumb)
		self.crumbs.append(currentCrumb)
		self.crumbs.remove(currentCrumb)
		for crumb in self.crumbs:
			crumb.turns_survived += 1

test_dish = PetriDish(10, 10)
turn = 0
while True:
	test_dish.advanceTime()
	#print(test_dish.crumbs)
	print(f'CURRENT TURN: {turn}')
	#print(test_dish.crumbs[0].stats)
	turn += 1
	if turn % 100 == 0:
		vsaveLog(log_list)
		log_list = []
	if turn % 50 == 0:
		high_scores = test_dish.getHighestReleventStats()
		vprint(f'\n{"#"*10}\nSTAT UPDATE:\nHIGHEST spe: {high_scores[0].id} with a speed of {high_scores[0].stats["base"]["speed"]}\nHIGHEST str: {high_scores[1].id} with a strength of {high_scores[1].stats["base"]["strength"]}\nHIGHEST sma: {high_scores[2].id} with a smarts of {high_scores[2].stats["base"]["smarts"]}\nHIGHEST mhp: {high_scores[3].id} with a max hp of {high_scores[3].stats["base"]["maxhp"]}\nMOST TURNS SURVIVED: {high_scores[4].id} with a turns survived of {high_scores[4].turns_survived}\n{"#"*10}')
	if verboseRunning:
		pass
	else:
		sleep(0.001)
	
