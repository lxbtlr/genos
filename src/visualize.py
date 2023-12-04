import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from src.custom_types import Canvas, Polygon, Vertices, RGBA

DIMS = (64, 64)


def visualize_canvas(canvas: Canvas) -> None:
    """
    Draw polygons on canvas
    """
    polygons = PatchCollection(canvas.sequence, match_original=True)
    _, ax = plt.subplots()
    # Add the polygon patch to the axis
    ax.add_collection(polygons)
    # Set axis limits
    ax.set_xlim(0, DIMS[0])
    ax.set_ylim(0, DIMS[1])
    # Display the plot
    plt.show()


def add_polygon(canvas: Canvas, polygon: Polygon) -> Canvas:
    """
    Add a polygon to the canvas
    """
    canvas.sequence.append(polygon)
    return canvas


if __name__ == "__main__":
    canvas = Canvas([])

    for i in range(10):
        polygon = Polygon(
            Vertices(np.random.rand(3, 1) * DIMS[0], np.random.rand(3, 1) * DIMS[1]),
            RGBA(
                np.random.rand(),
                np.random.rand(),
                np.random.rand(),
                np.random.rand(),
            ),
            _id=i,
        )
        canvas = add_polygon(canvas, polygon)

    visualize_canvas(canvas)
