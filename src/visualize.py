import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from types1 import Canvas, Solution, Vertex, RGBA

DIMS = (64, 64)
N_VERTICES_TRI = 3


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


def create_polygon(solution: Solution) -> Polygon:
    """
    Create a Polygon object from a Solution
    """
    polygon = Polygon(
        xy=np.c_[solution.vertices.x, solution.vertices.y],
        closed=True,
        color=solution.color.get_all() / 255,  # Normalize RGBA values from 0-255 to 0-1
    )
    return polygon


def add_polygon(canvas: Canvas, polygon: Polygon) -> Canvas:
    """
    Add a polygon to the canvas
    """
    canvas.sequence.append(polygon)
    return canvas


if __name__ == "__main__":
    canvas = Canvas([])

    for i in range(10):
        solution = Solution(
            N_VERTICES_TRI,
            Vertex(np.random.rand(3, 1) * DIMS[0], np.random.rand(3, 1) * DIMS[1]),
            RGBA(
                np.random.rand() * 255,
                np.random.rand() * 255,
                np.random.rand() * 255,
                100,
            ),
        )
        canvas = add_polygon(canvas, create_polygon(solution))

    visualize_canvas(canvas)
