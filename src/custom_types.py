from numpy import dtype, array, recarray, float32, uint8, ndarray, str_
import numpy as np
import matplotlib.patches
from dataclasses import dataclass
from numpy.typing import ArrayLike

#FIXME: import flags from argparse for colormode

# RGBA Color
@dataclass
class RGBA():
    r:float32
    g:float32
    b:float32
    a:float32
    
    def __init__(self,r,g,b,a):
        self.r = float32(r)
        self.g = float32(g)
        self.b = float32(b)
        self.a = float32(a)

    def get_all(self)-> ndarray:
        return array((self.r,self.g,self.b,self.a))

@dataclass
class Vertex():
    x:ndarray
    y:ndarray

    def pairs(self,):
        """
        Get x,y pairs
        """
        return zip(self.x,self.y)
    

@dataclass
class Solution(matplotlib.patches.Polygon):
    """
    Datatype representing a single solution / polygon
    """
    def __init__(self, vertices:Vertex, color:RGBA, _id:int):
        
        super().__init__(xy=np.c_[vertices.x, vertices.y], 
                       color=color.get_all(),
                       closed=True)
        self._id:int = _id

        #self.vertices = vertices
        #self.nvertices = uint8(nvertices)
        #self.color = color




@dataclass
class Canvas():
    sequence: list[Solution]
    

    def swap(self, ind_1, ind_2):
        """
        given two indicies swap the position of the two Solutions
        """
        self.sequence[ind_1], self.sequence[ind_2] = self.sequence[ind_2], self.sequence[ind_1] 
        return None

    def image(self):
        """
        Composite all polygons into an image
        """
        
        return


if __name__ == "__main__":
    red = RGBA(1,1,1,1)
    print(red.r, type(red.r))
