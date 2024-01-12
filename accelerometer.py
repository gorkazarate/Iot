import time
import grovepi

    # Connect the Grove Accelerometer (+/- 1.5g) to any I2C port eg. I2C-1
    # Can be found at I2C address 0x4c
    # SCL,SDA,VCC,GND
while True:
	try:
		# Lee las lecturas del acelerómetro en los tres ejes
		x, y, z = grovepi.acc_xyz()
		print("X: {:.2f}, Y: {:.2f}, Z: {:.2f}".format(x, y, z))
		time.sleep(.5)

	except IOError:
		print ("Error")
