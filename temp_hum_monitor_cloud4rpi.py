import random
import board
import busio
import time
import sys
import cloud4rpi
#import rpi
import adafruit_bme280
import adafruit_bmp280

# Put your device token here. To get the token,
# sign up at https://cloud4rpi.io and create a device.
DEVICE_TOKEN = 'PUT YOUR DEVICE TOKEN HERE'

# Constants
DATA_SENDING_INTERVAL = 60*10 #600  # secs
DIAG_SENDING_INTERVAL = 600  # secs
POLL_INTERVAL = 1  # secs
DATA_UPDATE_INTERVAL = 10 # secs

BME280_TEMP_OFFSET = 0 # deg F
BMP280_TEMP_OFFSET = 0 # deg F

INSIDE_TEMP_LOW = 45  # deg F
INSIDE_TEMP_HIGH = 65  # deg F
inside_temp_alert_high = None
inside_temp_alert_low = None
inside_temp_alert_normal = None

temp_in, hum_in, temp_out, hum_out = None, None, None, None
last_update = time.time() - 20

# Create busio I2C
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Create BME280 object - Can measure humidity - Used for inside sensor
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
bme280.sea_level_pressure = 1013.25
# Create BMP280 object - Same as BME280 but without humidity measurement - Used for outside sensor
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c,address=0x76)
bmp280.sea_level_pressure = 1013.25


def update_data():
    global last_update, hum_in, temp_in, hum_out, temp_out, inside_temp_alert_high, inside_temp_alert_low, inside_temp_alert_normal
    if time.time() - last_update > DATA_UPDATE_INTERVAL:
        # Read BME280.
        temp_in = bme280.temperature
        # convert temperature (C->F)
        temp_in = temp_in * 1.8 + 32
        temp_in = temp_in + BME280_TEMP_OFFSET
        hum_in = bme280.humidity

        temp_out = bmp280.temperature
        temp_out = temp_out * 1.8 + 32
        temp_out = temp_out + BMP280_TEMP_OFFSET
        hum_out = None

        inside_temp_alert_low = temp_in
        inside_temp_alert_high = temp_in
        if temp_in <= INSIDE_TEMP_HIGH and temp_in >= INSIDE_TEMP_LOW:
            inside_temp_alert_normal = 100
        else:
            inside_temp_alert_normal = 0

        last_update = time.time()

def get_t_in():
    update_data()
    return round(temp_in,2) if temp_in is not None else None

def get_h_in():
    update_data()
    return round(hum_in,2) if hum_in is not None else None

def get_t_out():
    update_data()
    return round(temp_out,2) if temp_out is not None else None

def get_h_out():
    update_data()
    return round(hum_out,2) if hum_out is not None else None

def get_temp_alert_in_low():
    update_data()
    return inside_temp_alert_low

def get_temp_alert_in_high():
    update_data()
    return inside_temp_alert_high

def get_temp_alert_in_normal():
    update_data()
    return inside_temp_alert_normal


def main():

    # Put variable declarations here
    variables = {
        'Inside Temp': {
                'type': 'numeric',
                'bind': get_t_in
        },
        'Inside Humidity': {
                'type': 'numeric',
                'bind': get_h_in
        },
	'Outside Temp': {
		'type': 'numeric',
		'bind': get_t_out
	},
        'Inside Temp Alert Low': {
                'type': 'numeric',
                'bind': get_temp_alert_in_low
        },
        'Inside Temp Alert High': {
                'type': 'numeric',
                'bind': get_temp_alert_in_high
        },
        'Inside Temp Alert Normal': {
                'type': 'numeric',
                'bind': get_temp_alert_in_normal
        },
    }

    diagnostics = {
        'CPU Temp': 1,
        'IP Address': '111.111.111.111',
        'Host': 'one',
        'Operating System': 'oneOS',
    }

    device = cloud4rpi.connect(DEVICE_TOKEN)
    device.declare(variables)
    device.declare_diag(diagnostics)

    device.publish_config()

    # Adds a 1 second delay to ensure device variables are created
    time.sleep(1)

    try:
        data_timer = -1
        diag_timer = -1
        while True:
            if data_timer <= 0:
                device.publish_data()
                data_timer = DATA_SENDING_INTERVAL

            if diag_timer <= 0:
                device.publish_diag()
                diag_timer = DIAG_SENDING_INTERVAL

            time.sleep(POLL_INTERVAL)
            diag_timer -= POLL_INTERVAL
            data_timer -= POLL_INTERVAL

    except KeyboardInterrupt:
        cloud4rpi.log.info('Keyboard interrupt received. Stopping...')

    except Exception as e:
        error = cloud4rpi.get_error_message(e)
        cloud4rpi.log.error("ERROR! %s %s", error, sys.exc_info()[0])

    finally:
        sys.exit(0)


if __name__ == '__main__':
    main()
