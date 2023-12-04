from src.simulation import Simulation
import src.log_trace
import logging

from src.arg_parse import args
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
    debug_level=args.debug,
    mode=args.stream_mode,
)


logger.debug(
    f"""Max Generations: {args.max_polygons}
Max Evaluations: {args.max_evaluations}
Stagnation Limits: {args.stagnation_limit}
Min Save: {args.min_save}
Debug State: {args.debug}"""
)


if __name__ == "__main__":
    small_test_sim = Simulation(
        folder_path=simulation_data_folder,
        b_image=args.base_image,
        o_image=args.output_image,
        m_poly=args.max_polygons,
        stag_lim=args.stagnation_limit,
        n_evals=args.max_evaluations,
        min_save=args.min_save,
    )
    # run simulation
    logger.info("running sim")
    small_test_sim.run()

    small_test_sim.write_results()
