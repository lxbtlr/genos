from argparse import ArgumentParser


parser = ArgumentParser(description="A Progressive Hill Climbing Image Reconstruction Script")

parser.add_argument('-b',"--base-image",type=str,
                    help="The path of the base image")

parser.add_argument('-o',"--output-image", type=str, 
                    help="The path of the output image")

# NOTE: could also look at implementing HSBA too
parser.add_argument('-c',"--color-mode",type=str,choices=["GRAY", "RGBA"],default="GRAY",
                    help="Specify the color-mode that will be used")

parser.add_argument('-g',"--max-generations",type=int,default=10,
                    help="Maximum number of generations")

parser.add_argument('-i',"--max-iterations",type=int,default=10,
                    help="Maximum number of iterations")

parser.add_argument('-s',"--stagnation-limit",type=int,default=100,
                    help="Max number of iterations allowed for stagnated solutions")

parser.add_argument('-d',"--debug",action="store_true",default=False,
                    help="Toggle the debug flag")

args = parser.parse_args()

#HACK: this allows for global flags to be passed onto other files
FLAGS = {"debug":args.debug, "axis":args.axis}
