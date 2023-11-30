from src.simulation import Simulation

if __name__ == "__main__":
    small_test_sim = Simulation(
        b_image="img/test_base.jpg",
        o_image="img/test_output.jpg",
        m_poly=3,
        stag_lim=10,
        num_evals=5000,
    )
    # run simulation
    small_test_sim.run()

    # TODO: automate making an output folder with all simulation information such as args, photos, logs
    # write results
    small_test_sim.write_results()
