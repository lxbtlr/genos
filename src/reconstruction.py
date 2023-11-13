import numpy as np
from matplotlib.patches import Polygon
from src.custom_types import Canvas, Solution, Vertex, RGBA

DIMS = (64, 64)
N_VERTICES_TRI = 3


def polygon_init(
    n_vertices: int = N_VERTICES_TRI, bounds: tuple[int, int] = DIMS, id: int
) -> Polygon:
    """
    Create a random Polygon object.

    Args:
        n_vertices (int): Number of vertices for the polygon. Defaults to 3
          (triangle).
        bounds (tuple[int, int]): Bounds of the canvas in (x, y). Defaults to
          (64, 64).
        id (int): ID of the polygon.

    Returns:
        Polygon: Polygon object.
    """
    # TODO: incorporate energy map into this
    solution = Solution(
        Vertex(
            np.random.rand(n_vertices, 1) * bounds[0],
            np.random.rand(n_vertices, 1) * bounds[1],
        ),
        RGBA(
            np.random.rand(),
            np.random.rand(),
            np.random.rand(),
            np.random.rand(),
        ),
        id
    )
    return solution


def polygon_mutate(canvas: Canvas, polygon: Polygon) -> Polygon:
    """
    Mutate a Polygon object.

    There are 3 possible mutation mechanisms:
    1. Mutate a vertex
    2. Mutate one of RGBA values
    3. Mutate the sequence of polygons

    Args:
        polygon (Polygon): Polygon object to mutate.

    Returns:
        Polygon: Mutated Polygon object.
    """
    mode = np.random.randint(3)

    if mode == 0:
        polygon = mutate_vertex(polygon)
    elif mode == 1:
        polygon = mutate_color(polygon)
    else:
        # Mutate the sequence of polygons
        n_polygons = len(canvas.sequence)
        # Select a random polygon to swap with
        swap_idx = np.random.randint(n_polygons)
        # Swap the polygons
        # FIXME: id is not defined yet -- need a way to keep track of the order
        canvas.swap(polygon.id, swap_idx)

    return canvas, polygon


def mutate_vertex(polygon: Polygon, bounds: tuple[int, int] = DIMS) -> Polygon:
    """
    Mutate a vertex of a Polygon object.

    There are 4 possible vertex mutation mechanisms:
    - Mutate the x coordinate of a vertex
        1. Mutation by a random scaled increment
        2. Mutation by a random number in bound
    - Mutate the y coordinate of a vertex
        3. Mutation by a random scaled increment
        4. Mutation by a random number in bound

    Args:
        polygon (Polygon): Polygon object to mutate.

    Returns:
        Polygon: Mutated Polygon object.
    """

    def change_value(value: float, bound: int):
        mode = np.random.randint(2)
        if mode:
            # Mutate by a scaled increment
            increment = check_bound(np.random.randint(0.1 * bound), value, bound)
            value += increment
        else:
            # Mutate by a number in bound
            value = np.random.randint(bound + 1)
        return value

    vertex_idx = np.random.randint(len(polygon.xy))
    if np.random.randint(2):
        # Mutate x
        polygon.xy[vertex_idx][0] = (
            change_value(polygon.xy[vertex_idx][0], bounds[0]),
            polygon.xy[vertex_idx][1],
        )
    else:
        # Mutate y
        polygon.xy[vertex_idx][1] = (
            polygon.xy[vertex_idx][0],
            change_value(polygon.xy[vertex_idx][1], bounds[1]),
        )

    # If the first vertex is selected, we need to update the last vertex as well
    if vertex_idx == 0:
        polygon.xy[-1] = polygon.xy[vertex_idx]
    return polygon


def check_bound(
    increment: int | float,
    value: int | float,
    bound: int,
) -> int | float:
    """
    Check if a value within bounds after increment.

    If the point is out of bounds, it increment will be used as a decrement.
    This function is for x, y coordinates, and color values.

    Args:
        increment (int | value): Increment to use.
        value (int | float): Value to check.
        bounds (int): Upper bound of the canvas for x or y, or of colors.

    Returns:
        int | float: Adjusted increment.
    """
    if value + increment <= bound:
        return increment
    return -increment


def mutate_color(polygon: Polygon) -> Polygon:
    """
    Mutate one of the RGBA values of a Polygon object.

    There are 8 possible color mutation mechanisms:
    - Mutate the red value of a polygon
        1. Mutation by a random scaled increment
        2. Mutation by a random number in bound
    - Mutate the green value of a polygon
        3. Mutation by a random scaled increment
        4. Mutation by a random number in bound
    - Mutate the blue value of a polygon
        5. Mutation by a random scaled increment
        6. Mutation by a random number in bound
    - Mutate the alpha value of a polygon
        7. Mutation by a random scaled increment
        8. Mutation by a random number in bound

    Args:
        polygon (Polygon): Polygon object to mutate.

    Returns:
        Polygon: Mutated Polygon object.
    """

    def change_value(value: float):
        mode = np.random.randint(2)
        if mode == 0:
            # Mutate by a scaled increment
            increment = check_bound(np.random.uniform(0, 0.1), value, 1)
            value += increment
        else:
            # Mutate by a number in bound
            value = np.random.rand()
        return value

    rgba = list(polygon.get_facecolor())
    color_idx = np.random.randint(4)
    rgba[color_idx] = change_value(rgba[color_idx])
    polygon.set_color(rgba)

    return polygon
