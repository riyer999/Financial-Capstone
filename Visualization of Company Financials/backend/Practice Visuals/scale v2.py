import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Create figure and axis
fig, ax = plt.subplots()

# Draw the base of the scale
base = patches.Rectangle((-0.1, -0.5), 0.2, 0.05, linewidth=2, edgecolor='black', facecolor='black')
ax.add_patch(base)

# Draw the vertical bar
vertical_bar = patches.Rectangle((-0.02, -0.5), 0.04, 1, linewidth=2, edgecolor='black', facecolor='black')
ax.add_patch(vertical_bar)

# Draw the tilted arm of the scale
ax.plot([-0.6, 0], [0.5, 0.4], color='black', linewidth=2)  # Left arm
ax.plot([0, 0.6], [0.4, 0.5], color='black', linewidth=2)  # Right arm

# Draw the left string and bowl
ax.plot([-0.6, -0.6], [0.35, 0.5], color='black', linewidth=2)  # Left string
left_bowl = patches.Arc((-0.6, 0.3), 0.2, 0.1, angle=0, theta1=0, theta2=180, linewidth=2, edgecolor='black')
ax.add_patch(left_bowl)

# Draw the right string and bowl
ax.plot([0.6, 0.6], [0.35, 0.5], color='black', linewidth=2)  # Right string
right_bowl = patches.Arc((0.6, 0.3), 0.2, 0.1, angle=0, theta1=0, theta2=180, linewidth=2, edgecolor='black')
ax.add_patch(right_bowl)

# Set the limits and aspect ratio
ax.set_xlim([-1, 1])
ax.set_ylim([-0.6, 1])
ax.set_aspect('equal')

# Hide the axes
ax.axis('off')

# Show the plot
plt.show()
