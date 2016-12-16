from requests import *
from json import *
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import sys
import pyglet
window = pyglet.window.Window()


planets = {}

num = 1
x = True

print('Gathering Data')
pokemon = 'http://pokeapi.co/api/v2/pokemon/'
star_wars = 'http://swapi.co/api/people/'
while x:
    resp = get(star_wars + str(num))
    try:
        try:
            print(loads(resp.text)['name'] + ' -- ' + str(num))
        except:
            print('Not Found')

    except:
        pass
        # x = False
    num += 1
    num %= 88

y_pos = np.arange(len(planets))
pop = []
for x in planets:
    pop.append(planets[x])
plt.subplot(1, 1, 1)
plt.barh(y_pos, pop)
plt.yticks(y_pos, planets)
plt.xlabel('People')
plt.ylabel('Planet')

plt.show()
