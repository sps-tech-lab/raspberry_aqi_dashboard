from sds011_driver import SDS011
from datetime import datetime
import os

file_path = "~/dashboard/dust_log.csv"
write_header = not os.path.exists(file_path)

sensor = SDS011("/dev/serial0")
pm25, pm10 = sensor.read()
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(file_path, "a") as f:
    if write_header:
        f.write("Timestamp\tPM2.5 (µg/m³)\tPM10 (µg/m³)\n")
    f.write(f"{timestamp}\t{pm25}\t{pm10}\n")

sensor.close()
