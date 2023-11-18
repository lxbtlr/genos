from src.custom_types import Solution, Vertex, RGBA, Canvas
from src.reconstruction import polygon_init, polygon_mutate 
from src.visualize import add_polygon, visualize_canvas
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
        
        self.counter = 0
        self.create_polygon()

    def update_probabilities(self,):
        """
        Choose a polygon to mutate weighted by the sequence probabilities
        """
        num = self.canvas.how_many()

        # Generate Geometric series of probabilities for the sequence
        probabilities = array([1/(2**(1+x)) for x in range(num)])
            
        # Normalize the probabilities to 1
        n_probabilities = probabilities / np.sum(probabilities)
        
        self.probabilities = n_probabilities
        return n_probabilities

    def norm_opti_probs(self,):
        """
        Create a uniform distribution with mg elements, where mg is the max 
        generations / max number of polygons 
        """
        self.probabilities = [1/self.max_generations]*self.max_generations
        return self.probabilities

    def eval_loss(self, image):
        """
        Evaluate an image to the base_image and return the SAD
        """
        return sad(self.base_image, image)

    def cc_loss(self,):
        """
        Compute and compare loss
        param
            child - 

        return
            float - base loss
            float - child loss
        """
        
        # compute the loss of the child iteration with the parent
        l_parent = self.eval_loss(self.canvas.image())
        l_child = self.eval_loss(self.child)
        
        # compare loss
        if l_child < l_parent:
            
            self.counter = 0
        else:
            
            self.child = self.polygon_i
            self.counter +=1
        
        return l_parent, l_child

    def select(self,):
        """
        Using probabilities, randomly select and return a polygon from the 
        canvas sequence and its index
        """
        indx, self.polygon_i = np.random.choice(
                list(enumerate(self.canvas.sequence)),
                p=self.probabilities)
            
        return indx, self.polygon_i

    def create_polygon(self,):
        """
        Create polygon and add it to the canvas
        """
        
        self.canvas = add_polygon(canvas=self.canvas, 
                                  polygon=polygon_init(
                                      id=self.canvas.how_many()))
            
        self.counter = 0
        self.update_probabilities()
        return

    def run(self,):
        """
        Run the simulation until completion.
        """
        
        # initialize vars
        t= 0
        
        # get loss of current solution
        v_k = self.eval_loss(self.canvas.image()) 
            
        while t <= self.num_evals:
            # TODO: make this a method
            indx, self.polygon_i = self.select()
            
            self.canvas, self.child = polygon_mutate(self.canvas,self.polygon_i)
            
            # compare and compute the child with the parent loss
            l_child, l_parent = self.cc_loss()
                
            t += 1
            
            if (self.counter > self.max_iterations) and (self.canvas.how_many() < self.max_generations):
                    
                if l_child < v_k:
                    self.create_polygon()
                else:
                    
                    # reinit polygon
                    # TODO: make this a method
                    self.canvas.sequence[indx] = polygon_init(id=self.canvas.how_many()) 
                    self.counter += 1
                    
            if (self.counter > self.max_iterations) and (self.canvas.how_many() == self.max_generations):
                # Once we reach the maximum number of generations, now we can send the rest of our cycles optimizing all polygons
                self.norm_opti_probs()            
            # TODO: incorporate logging at end of loop cycle to track sim status

    def get_results(self,):
        """
        Save the results of the simulation to disk
        """
        return visualize_canvas(self.canvas)
