Final Project
ECE 4564

Smart Alarm Clock
-----------------

- To ensure all features work, please use Google Chrome as your browser


ADXL345:

$ sudo nano /etc/modules
	add the following lines:
		i2c-bcm2708
		i2c-dev

$ sudo nano /etc/modprobe.d/raspi-blacklist.conf
	# blacklist i2c-bcm2708

$ sudo shutdown -h now
$ sudo apt-get install python-smbus i2c-tools git-core

$ sudo i2cdetect -y l
	to see if accelerometer is found on the i2c bus

=======
Packages

- gflags
- google-api-python-client
- twisted
- adxl345-python
