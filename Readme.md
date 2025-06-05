
# Raspberry AQI dashboard

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/sps-tech-lab/raspberry_aqi_dashboard?label=version)
![License](https://img.shields.io/github/license/sps-tech-lab/raspberry_aqi_dashboard)

Simple dashboard could be implemented on any raspberry pi board and provides access to collected data carts.

> [!IMPORTANT]
> At the moment it collects only PM2.5/PM10 dust particles measurements

![Appearence](https://github.com/sps-tech-lab/raspberry_aqi_dashboard/raw/main/readme/dashboard_example.png)

### Hardware
- Raspberry Pi Zero 2 W / Pi 3 / Pi 4 with Raspberry Pi OS (Lite or Full)
- [Nova SDS011 Dust Sensor](http://en.novasensor.cn/?list_16/55.html)
- Connected SDS011 sensor via GPIO UART (look table below)

### SDS011 wiring

| SDS011   | Pi GPIO Pin | Note               |
| -------- |:-----------:|:------------------:|
| VCC      | Pin 2 (5V)  | 5V only — NOT 3.3V |
| GND      | Pin 6 (GND) |                    |
| TXD      | Pin 10 (RX) | Pi receives data   |
| RXD      | Pin 8 (TX)  | Pi sends data      |

## Set up

### Enable serial port

```bash
sudo raspi-config
```
Interface Options → Serial Port → Login shell over serial: No → Enable serial hardware: Yes

```bash
sudo reboot
```

### Install required packages

```bash
sudo apt update
sudo apt install -y python3-pip python3-serial git unzip curl libatlas-base-dev
pip3 install dash pandas plotly
```

### Set log path

```python
#Change next string to preferable path
file_path = "~/dashboard/dust_log.csv"
```

### Enable periodic logging

```bash
crontab -e
```
add and save next
```
* * * * * /usr/bin/python3 /home/pi/log_sds011.py
```


### Install and configure Ngrok
Get ngrok:
- Visit https://ngrok.com/
- Create accaunt
- follow the prompts for your OS

Auth token:
```bash
ngrok config add-authtoken <your_token_here>
```


### Create systemd services

Create one file with name ```dashboard.service```
```bash
sudo nano /etc/systemd/system/dashboard.service
```
use next example below to set basic config
```ini
[Unit]
Description=Dash Air Quality Web App
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 /home/pi/dashboard.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Create another one file with name ```ngrok.service```
```bash
sudo nano /etc/systemd/system/ngrok.service
```
use next example below to set basic config
```ini
[Unit]
Description=Ngrok Tunnel for Air Quality Dashboard
After=network-online.target dashboard.service
Requires=dashboard.service

[Service]
User=pi
WorkingDirectory=/home/pi
ExecStartPre=/bin/sleep 5
ExecStart=/usr/local/bin/ngrok http 8050
Restart=on-failure
StandardOutput=append:/home/pi/ngrok.log
StandardError=append:/home/pi/ngrok.log
ExecStartPost=/bin/bash -c 'sleep 5 && grep -m 1 "https://" /home/pi/ngrok.log > /home/pi/current_url.txt'

[Install]
WantedBy=multi-user.target
```

### Enable and start services

```bash
sudo systemctl daemon-reload
sudo systemctl enable dashboard.service ngrok.service
sudo systemctl start dashboard.service ngrok.service
```

### Confirm everything Is working
```bash
systemctl status dashboard.service
systemctl status ngrok.service
```

### Get your live dashboard URL
```bash
cat /home/pi/current_url.txt
```
> [!TIP]
> Current dashboard url could be also found in Ngrok account:
> https://ngrok.com/ → Login → Endpoints
