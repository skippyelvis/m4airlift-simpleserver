import adafruit_esp32spi.adafruit_esp32spi_wsgiserver as server
from adafruit_wsgi.wsgi_app import WSGIApp
from secrets import secrets
from esp32 import ESP32

esp = ESP32()
esp.connect_ap(secrets)
print(esp.device_info()['IP'])

web_app = WSGIApp()

@web_app.route("/health")
def health(request):  
    print("healthy!")
    return ("200 OK", [], "healthy!")

# Here we setup our server, passing in our web_app as the application
server.set_interface(esp.esp)
wsgiServer = server.WSGIServer(80, application=web_app)

# Start the server
wsgiServer.start()
while True:
    try:
        wsgiServer.update_poll()
    except (ValueError, RuntimeError) as e:
        print("Failed to update server, restarting ESP32\n", e)
        esp.connect_ap(secrets)
        continue

