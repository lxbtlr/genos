from argparse import ArgumentParser
import src.log_trace
import logging


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
    "-p",
    "--max-polygons",
    type=int,
    default=10,
    help="Maximum number of generations & polygons",
)

parser.add_argument(
    "-e",
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
    "-m",
    "--min-save",
    action="store_true",
    default=False,
    help="Save only images that are improving the current generation's fitness score (default=False)",
)

parser.add_argument(
    "--stream-mode",
    action="store_true",
    default=False,
    help="Sets the logger handler mode where FALSE pushes the stream to a file and TRUE pushes the stream to the terminal (default=False)",
)

parser.add_argument(
    "-d",
    "--debug",
    action="store_true",
    default=False,
    help="Toggle the debug flag, this directly controls the minimum logging level of the logging handler (default=False)",
)

args = parser.parse_args()


# HACK: this allows for global flags to be passed onto other files
FLAGS = {"debug": args.debug}
