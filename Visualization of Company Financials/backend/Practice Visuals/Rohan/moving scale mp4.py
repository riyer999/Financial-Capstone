import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
from matplotlib import animation
import numpy as np

# Set up the figure and axis
fig, ax = plt.subplots()
x = range(30)
y = [0] * 30
bars = ax.bar(x, y, color="blue")
ax.set_ylim(0, 10)  # Set the y-axis limits

# Update function for the animation
def update(i):
    y[i] = np.random.randint(0, 10)  # Generate a random height for each bar
    bars[i].set_height(y[i])  # Update the height of the corresponding bar

# Create the animation and assign it to a variable
anim = FuncAnimation(fig, update, frames=len(bars), interval=100)  # Use len(bars) for frames
# Display the animation
plt.show()
matplotlib.rcParams['animation.ffmpeg_path'] = "C:\\Users\\RIyer\\Downloads\\ffmpeg-7.1-essentials_build\\ffmpeg-7.1-essentials_build\\bin\\ffmpeg.exe"
writer = animation.FFMpegWriter(fps=1, metadata=dict(artist="Rohan"), bitrate = 1800)

# Save the animation
anim.save('Line Graph Animation.mp4')

# Optionally, display the plot window
#plt.show()



#"C:\Users\RIyer\Downloads\ffmpeg-7.1-essentials_build\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe"

