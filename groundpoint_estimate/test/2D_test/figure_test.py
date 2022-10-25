import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig = plt.figure(figsize=[5,5])
ax = plt.axes()

# fc = face color, ec = edge color
# c = patches.Circle(xy=(0, 0), radius=0.5, fc='g', ec='r')
# e = patches.Ellipse(xy=(-0.25, 0), width=0.5, height=0.25, fc='b', ec='y')
body = patches.Rectangle(xy=(-69, -128), width=138, height=150, ec='#000000', fill=False)
left_arm = patches.Rectangle(xy=(-90, -20), width=13.2, height=126, ec='#000000', fill=False)
right_arm = patches.Rectangle(xy=(76.8, -20), width=13.2, height=126, ec='#000000', fill=False)
# r = patches.Rectangle(xy=(0, 0), width=0.25, height=0.5, ec='#000000', fill=False)

plt.minorticks_on()
ax.grid(which="major",alpha=0.6)
ax.grid(which="minor",alpha=0.3)
ax.add_patch(body)
ax.add_patch(left_arm)
ax.add_patch(right_arm)

plt.axis('scaled')
ax.set_aspect('equal')

plt.show()
