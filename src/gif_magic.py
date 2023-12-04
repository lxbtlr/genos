import os
import subprocess
from argparse import ArgumentParser

parser = ArgumentParser(description="A script to make gifs")

parser.add_argument(
    "-i",
    "--input-dir",
    default=".",
    type=str,
    help="The path of the input images (will assume all files in this directory are to be used for the gif)",
)

parser.add_argument(
    "-o",
    "--output-dir",
    default="~",
    type=str,
    help="The path of where the output will be generated, default (~)",
)

parser.add_argument(
    "-d", "--delay", default=1, type=str, help="the delay between frames of the gif"
)

args = parser.parse_args()


def create_gif(input_dir, output_file, delay=0.1):
    # Check if the input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return

    # Get a list of image files in the input directory
    image_files = sorted(
        [
            f
            for f in os.listdir(input_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))
        ]
    )

    if not image_files:
        print(f"No image files found in '{input_dir}'.")
        return

    # Construct the ImageMagick command
    convert_command = [
        "convert",  # The ImageMagick command
        "-delay",
        str(delay),  # Set the delay between frames in milliseconds
        os.path.join(input_dir, "*"),  # Input image files path
        output_file,  # Output GIF file
    ]

    try:
        # Run the ImageMagick command
        subprocess.run(convert_command, check=True)
        print(f"GIF created: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating GIF: {e}")


if __name__ == "__main__":
    input_directory = args.input_dir  # Replace with your input directory
    output_filename = "/".join(
        [args.output_dir, "output.gif"]
    )  # Replace with your output GIF filename
    frame_delay = args.delay  # Delay between frames in milliseconds

    create_gif(input_directory, output_filename, frame_delay)
