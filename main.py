import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# New Antecedent/Consequent objects hold universe variables and membership
# functions
quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

# Auto-membership function population is possible with .automf(3, 5, or 7)
quality.automf(3)
service.automf(3)

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])

# quality['average'].view()


rule1 = ctrl.Rule(quality['poor'] | service['poor'], tip['low'])
rule2 = ctrl.Rule(service['average'], tip['medium'])
rule3 = ctrl.Rule(service['good'] | quality['good'], tip['high'])

tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

tipping = ctrl.ControlSystemSimulation(tipping_ctrl)


tipping.input['quality'] = 6.5
tipping.input['service'] = 9.8

# Crunch the numbers
# tipping.compute()



#2


light_distance = ctrl.Antecedent(np.arange(0, 140, 1), 'light_distance')
speed = ctrl.Antecedent(np.arange(0, 120, 1), 'speed')
acceleration = ctrl.Consequent(np.arange(-1, 1, .1), 'acceleration')
#
# light_distance.automf(3, 'quant')
# speed.automf(3, 'quant')
# acceleration.automf(3, 'quant')


light_distance['low'] = fuzz.trapmf(light_distance.universe, [-1, 0, 20, 45])
light_distance['medium'] = fuzz.trapmf(light_distance.universe, [20, 45, 100, 130])
light_distance['high'] = fuzz.trapmf(light_distance.universe, [105, 130, 140, 141])

speed['low'] = fuzz.trapmf(speed.universe, [-1, -1, 20, 65])
speed['medium'] = fuzz.trimf(speed.universe, [15, 65, 115])
speed['high'] = fuzz.trapmf(speed.universe, [65, 105, 120, 121])


acceleration['high-'] = fuzz.trapmf(acceleration.universe, [-1.1, -1.1, -0.4, 0])
acceleration['high+'] = fuzz.trimf(acceleration.universe, [-0.4, 0, 0.1])
acceleration['low+'] = fuzz.trimf(acceleration.universe, [-0.2, 0, 0.4])
acceleration['low-'] = fuzz.trapmf(acceleration.universe, [0, 0.4, 1.1, 1.1])

rules = [
    ctrl.Rule(light_distance['low'] | speed['low'], acceleration['high-']),
    ctrl.Rule(light_distance['medium'] | speed['low'], acceleration['low-']),
    ctrl.Rule(light_distance['high'] | speed['low'], acceleration['low-']),
    ctrl.Rule(light_distance['low'] | speed['medium'], acceleration['high+']),
    ctrl.Rule(light_distance['medium'] | speed['medium'], acceleration['low-']),
    ctrl.Rule(light_distance['high'] | speed['medium'], acceleration['low-']),
    ctrl.Rule(light_distance['low'] | speed['high'], acceleration['low+']),
    ctrl.Rule(light_distance['medium'] | speed['high'], acceleration['high-']),
    ctrl.Rule(light_distance['high'] | speed['high'], acceleration['low-']),
]


acceleration_ctrl = ctrl.ControlSystem(rules)
acceleration_sim = ctrl.ControlSystemSimulation(acceleration_ctrl)


acceleration_sim.input['light_distance'] = 20
acceleration_sim.input['speed'] = 100


# light_distance.view()
# speed.view()
# acceleration.view()

acceleration_sim.compute()
print(acceleration_sim.output['acceleration'])
