# Music to Fireworks

Let's celebrate 2023 in style.

There are 4 parts to this project.  We leveraged an opensource project called Fireworks Simulator v2.  Thanks to Caleb Miller for making this available.

## MQTT server 

You can you an existing MQTT server or setup one yourself.  I leveraged [Mosquitto](https://mosquitto.org/) for this application.  You can use on of your choice, this is just the one that I have the most experience with.  

I am not using any authentication for this application, but feel free to add it if you would like.


## Audio Capture

This is a python application that is 3 parts.  

Make a venv environment
```
python -m venv audio
```
Windows:
```
\audio\Scripts\activate
pip install -r requirements.txt
```

To see audiodevice on computer run:
```
python audiodevices.py
```

To test to see if you have audio coming through.  Be careful and be ready to turn off in case of feedback.  This will allow you to identify what source you want to select.
```
python testdevice.py
```

Once you have identified your sources correctly.  You will need to configure the program to those inputs. This can be configured in the run.py file.  Change **input_device_index** to your audio input.

```stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True, input_device_index=2)```

Configure your MQTT inputs:

```
mqtt_broker = "192.168.222.150"  # Replace with your MQTT broker address
mqtt_port = 1883  # Replace with your MQTT broker port
mqtt_topic = "/fireworks"  # Replace with your desired topic
```


I needed to install a couple of tool from VB-Audio so that I could capture audio from my computer.

[VB-AUDIO](https://vb-audio.com/Voicemeeter/)

[VB-CABLE](https://vb-audio.com/Cable/)

Run the code:

```
python run.py
```


##  Firework Simulator v2

Run the following to install Node Modules from the Fireworks Directory:
```
npm install
```

Configure your broker that you would like to use:

```const mqttClient = mqtt.connect('mqtt://192.168.222.150:1883');```

To run the code:

```
node  .\basic_node_server.js
```

Navigate to **localhost:3000** to see your fireworks.

Play your music to fire off fireworks with the beat of the song.

## Node-RED dashboard 

[Node-RED Flow](https://flows.nodered.org/flow/8483e33bd3e57c775813bca4d0b57057)

[Current Song being Played - Haven't Tested](https://flows.nodered.org/flow/a559bbb4e17e99392c9a4757d442f308)