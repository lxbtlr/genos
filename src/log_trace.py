import logging
import os
import sys
import time


def setup_logger(
    logger, *, name: str = "simulation", debug_level: bool = False, mode: bool = False
) -> logging.Logger:
    """
    Create a standardized logger for this module
    """
    log_format = "%(asctime)-8s :: %(module)-.8s :: %(levelname)-.1s :: %(message)s"
    if debug_level:
        logger.setLevel("INFO")
    else:
        logger.setLevel("DEBUG")

    formatter = logging.Formatter(log_format, datefmt="%H:%M:%S")

    file_handler = logging.FileHandler(filename=f"{name}.log", mode="w")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if mode == True:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    else:
        file_handler = logging.FileHandler(filename=f"{name}.log", mode="w")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def mk_folder_path(
    folder_name, *, sub_fldr_name: str = "-".join(time.ctime().split()[1:4])
) -> str:
    """
    Check to see if the folder exists, if not, make the folder.
    @return str The abs. path to the folder
    """

    script_loc = os.path.dirname(os.path.abspath(sys.argv[0]))
    folder_path = os.path.join(script_loc, f"{folder_name}", sub_fldr_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return folder_path


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger = setup_logger(logger)
    logger.info("This is a test")
    logger.debug("THIS IS  A DEBUG MSG")
