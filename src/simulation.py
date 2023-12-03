from src.custom_types import Polygon, Vertices, RGBA, Canvas
from src.reconstruction import polygon_mutate
from src.visualize import add_polygon

import matplotlib.pyplot as mpl
import matplotlib.patches
import matplotlib.collections
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

from src.loss import complete_percent, sad
from PIL import Image
from copy import deepcopy
import src.log_trace
import logging
from numpy import array
import numpy as np
import time
import os
import sys


_logger = logging.getLogger("__main__")
logger = _logger.getChild(__name__)
# logger = src.log_trace.setup_logger(logger)


class Simulation:
    def __init__(self, folder_path, **kwargs):
        """
        Init simulation.
        Keywords:
            - Base image
            - Output image
            - Max generations / polygons
            - Stagnation limit
            - Number evaluations
            - Number Verticies
        """
        self.base_image: np.ndarray = np.asarray(Image.open(kwargs.get("b_image")))
        self.max_polygons: int = kwargs.get("m_poly", 10)
        self.stagnation_limit: int = kwargs.get("stag_lim", 10)
        self.n_verticies: int = kwargs.get("n_vert", 3)
        self.num_evals: int = kwargs.get("n_evals", 50000)

        # NOTE: this value is from the paper
        # Derived class variables
        self.height, self.width = self.base_image.shape[:2]
        self.canvas = Canvas(list())
        self.counter = 0
        self.canvas = self.create_polygon(self.canvas)

        self.folder_path = folder_path
        logger.info(f"Initialize simulation")

    def update_probabilities(
        self,
    ):
        """
        Choose a polygon to mutate weighted by the sequence probabilities
        """
        num = self.canvas.how_many()

        # Generate Geometric series of probabilities for the sequence
        probabilities = array([1 / (2 ** (1 + (num - 1 - x))) for x in range(num)])

        # Normalize the probabilities to 1
        n_probabilities = probabilities / np.sum(probabilities)
        self.probabilities = n_probabilities
        logger.debug(f"Probabilities updated, now: {self.probabilities}")
        return n_probabilities

    def norm_opti_probs(
        self,
    ):
        """
        Create a uniform distribution with mg elements, where mg is the max
        generations / max number of polygons
        """
        self.probabilities = [1 / self.max_polygons] * self.max_polygons
        return self.probabilities

    def eval_loss(self, image: Canvas):
        """
        Evaluate an image to the base_image and return the SAD
        """
        return sad(self.base_image, image.image())

    def cc_loss(self, parent: Canvas, child: Canvas) -> tuple[float, float]:
        """
        Compute and compare loss
        """

        # compute the loss of the child iteration with the parent
        l_parent = self.eval_loss(parent)
        l_child = self.eval_loss(child)

        logger.debug(f"parent: {l_parent} | child: {l_child}")
        return l_parent, l_child

    def select(
        self,
    ):
        """
        Using probabilities, randomly select and return a polygon from the
        canvas sequence and its index
        """
        selected_polygon: Polygon = np.random.choice(
            self.canvas.sequence, p=self.probabilities
        )
        indx = self.canvas.get_index(selected_polygon.id)

        logger.debug(
            f"Polgon selected: {selected_polygon.id}, indx: {indx}, (p={self.probabilities}) "
        )
        return indx, selected_polygon

    def create_polygon(self, c: Canvas):
        """
        Create polygon and add it to the canvas
        """
        picked_verts = vertices_em(
            self.base_image,
            self.canvas.image(),
        )
        polygon = Polygon(
            picked_verts,
            RGBA(
                np.random.rand(),
                np.random.rand(),
                np.random.rand(),
                np.random.rand(),
            ),
            _id=c.how_many(),
        )
        c = add_polygon(canvas=c, polygon=polygon)

        # self.counter = 0
        self.update_probabilities()
        return c

    def run(
        self,
    ):
        """
        Run the simulation until completion.
        """

        # initialize vars
        t = 0

        generations = [self.canvas]

        newer_solution = None
        older_solution = None
        # get loss of current solution
        v_k = self.eval_loss(self.canvas)
        # print(self.num_evals)
        logger.info(f"Running Simulation, baseline loss: {v_k}")

        while t <= self.num_evals:
            logger.info(
                f"time:{t}, Polygons: {self.canvas.how_many()}, baseline loss {v_k}"
            )
            _indx, selected_polygon = self.select()

            # use temporary variables to store previous and current solutions
            older_solution = deepcopy(self.canvas)
            newer_solution = polygon_mutate(self.canvas, selected_polygon)

            # compare and compute the child with the parent loss
            l_parent, l_child = self.cc_loss(older_solution, newer_solution)

            # compare loss
            if l_child < l_parent:
                self.counter = 0
                # pushing the better solution
                self.canvas = newer_solution
            else:
                self.counter += 1
                # keep the old canvas
                self.canvas = older_solution

            t += 1

            if (self.counter > self.stagnation_limit) and (
                self.canvas.how_many() < self.max_polygons
            ):
                logger.info("Stagnation counter over threshold")
                if l_parent < v_k:
                    logger.warn("Child solution improves on parent, adding new polygon")
                    # update the canvas to the improved version
                    generations.append(deepcopy(self.canvas))
                    self.canvas = self.create_polygon(self.canvas)

                    v_k = l_parent
                    self.counter = 0

                    logger.info(f"reseting counter, new baseline: {v_k}")
                else:
                    logger.info(
                        "Child solution does not improve on parent, reinit. polygon"
                    )
                    # reinit polygon
                    #  This is attempting to perform a rollback
                    previous_generation = generations[-1]
                    # reinitializing a polygon onto the canvas
                    # TODO: implement EM here

                    picked_verts = vertices_em(
                        self.base_image,
                        previous_generation.image(),
                    )

                    reinit_polygon = Polygon(
                        picked_verts,
                        RGBA(
                            np.random.rand(),
                            np.random.rand(),
                            np.random.rand(),
                            np.random.rand(),
                        ),
                        _id=previous_generation.how_many(),
                    )
                    self.canvas = add_polygon(
                        canvas=previous_generation, polygon=reinit_polygon
                    )

                    self.update_probabilities()
                    # keep pushing the counter up
                    self.counter += 1

            if (self.counter > self.stagnation_limit) and (
                self.canvas.how_many() == self.max_polygons
            ):
                logger.warn("Stagnation counter over threshold, max polygons reached")
                # Once we reach the maximum number of generations, now we can
                # send the rest of our cycles optimizing all polygons
                self.norm_opti_probs()
            # TODO: incorporate logging at end of loop cycle to track sim status

            # NOTE: this is for debugging purposes
            fig = Figure(figsize=(self.width / 100, self.height / 100), dpi=100)
            canvas_agg = FigureCanvasAgg(fig)

            ax = fig.add_subplot()
            ax.axis("off")
            ax.set_xlim(0, self.width)
            ax.set_ylim(0, self.height)
            ax.add_collection(
                matplotlib.collections.PatchCollection(
                    self.canvas.sequence, match_original=True
                )
            )
            canvas_agg.draw()
            canvas_agg.print_figure(
                f"{self.folder_path}/{str(t).zfill(len(str(self.num_evals)))}.png",
                bbox_inches="tight",
            )

        logger.warn("Simulation Complete")

    def write_results(
        self,
        generations: bool = False,
    ):
        """
        Save the results of the simulation to disk
        if generations is made true, save all the saved generations up to the final result
        """

        fig = Figure(figsize=(self.width / 100, self.height / 100), dpi=100)
        canvas_agg = FigureCanvasAgg(fig)

        ax = fig.add_subplot()
        ax.axis("off")
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.add_collection(
            matplotlib.collections.PatchCollection(
                self.canvas.sequence, match_original=True
            )
        )
        mpl.savefig(self.folder_path + "/output.png", bbox_inches="tight")
        # visualize_canvas(self.canvas)

        if generations:
            pass

        # TODO: add mkfldr
        # TODO: save images to dir
        # TODO: save other simulation data to that folder
        return


def make_folder_path(
    folder_name="img", *, START_TIME: str = "-".join(time.ctime().split()[1:4])
) -> str:
    """
    Check to see if the folder exists, if not make the folder.
    @return str The abs. path to the folder
    """

    script_loc = os.path.dirname(os.path.abspath(sys.argv[0]))
    folder_path = os.path.join(script_loc, f"{folder_name}", START_TIME)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def get_energy_map(source: np.ndarray, recon: np.ndarray) -> np.ndarray:
    """
    Computes the energy map.

    Args:
        source (np.ndarray): Source image as ndarray.
        recon (np.ndarray): Reconstructed image as ndarray.

    Returns:
        np.ndarray: Supplementary matrix of cumulative energy values of each
        pixel.
    """
    # Compute for total difference
    cumulative_e = np.sum(np.absolute(source - recon))

    # Compute for pixel-wise probability
    pixel_e = 0
    for channel in [0, 1, 2]:
        pixel_e += np.absolute(source[:, :, channel] - recon[:, :, channel])

    prob_matrix = pixel_e / cumulative_e

    # Supplementary matrix is the cumulative sum of probabilities
    supp_matrix = prob_matrix.cumsum().reshape(source.shape[:2])

    return supp_matrix


def vertices_em(source: np.ndarray, recon: np.ndarray, n_vertices: int = 3) -> Vertices:
    """

    Args:
        source (np.ndarray): Source image as ndarray.
        recon (np.ndarray): Reconstructed image as ndarray.
        n_vertices (int): Number of vertices. Defaults to

    Returns:
        Vertices: A set of vertices chosen based on the energy map.
    """
    matrix = get_energy_map(source, recon)
    x = []
    y = []
    for _ in range(n_vertices):
        threshold = np.random.rand()
        raw_index = np.argmax(matrix > threshold)

        # TODO: check if this is relevant in final logs
        logger.debug(f"Raw Index: {raw_index}")
        x_new = raw_index // source.shape[0]
        y_new = raw_index % source.shape[1]
        x.append(x_new)
        y.append(y_new)
    logger.debug("Energy Mapping finished")
    point = Vertices(np.array(x), np.array(y))
    logger.debug(point)
    return point
