import board
import busio
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi

class ESP32:

    def __init__(self):
        self.esp = self._build_esp()

    def _build_esp(self):
        esp32_cs = DigitalInOut(board.ESP_CS)
        esp32_ready = DigitalInOut(board.ESP_BUSY)
        esp32_reset = DigitalInOut(board.ESP_RESET)
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
        return esp

    def device_info(self):
        info = {
            'firmware_version': self.esp.firmware_version,
            'MAC': [hex(i) for i in self.esp.MAC_address],
            'IP': self.esp.pretty_ip(self.esp.ip_address)
        }
        return info

    def list_aps(self):
        aps = {}
        for ap in self.esp.scan_networks():
            aps[str(ap['ssid'], 'utf-8')] = ap['rssi']
        return aps

    def connect_ap(self, secrets):
        while not self.esp.is_connected:
            try:
                self.esp.connect_AP(secrets["ssid"], secrets["password"])
            except OSError as e:
                print("Connection failed, retrying...", e)
                continue

    
