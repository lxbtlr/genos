from src.custom_types import Solution, Vertex, RGBA, Canvas
from src.reconstruction import polygon_init, polygon_mutate 
from src.visualize import add_polygon
from src.loss import sad
from numpy import array
import numpy as np

class Simulation():

    def __init__(self,**kwargs):
        """
        Init simulation.
        Keywords:
            - Base image
            - Output image
            - Max generations
            - Max iterations
            - Stagnation limit
            - Number evaluations
            - Height
            - Width
            - Number Verticies
        """
        
        self.base_image:np.ndarray= kwargs.get("b_image",array([]))
        self.output_image         = kwargs.get("o_image")
        self.max_generations:int  = kwargs.get("m_gen",10)
        self.max_iterations:int   = kwargs.get("m_iter",10)
        self.stagnation_limit:int = kwargs.get("stag_lim",10)
        self.n_verticies:int      = kwargs.get("n_vert",3)
        self.num_evals:int        = kwargs.get("n_evals",50000) # NOTE: this value is from the paper
        
        # Derived class variables
        #TODO: make these defined by the base image
        self.height,self.width    =  self.base_image.shape        
        self.canvas = Canvas(list())

    def mk_probabilities(self,):
        """
        Choose a polygon to mutate weighted by the sequence probabilities
        """
        num = self.canvas.how_many()

        # Generate Geometric series of probabilities for the sequence
        probabilities = array([1/(2**(1+x)) for x in range(num)])
            
        # Normalize the probabilities to 1
        n_probabilities = probabilities / np.sum(probabilities)
        return

    def eval_loss(self, image):
        """
        Evaluate an image to the base_image and return the SAD
        """
        return sad(self.base_image, image)

    def run(self,):
        """
        Run the simulation until completion.
        """
        
        # initialize vars
        t= 0
        counter = 0
        
        # Create a new random polygon & add it to the canvas
        self.canvas = add_polygon(self.canvas,
                                  polygon_init(id=self.canvas.how_many()))
        probabilities = self.mk_probabilities()
     
        # get loss of current solution
        v_k = self.eval_loss(self.canvas.image()) 
            
        while t <= self.num_evals:
            indx, polygon_i = np.random.choice(list(enumerate(self.canvas.sequence)),p=probabilities)
                
            self.canvas, new = polygon_mutate(self.canvas,polygon_i)
            
            # compute the loss of the new iteration with the parent
            l_base = self.eval_loss(self.canvas.image())
            l_new = self.eval_loss(new)
            
            # compare the child with the parent
            if l_new < l_base:
                
                counter = 0
            else:
                
                new = polygon_i
                counter +=1
                    
            t += 1
            
            if (counter > self.max_iterations) and (self.canvas.how_many() < self.max_generations):
                    
                if l_new < v_k:
                    polygon_i1 = polygon_init(id=self.canvas.how_many())
                    
                    self.canvas = add_polygon(canvas=self.canvas, 
                                              polygon=polygon_i1)
                    counter = 0
                    probabilities = self.mk_probabilities()
                else:
                    
                    # reinit polygon
                    self.canvas.sequence[indx]  = polygon_init(id=self.canvas.how_many()) 
                    counter += 1
                    
            if (counter > self.max_iterations) and (self.canvas.how_many() == self.max_generations):
                # Once we reach the maximum number of generations, now we can send the rest of our cycles optimizing all polygons
                probabilities = [1/self.max_generations]*self.max_generations


    def get_results(self,):
        
        pass
