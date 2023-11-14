from numpy import dtype, array, recarray, float32, uint8, ndarray, str_
import numpy as np
import matplotlib.patches
import matplotlib.collections
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


@dataclass
class Canvas():
    sequence: list[Solution]    

    def swap(self, ind_1, ind_2):
        """
        given two indicies swap the position of the two Solutions
        """
        
        self.sequence[ind_1], self.sequence[ind_2] = self.sequence[ind_2], self.sequence[ind_1] 
        
        return None

    def how_many(self):
        """
        get how many solutions are in the sequence
        """
        return len(self.sequence)

    def get_index(self, _id):
        """
        get the index of a solution in the sequence by id
        """
        for c, val in enumerate(self.sequence):
            if val._id == _id:
                return c
            
        #NOTE: Case where the index is not found
        return -1 

    def mut_prob(self, _id):
        """
        get the mutability from a polygon by id, this should be the geometric 
        series 1/(2^i), where the i is the index of the id given 
        """

        return 1/(2**(1+self.get_index(_id)))


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

class Simulation():

    def __init__(self,**kwargs):
        """
        Init simulation.
        Keywords:
            - base image
            - output image
            - max generations
            - max iterations
            - stagnation limit
        """
        
        self.base_image       = kwargs.get("b_image")
        self.output_image     = kwargs.get("o_image")
        self.max_generations:int  = kwargs.get("m_gen",10)
        self.max_iterations:int   = kwargs.get("m_iter",10)
        self.stagnation_limit:int = kwargs.get("stag_lim",10)
        self.n_verticies:int = kwargs.get("n_vert",3)
        self.height:int = kwargs.get("height",32)
        self.width:int = kwargs.get("width",32)

    def _rand_solution(self, number)->Solution:
        """
        Create a random Solution
        """
        color = RGBA(r=np.random.random(), 
                             g=np.random.random(),
                             b=np.random.random(),
                             a=np.random.random(),)
            
        vertices = Vertex(array([np.random.randint(2) for _x in range(3)]),
                          array([np.random.randint(2) for _y in range(3)]))
        return Solution(vertices=vertices, color=color, _id=number)

    def _iteration(self,)->Solution:
        """
        Function that processes the current solution and applies mutation(s)
        """
        #Create iteration tracked variables
        
        return Solution()

    def _generation(self,):
        
        #Create generation tracked variables
            
        # initialize solution
        current_solution = self._rand_solution(1)

        for iter_ in range(self.max_iterations):
            self._iteration()
            pass
        pass

    def run(self,):
        """
        Run the simulation until completion.
        """
        
        #NOTE: there are generations where the best polygon is iterated through and searched for. 
        # iterations end if the counter is reached  
        
        

        #NOTE: polygon initialization
        
        #NOTE: Loop

        #NOTE: mutation

        #NOTE: Replacement

        #NOTE: polygon initialization
        #NOTE: end loop

        # NOTE: normalized optimiziation
        
        pass

    def get_results(self,):
        
        pass





if __name__ == "__main__":
    red = RGBA(1,1,1,1)
    print(red.r, type(red.r))
