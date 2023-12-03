from argparse import ArgumentParser
import src.log_trace
import logging

logger = logging.getLogger(__name__)
logger = src.log_trace.setup_logger(logger)

parser = ArgumentParser(
    description="A Progressive Hill Climbing Image Reconstruction Script"
)

parser.add_argument("-b", "--base-image", type=str, help="The path of the base image")

parser.add_argument(
    "-o", "--output-image", type=str, help="The path of the output image"
)

# NOTE: could also look at implementing HSBA too

# parser.add_argument(
#     "-c",
#     "--color-mode",
#     type=str,
#     choices=["GRAY", "RGBA"],
#     default="GRAY",
#     help="Specify the color-mode that will be used",
# )


parser.add_argument(
    "-g",
    "--max-polygons",
    type=int,
    default=10,
    help="Maximum number of generations & polygons",
)

parser.add_argument(
    "-i",
    "--max-evaluations",
    type=int,
    default=50000,
    help="Maximum number of evaluations in the simulation (default=50000)",
)

parser.add_argument(
    "-s",
    "--stagnation-limit",
    type=int,
    default=40,
    help="Max number of iterations allowed before a solution is considered 'stagnate'",
)

parser.add_argument(
    "-d", "--debug", action="store_true", default=False, help="Toggle the debug flag"
)

args = parser.parse_args()

logger.debug(
    f"""Max Generations: {args.max_polygons}
Max Evaluations: {args.max_evaluations}
Stagnation Limits: {args.stagnation_limit}
Debug State: {args.debug}"""
)

# HACK: this allows for global flags to be passed onto other files
FLAGS = {"debug": args.debug}
