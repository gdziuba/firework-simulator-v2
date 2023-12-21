import pyaudio

# Set the device ID to the ID of the microphone you want to use
input_device_index = 2  # Using the "Microphone (Mic in at front panel (black))"

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the input stream with the selected device
input_stream = p.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=44100,
                      input=True,
                      input_device_index=input_device_index,
                      frames_per_buffer=1024)

# Open the output stream
output_stream = p.open(format=pyaudio.paInt16,
                       channels=1,
                       rate=44100,
                       output=True)

print("Starting, speak into the microphone")
try:
    while True:
        # Read data from the input stream
        data = input_stream.read(1024)
        
        # Play back the data on the output stream
        output_stream.write(data)
except KeyboardInterrupt:
    print("Finished")

# Stop and close the streams
input_stream.stop_stream()
input_stream.close()
output_stream.stop_stream()
output_stream.close()

# Terminate PyAudio
p.terminate()
