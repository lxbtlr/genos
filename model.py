from src.arg_parse import args
from src.simulation import Simulation
import src.log_trace

import logging
import time


# Create the simulation environment folder
START_TIME = "-".join(time.ctime().split()[1:4]).replace(":", ".")
simulation_data_folder = src.log_trace.mk_folder_path(
    folder_name="playground", sub_fldr_name=str(START_TIME)
)

# NOTE: Create logger and set the log file in the simulation environment we just made
logger = logging.getLogger(__name__)
logger = src.log_trace.setup_logger(
    logger, name="/".join([simulation_data_folder, "simulation"])
)
if __name__ == "__main__":
    sim = Simulation(
        folder_path=simulation_data_folder,
        b_image=args.base_image,
        o_image=args.output_image,
        m_poly=args.max_polygons,
        stag_lim=args.stagnation_limit,
        num_evals=args.max_evaluations,
        min_save=args.min_save,
    )
    # run simulation
    sim.run()

    # TODO: automate making an output folder with all simulation information such as args, photos, logs
    # write results
    sim.write_results()
