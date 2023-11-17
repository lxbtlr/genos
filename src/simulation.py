from src.custom_types import Solution, Vertex, RGBA, Canvas
from src.reconstruction import polygon_init, polygon_mutate
from src.visualize import add_polygon

from numpy import array
import numpy as np


class Simulation:
    def __init__(self, **kwargs):
        """
        Init simulation.
        Keywords:
            - base image
            - output image
            - max generations
            - max iterations
            - stagnation limit
        """

        self.base_image = kwargs.get("b_image")
        self.output_image = kwargs.get("o_image")
        self.max_generations: int = kwargs.get("m_gen", 10)
        self.max_iterations: int = kwargs.get("m_iter", 10)
        self.stagnation_limit: int = kwargs.get("stag_lim", 10)
        self.n_vertices: int = kwargs.get("n_vert", 3)
        self.num_evals: int = kwargs.get("n_evals", 50000)
        self.height: int = kwargs.get("height", 32)
        self.width: int = kwargs.get("width", 32)

        # NOTE: this value is from the paper
        self.canvas = Canvas(list())
        self.counter = 0

    def mk_probabilities(self):
        """
        Choose a polygon to mutate weighted by the sequence probabilities
        """
        num = self.canvas.how_many()

        # Generate Geometric series of probabilities for the sequence
        probabilities = array([1 / (2 ** (1 + x)) for x in range(num)])

        # Normalize the probabilities to 1
        n_probabilities = probabilities / np.sum(probabilities)
        return n_probabilities

    def run(self):
        """
        Run the simulation until completion.
        """

        # initialize vars
        t = 0
        self.counter = 0

        # Create a new random polygon & add it to the canvas
        self.canvas = add_polygon(
            self.canvas, polygon_init(id=self.canvas.how_many())
        )
        probabilities = self.mk_probabilities()

        # TODO: get loss of current solution
        v_k = float(0.1)

        while t <= self.num_evals:
            polygon_i = np.random.choice(
                array(self.canvas.sequence), p=probabilities
            )

            self.canvas, new = polygon_mutate(self.canvas, polygon_i)

            # TODO: SCORE
            l_base = float(1)
            l_new = float(1)

            if l_new > l_base:
                self.counter += 1

            else:
                new = polygon_i
                self.counter = 0
            t += 1

            # NOTE: CHECK THIS
            if (self.counter > self.max_iterations) and (
                self.canvas.how_many() < self.max_generations
            ):
                if l_new < v_k:
                    polygon_i1 = polygon_init(id=self.canvas.how_many())

                    self.canvas = add_polygon(
                        canvas=self.canvas, polygon=polygon_i1
                    )

                    probabilities = self.mk_probabilities()
                else:
                    self.counter += 1

            if (self.counter > self.max_iterations) and (
                self.canvas.how_many() == self.max_generations
            ):
                # Once we reach the maximum number of generations, now we can
                # send the rest of our cycles optimizing all polygons
                probabilities = [
                    1 / self.max_generations
                ] * self.max_generations

    def get_results(self):
        pass
