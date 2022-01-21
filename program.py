import serial
import sys
import subprocess
import json

PANEL_DEVICE = sys.argv[1]

def main():
  print(f"Opening serial connection to {PANEL_DEVICE}", flush=True)
  ser = serial.Serial()
  ser.port=PANEL_DEVICE
  ser.baudrate=9600
  ser.timeout=2
  ser.parity=serial.PARITY_NONE
  ser.stopbits=serial.STOPBITS_ONE
  ser.bytesize=serial.EIGHTBITS
  ser.xonxoff=serial.XOFF
  ser.rtscts=False
  ser.dsrdtr=False

  ser.open()
  
  handlers = {
    "motion": onMotion
  }

  while True:
    #read the next line
    data = ser.readline()
    if len(data) > 0:
      try:
        command = json.loads(data.decode('UTF-8'))
        handlers[command["command"]](command["value"])
      except Exception as ex:
        print(f"Error processing command. {ex=}")

def onMotion(value):
  if value:
    subprocess.call("xset dpms force on", shell=True)
    print('Turn monitor on')


main()
