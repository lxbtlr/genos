import logging
import os
import sys
import time


def setup_logger() -> logging.Logger:
    """
    Create a standardized logger for this module
    """
    log_format = "%(asctime)s :: %(name)s :: %(module)s :: %(levelname)s :: %(message)s"

    logger = logging.getLogger(__name__)
    logger.setLevel("DEBUG")

    file_handler = logging.FileHandler(filename="simulation.log", mode="a")
    logger.addHandler(file_handler)

    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)

    return logger


def mk_folder_path(
    folder_name, *, sub_fldr_name: str = "-".join(time.ctime().split()[1:4])
) -> str:
    """
    Check to see if the folder exists, if not, make the folder.
    @return str The abs. path to the folder
    """

    # TODO: check this with Carrie to make sure it will play nice with cluster
    script_loc = os.path.dirname(os.path.abspath(sys.argv[0]))
    folder_path = os.path.join(script_loc, f"{folder_name}", sub_fldr_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return folder_path


if __name__ == "__main__":
    logger = setup_logger()
    logger.info("This is a test")
    logger.debug("THIS IS  A DEBUG MSG")
