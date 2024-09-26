import matplotlib.pyplot as plt

# Create the figure and axis
fig, ax = plt.subplots()

# Drawing the balance scale
ax.plot([0.5, 0.5], [0, 1], color='black', linewidth=2)  # The balance beam
ax.plot([0.2, 0.8], [1, 1], color='black', linewidth=4)  # The horizontal bar

# Draw weights (total revenue vs. expenses)
ax.barh(1.1, width=0.3, left=0.5, color='blue')  # Total revenue
ax.barh(0.9, width=0.25, left=0.4, color='red')  # Cost of revenue

# Set labels and adjust layout
ax.text(0.5, 1.15, 'Total Revenue', ha='center')
ax.text(0.25, 0.85, 'Cost of Revenue', ha='center')

plt.xlim(0, 1)
plt.ylim(0, 1.2)
plt.show()
