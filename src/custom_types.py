from numpy import dtype, array, recarray, float32, uint8, ndarray, str_
import numpy as np
import matplotlib.patches
import matplotlib.collections
from dataclasses import dataclass
from numpy.typing import ArrayLike

# FIXME: import flags from argparse for colormode


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
class Vertex:
    x: ndarray
    y: ndarray

    def pairs(
        self,
    ):
        """
        Get x,y pairs
        """
        return zip(self.x, self.y)


@dataclass
class Polygon(matplotlib.patches.Polygon):
    """
    Datatype representing a single solution / polygon
    """

    def __init__(self, vertices: Vertex, color: RGBA, _id: int):
        super().__init__(
            xy=np.c_[vertices.x, vertices.y], color=color.get_all(), closed=True
        )
        self._id: int = _id


@dataclass
class Canvas:
    sequence: list[Polygon]

    def swap(self, ind_1, ind_2):
        """
        given two indicies swap the position of the two Polygons
        """

        self.sequence[ind_1], self.sequence[ind_2] = (
            self.sequence[ind_2],
            self.sequence[ind_1],
        )

        return None

    def how_many(self):
        """
        get how many polygons are in the sequence
        """
        return len(self.sequence)

    def get_index(self, _id):
        """
        get the index of a polygon in the sequence by id
        """
        for c, val in enumerate(self.sequence):
            if val._id == _id:
                return c

        # NOTE: Case where the index is not found
        return -1

    def replace_polygon(self, updated_polygon: Polygon):
        """
        update the polygon at the given index with an updated polygon
        """
        self.sequence[updated_polygon._id] = updated_polygon
        pass

    # def mut_prob(self, _id):
    #    """
    #    get the mutability from a polygon by id, this should be the geometric
    #    series 1/(2^i), where the i is the index of the id given
    #    """

    #    return 1/(2**(1+self.get_index(_id)))

    def get_order(self):
        """
        get all id's of the sequence in the order they appear
        """

        return array([i._id for i in self.sequence])

    def image(self):
        """
        Composite all polygons into an image
        """

        return


if __name__ == "__main__":
    red = RGBA(1, 1, 1, 1)
    print(red.r, type(red.r))
