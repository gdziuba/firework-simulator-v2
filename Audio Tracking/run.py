import pyaudio
import numpy as np
import time
import json
import paho.mqtt.client as mqtt
from collections import deque

# MQTT configuration
mqtt_broker = "192.168.222.150"  # Replace with your MQTT broker address
mqtt_port = 1883  # Replace with your MQTT broker port
mqtt_topic = "/fireworks"  # Replace with your desired topic

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream with a specific input device
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True, input_device_index=2)

# Initialize a deque to store recent volume levels
volume_buffer = deque(maxlen=200)  # Adjust maxlen as needed

# Time of the last trigger
last_trigger_time = 0

def process_audio(data, buffer):
    # Calculate the current volume
    volume = np.average(np.abs(data))

    # Append the current volume to the buffer
    buffer.append(volume)

    # Calculate the rolling average and standard deviation
    if len(buffer) == buffer.maxlen:  # Ensure buffer is full for accurate calculations
        rolling_avg = np.mean(buffer)
        std_dev = np.std(buffer)

        # Define thresholds
        thresholds = [rolling_avg + (std_dev * 0.75), 
                      rolling_avg + (std_dev * 1.5), 
                      rolling_avg + (std_dev * 2.25), 
                      rolling_avg + (std_dev * 3)]

        # Determine the special bit based on volume
        special_bit = 0
        for i, threshold in enumerate(thresholds):
            if volume > threshold:
                special_bit = i

        # Check for basic condition
        basic_condition = 0.01 < volume > thresholds[0] and 0.01 < volume < thresholds[1]

        return basic_condition, special_bit, volume
    else:
        return False, 0, volume


# Create an MQTT client instance
mqtt_client = mqtt.Client()

# Connect to the MQTT broker
mqtt_client.connect(mqtt_broker, mqtt_port, 60)

def send_trigger(volume, special_bit):
    # Convert NumPy float32 to native Python float
    volume_native = float(volume)

    # Prepare the message payload
    payload = {'volume': volume_native, 'special': special_bit}

    # Convert the payload to a JSON string
    payload_json = json.dumps(payload)

    # Publish the JSON string to the MQTT broker
    mqtt_client.publish(mqtt_topic, payload_json)

try:
    while True:
        # Read data from the stream
        try:
            data = stream.read(1024, exception_on_overflow=False)
            np_data = np.frombuffer(data, dtype=np.float32)

            # Process the audio data
            basic_condition, special_bit, volume = process_audio(np_data, volume_buffer)
            current_time = time.time()
            if (current_time - last_trigger_time > 0.3) and (basic_condition or (volume > 0.01 and special_bit > 0)):
                send_trigger(volume, special_bit)
                last_trigger_time = current_time
        except Exception as e:
            print(f"Error reading stream: {e}")
            break
except KeyboardInterrupt:
    print("Stopping stream")

# Close the stream
stream.stop_stream()
stream.close()
p.terminate()
