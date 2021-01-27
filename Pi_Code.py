import time
#import RPi.GPIO as GPIO
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging


direc = 24
step = 23

totalSteps = 200

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(direc, GPIO.OUT)
# GPIO.setup(step, GPIO.OUT)


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length)

        message = post_data.decode('utf-8')

        motorSplit = message.split('.')

        if motorSplit[0] == 'pitch':
            moveOptions = motorSplit[1].split('=')
            print(moveOptions)

            if moveOptions[0] == 'Set':
                print('blah')
            elif moveOptions[0] == 'Inc':
                print('blah')

        elif motorSplit[0] == 'yaw':
            moveOptions = motorSplit[1].split('=')
            print(moveOptions)

            if moveOptions[0] == 'Set':
                print('blah')
            elif moveOptions[0] == 'Inc':
                print('blah')


        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    #GPIO.cleanup()
    logging.info('Stopping httpd...\n')



if __name__ == '__main__':
    run()


# try:
#   while True:
#     steps = input("Input a number\n")
#     try:
#       steps = int(steps)
#     except:
#       print("An error occurred. Make sure your input is an int.")
#     else:
#       GPIO.output(direc, GPIO.HIGH)
#       if (steps<0):
#         GPIO.output(direc, GPIO.LOW)
#         steps = steps*(-1)
      
#       for i in range(0, steps):
#         GPIO.output(step, GPIO.HIGH)
#         time.sleep(0.005)
#         GPIO.output(step, GPIO.LOW)
#         time.sleep(0.005)
#     print()

# # When you press ctrl+c, this will be called
# finally:
  