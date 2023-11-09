from numpy import dtype, array, recarray, uint8, ndarray
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
class Polygon():
    nvertices:uint8
    vertices:ArrayLike
    color:ArrayLike

#HACK: currently only using RGBA, move to using *ARGS and toggle how they are
# used by the argparse colormode flag
def color(r,g,b,a):
    Color = dtype({'names': ['r', 'g', 'b','a'],
                   'formats': ['B', 'B','B', 'B',]}) 
    arr = array((r,g,b,a),dtype=Color)
    return arr.view(recarray)

if __name__ == "__main__":
    print(color(1,1,1,1))
