from numpy import dtype, array, recarray, uint8, ndarray, str_
from dataclasses import dataclass
from numpy.typing import ArrayLike

#FIXME: import flags from argparse for colormode

# RGBA Color
@dataclass
class RGBA():
    r:uint8
    g:uint8
    b:uint8
    a:uint8
    
    def __init__(self,r,g,b,a):
        self.r = uint8(r)
        self.g = uint8(g)
        self.b = uint8(b)
        self.a = uint8(a)

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
class Solution():
    """
    Datatype representing a single solution / polygon
    """
    nvertices:uint8
    vertices:ArrayLike
    color:RGBA
    
    def __init__(self, nvertices, vertices, color):
        
        self.vertices = vertices
        self.nvertices = uint8(nvertices)
        self.color = color



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
