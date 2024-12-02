#python送信側

import socket
import random
import time
import json
import random

HOST = '127.0.0.1'
PORT = 50007

akari_pan = 0
akari_tilt = 0
text = ["akari", "AKARI", "Hello, akari"]

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    data = {
        "message": "Hello, from server!",
        "timestamp": time.time(),
        "pan": 0.0,
        "tilt": 0.0,
        "text": "TEXT"
    }    

    while True:
        #a = random.uniform(0, 30)
        #result = str(a)
        akari_pan = random.uniform(-90, 90)
        akari_tilt = random.uniform(-90, 90)
        akari_text = random.choice(text)
        data["pan"] = akari_pan
        data["tilt"] = akari_tilt
        data["text"] = akari_text
        print(data)
        json_data = json.dumps(data).encode('utf-8')
        client.sendto(json_data,(HOST,PORT))
        time.sleep(1.0)
    
if __name__ == '__main__':
    main()
