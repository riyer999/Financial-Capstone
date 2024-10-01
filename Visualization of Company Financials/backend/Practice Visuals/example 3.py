import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Create the figure and axis
fig, ax = plt.subplots(figsize=(6, 6))

# Set limits for the axis
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Draw static parts of the scale (center rod and beam)
rod, = ax.plot([0.5, 0.5], [0.3, 0.9], color='black', lw=5)  # Vertical rod
beam, = ax.plot([0.2, 0.8], [0.8, 0.8], color='black', lw=5)  # Horizontal beam

# Draw the left and right plates
left_plate = plt.Rectangle((0.15, 0.7), 0.1, 0.05, color='gray')  # Left plate
right_plate = plt.Rectangle((0.75, 0.7), 0.1, 0.05, color='gray')  # Right plate
ax.add_patch(left_plate)
ax.add_patch(right_plate)

# Function to animate the balance scale
def animate(i):
    shift = 0.05 * (i % 20 - 10) / 10  # Calculate shift based on frame number

    # Adjust the beam (horizontal part) position
    beam.set_data([0.2, 0.8], [0.8 + shift, 0.8 - shift])

    # Adjust the positions of the plates
    left_plate.set_xy((0.15, 0.7 + shift))
    right_plate.set_xy((0.75, 0.7 - shift))

    return rod, beam, left_plate, right_plate

# Set up the animation
ani = animation.FuncAnimation(fig, animate, frames=40, interval=100, blit=True)

# Show the animation
plt.title('Balance Scale Animation')
plt.show()
