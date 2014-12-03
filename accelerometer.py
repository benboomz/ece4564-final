import adxl345

accel = adxl345.ADXL345()

axes = accel.getAxes(True)

x = axes['x']
y = axes['y']
z = axes['z']

print x, y, z