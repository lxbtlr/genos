from src.simulation import Simulation
import src.log_trace
import logging

logger = logging.getLogger(__name__)
logger = src.log_trace.setup_logger(logger)

if __name__ == "__main__":
    small_test_sim = Simulation(
        b_image="img/windows.jpg",
        o_image="img/test_output.jpg",
        m_poly=50,
        stag_lim=100,
        n_evals=50000,
    )
    # run simulation
    logger.info("running sim")
    small_test_sim.run()

    small_test_sim.write_results()
