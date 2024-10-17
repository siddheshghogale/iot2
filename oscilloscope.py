import time
import matplotlib.pyplot as plt
from Adafruit_ADS1x15 import ADS1115

# Create an ADS1115 ADC (16-bit) instance on the specified I2C bus.vdd=3.3,sda=3,scl=5,
adc = ADS1115(busnum=1)  # Change busnum to 0 if you're using an older Raspberry Pi

# Set the gain
GAIN = 1  # Change this based on your input range

# Initialize a list to store the ADC values
data = [[] for _ in range(4)]  # One list for each channel
time_data = []

# Set up the plot
plt.ion()  # Enable interactive mode
fig, ax = plt.subplots()
lines = [ax.plot([], [])[0] for _ in range(4)]
ax.set_xlim(0, 10)  # Set x-axis limit (adjust as needed)
ax.set_ylim(0, 32767)  # Set y-axis limit for 16-bit ADC
ax.set_xlabel('Time (s)')
ax.set_ylabel('ADC Value')
ax.set_title('Real-time ADC Readings')
ax.legend(['Ch 0'])

print('Reading ADS1115 values, press Ctrl-C to quit...')
print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
print('-' * 37)

start_time = time.time()

# Main loop.
while True:
    try:
        # Read all the ADC channel values in a list.
        values = [adc.read_adc(i, gain=GAIN) for i in range(1)]
        
        # Record time data
        current_time = time.time() - start_time
        time_data.append(current_time)
        
        # Update the data for each channel
        for i in range(1):
            data[i].append(values[i])

        # Update the plots
        for i in range(1):
            lines[i].set_data(time_data, data[i])
        
        # Adjust x-axis limit if necessary
        if current_time > 10:  # After 10 seconds, scroll the x-axis
            ax.set_xlim(current_time - 10, current_time)

        plt.draw()
        plt.pause(0.5)  # Pause to allow the plot to update

        # Print the ADC values.
        print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
        
    except Exception as e:
        print(f'Error reading ADC: {e}')
    
    # Pause for half a second.
    time.sleep(0.5)
