import numpy as np
from matplotlib.patches import Polygon
import logging
from src.custom_types import Canvas, Polygon, Vertices, RGBA
from copy import deepcopy

DIMS = (64, 64)
N_VERTICES_TRI = 3


logger = logging.getLogger(__name__)


def polygon_init(
    id: int, n_vertices: int = N_VERTICES_TRI, bounds: tuple[int, int] = DIMS
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
    polygon = Polygon(
        Vertices(
            np.random.rand(n_vertices, 1) * bounds[0],
            np.random.rand(n_vertices, 1) * bounds[1],
        ),
        RGBA(
            np.random.rand(),
            np.random.rand(),
            np.random.rand(),
            np.random.rand(),
        ),
        _id=id,
    )
    return polygon


def polygon_mutate(canvas: Canvas, polygon: Polygon) -> Canvas:
    """
    Mutate a Polygon object.

    There are 3 possible mutation mechanisms:
    1. Mutate a vertex
    2. Mutate one of RGBA values
    3. Mutate the sequence of polygons

    Args:
        polygon: Polygon object to mutate.

    Returns:
        Canvas: Copy of the canvas object with the mutated polygon object.
    """
    mode = np.random.randint(low=0, high=3)
    canvas_copy = deepcopy(canvas)
    polygon_copy = deepcopy(polygon)
    if mode == 0:
        polygon_copy = mutate_vertex(polygon_copy)
        canvas_copy.replace_polygon(polygon_copy)
    elif mode == 1:
        polygon_copy = mutate_color(polygon_copy)
        canvas_copy.replace_polygon(polygon_copy)
    else:
        # Mutate the sequence of polygons
        n_polygons = len(canvas_copy.sequence)
        # Select a random polygon to swap with
        swap_idx = np.random.randint(low=0, high=n_polygons)
        # Swap the polygons
        # FIXME: id is not defined yet -- need a way to keep track of the order
        canvas_copy.swap(polygon_copy.id, swap_idx)

    # TODO: add the new polygon to a copy of the canvas and return that canvas copy
    return canvas_copy


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
        polygon: Polygon object to mutate.

    Returns:
        Polygon: Mutated Polygon object.
    """

    def change_value(value: float, bound: int):
        mode = np.random.randint(low=0, high=2)
        if mode:
            increment = np.random.uniform(0, 0.1) * bound
            if np.random.rand() < 0.5:
                increment = -increment
            increment = check_bound(increment, value, bound)
            value += increment
        else:
            # Mutate by a number in bound
            value = np.random.randint(low=0, high=bound + 1)
        return value

    # print(polygon.xy)
    vertex_idx = np.random.randint(low=0, high=len(polygon.xy))
    logger.debug(f"Vertex chosen: {vertex_idx}")
    old_polygon_vertex = polygon.xy[vertex_idx]
    if np.random.randint(low=0, high=2):
        # Mutate x
        # Changed this to only assign a new value to the chosen coord
        polygon.xy[vertex_idx][0] = change_value(polygon.xy[vertex_idx][0], bounds[0])

        logger.debug(
            f"Vertex mutation (X): was {old_polygon_vertex[0]} now {polygon.xy[vertex_idx][0]}"
        )
    else:
        # Mutate y
        polygon.xy[vertex_idx][1] = change_value(polygon.xy[vertex_idx][1], bounds[1])
        logger.debug(
            f"Vertex mutation (Y): was {old_polygon_vertex[1]} now {polygon.xy[vertex_idx][1]}"
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
    if value + increment <= bound and value + increment >= 0:
        logger.debug(f"Bounds: increment ({increment}) is in bounds")
        return increment
    logger.debug(f"Bounds: increment ({increment}) is out of bounds")
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
        polygon: Polygon object to mutate.

    Returns:
        Polygon: Mutated Polygon object.
    """
    change = ""

    def change_value(value: float):
        mode = np.random.randint(low=0, high=2)
        if mode == 0:
            # Mutate by a scaled increment
            increment = np.random.uniform(0, 0.1)
            if np.random.rand() < 0.5:
                increment = -increment
            increment = check_bound(increment, value, 1)
            value += increment
        else:
            # Mutate by a number in bound
            value = np.random.rand()
        return value

    rgba = deepcopy(list(polygon.get_facecolor()))
    old_rgba = rgba
    color_idx = np.random.randint(low=0, high=4)
    rgba[color_idx] = change_value(rgba[color_idx])
    if color_idx == 3:
        # If alpha is mutated, we need to update the polygon color
        alpha = change_value(rgba[3])
        logger.debug(f"Color mutation (alpha): was {rgba[3]} now {alpha}")
        polygon.set_alpha(alpha)
    else:
        rgb = tuple(rgba[:3])
        polygon.set_facecolor(rgb)
        logger.debug(f"Color mutation: was {old_rgba} now {rgb}")
    return polygon
