from numpy import array, float32, ndarray
import numpy as np
import matplotlib.patches
import matplotlib.collections
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from typing import Iterator, Tuple


from dataclasses import dataclass
from numpy.typing import ArrayLike

# FIXME: import flags from argparse for colormode

DIMS = (64, 64)  # Default dimensions of the canvas


# RGBA Color
@dataclass
class RGBA:
    r: float32
    g: float32
    b: float32
    a: float32

    def __init__(self, r, g, b, a):
        self.r = float32(r)
        self.g = float32(g)
        self.b = float32(b)
        self.a = float32(a)

    def get_all(self) -> ndarray:
        return array((self.r, self.g, self.b, self.a))


@dataclass
class Vertices:
    """Dataclass representing vertices of a polygon"""

    x: ndarray
    y: ndarray

    def pairs(
        self,
    ) -> Iterator[Tuple[ArrayLike, ArrayLike]]:
        """
        Get x,y pairs
        """
        return zip(self.x, self.y)


@dataclass
class Polygon(matplotlib.patches.Polygon):
    """
    Datatype representing a single solution / polygon
    """

    def __init__(self, vertices: Vertices, color: RGBA, _id: int):
        super().__init__(
            xy=np.c_[vertices.x, vertices.y], color=color.get_all(), closed=True
        )
        self._id: int = _id

    @property
    def id(self):
        """id of the polygon"""
        return self._id


@dataclass
class Canvas:
    """
    Datatype representing a sequence of polygons on a canvas
    """

    sequence: list[Polygon]

    def swap(self, ind_1: int, ind_2: int) -> None:
        """
        given two indices swap the position of the two Polygons
        """

        self.sequence[ind_1], self.sequence[ind_2] = (
            self.sequence[ind_2],
            self.sequence[ind_1],
        )

    def how_many(self) -> int:
        """
        get how many polygons are in the sequence
        """
        return len(self.sequence)

    def get_index(self, _id: int):
        """
        get the index of a polygon in the sequence by id
        """
        for i, polygon in enumerate(self.sequence):
            if polygon.id == _id:
                return i

        # NOTE: Case where the index is not found
        return -1

    def replace_polygon(self, updated_polygon: Polygon) -> None:
        """
        update the polygon at the given index with an updated polygon
        """
        self.sequence[updated_polygon.id] = updated_polygon

    # def mut_prob(self, _id):
    #    """
    #    get the mutability from a polygon by id, this should be the geometric
    #    series 1/(2^i), where the i is the index of the id given
    #    """

    #    return 1/(2**(1+self.get_index(_id)))

    def get_order(self) -> list[int]:
        """
        get all id's of the polygons in the order they appear in the sequence
        """
        return array([i.id for i in self.sequence])

    def image(self):
        """
        Composite all polygons into an image
        """
        fig = Figure(figsize=(DIMS[0] / 100, DIMS[1] / 100), dpi=100)
        canvas_agg = FigureCanvasAgg(fig)

        ax = fig.add_subplot()
        ax.axis("off")
        ax.set_xlim(0, DIMS[0])
        ax.set_ylim(0, DIMS[1])
        ax.add_collection(
            matplotlib.collections.PatchCollection(self.sequence, match_original=True)
        )
        canvas_agg.draw()
        rgba = np.asarray(canvas_agg.buffer_rgba())

        return rgba[:, :, :3] / 255


if __name__ == "__main__":
    red = RGBA(1, 1, 1, 1)
    print(red.r, type(red.r))
