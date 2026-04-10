from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

# Optional: improve sensitivity / stability
sense.colour.gain = 4
sense.colour.integration_cycles = 64

while True:
    sleep(sense.colour.integration_time + 0.1)

    red, green, blue, clear = sense.colour.colour
    print(f"R: {red}, G: {green}, B: {blue}, Brightness: {clear}")
