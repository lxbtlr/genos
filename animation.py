import os
import re
import imageio


def create_timelapse(directory_path):
    # Get a list of all PNG files in the directory
    png_files = [file for file in os.listdir(directory_path) if file.endswith(".png")]

    # Sort the files numerically using a regular expression to extract numbers
    png_files.sort(
        key=lambda x: int(re.search(r"\d+", x).group())
        if re.search(r"\d+", x)
        else float("inf")
    )

    # Create a list to store the images
    images = []

    # Read each image and append it to the list
    for png_file in png_files:
        image_path = os.path.join(directory_path, png_file)
        images.append(imageio.imread(image_path))

    # Save the images as a video (you can adjust the fps parameter)
    imageio.mimsave(f"{directory_path}/animation.mp4", images, fps=30)


if __name__ == "__main__":
    # Specify the directory path containing PNG files
    input_directory = "./playground/Dec-3-21.50.53/"

    # Specify the output path for the timelapse video
    output_video_path = "timelapse.mp4"

    # Create the timelapse
    create_timelapse(input_directory)
