from src.simulation import Simulation
import src.log_trace
import logging

# import src.arg_parse
import time


# Create the simulation environment folder
START_TIME = "-".join(time.ctime().split()[1:4]).replace(":", ".")
simulation_data_folder = src.log_trace.mk_folder_path(
    folder_name="playground", sub_fldr_name=str(START_TIME)
)

logger = logging.getLogger(__name__)
logger = src.log_trace.setup_logger(
    logger,
    name="/".join([simulation_data_folder, "simulation"]),
    debug_level=False,
    mode=False,
)


if __name__ == "__main__":
    small_test_sim = Simulation(
        folder_path=simulation_data_folder,
        b_image="img/1.png",
        o_image="img/test_output.jpg",
        m_poly=50,
        stag_lim=30,
        n_evals=50000,
        min_save=True,
    )
    # run simulation
    logger.info("running sim")
    small_test_sim.run()

    small_test_sim.write_results()
