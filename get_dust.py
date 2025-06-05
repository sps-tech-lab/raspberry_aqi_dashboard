from sds011_driver import SDS011

sensor = SDS011("/dev/serial0")
pm25, pm10 = sensor.read()

print(f"Current PM2.5: {pm25} µg/m³")
print(f"Current PM10:  {pm10} µg/m³")

sensor.close()
