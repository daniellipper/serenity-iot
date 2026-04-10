from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

print("Clearing display...")
sense.clear()
sleep(1)

print("Showing red...")
sense.clear(255, 0, 0)
sleep(2)

print("Showing green...")
sense.clear(0, 255, 0)
sleep(2)

print("Showing blue...")
sense.clear(0, 0, 255)
sleep(2)

print("Turning off...")
sense.clear()
