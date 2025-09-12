import matplotlib.pyplot as plt
from random_walk import RandomWalk  # pyright: ignore

# Keep making new walks, as long as the program is active
while True:
    # Make a random walk
    rw = RandomWalk()
    rw.fill_walk()

    # Plot the points in the walk
    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.tight_layout()
    point_numbers = range(rw.num_points)
    ax.scatter(
        rw.x_values,
        rw.y_values,
        c=point_numbers,
        cmap=plt.cm.Blues,  # pyright: ignore
        s=1,
    )
    ax.set_aspect("equal")

    # Emphasize the first and last points
    ax.scatter(0, 0, c="green", s=100)
    ax.scatter(rw.x_values[-1], rw.y_values[-1], c="red", s=100)

    # Remove the axes
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    plt.show()

    keep_running = input("Make another walk? (y/n): ")
    if keep_running == "n":
        break
