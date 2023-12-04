from numpy import ndarray, absolute, count_nonzero, zeros, ones, sum
import matplotlib.pyplot as plt
import matplotlib.image as img


def image_diff(image1: ndarray, image2: ndarray) -> float:
    """
    Compute the absolute difference of two images
    """
    if image1.size != image2.size:
        raise Exception("Images must be of the same size")

    abs_diff_mat = absolute(image1 - image2)
    percentage = (count_nonzero(abs_diff_mat) * 100) / abs_diff_mat.size

    return percentage


def sad(image1: ndarray, image2: ndarray):
    """
    Sum of all absolute pixel differences into one value, as defined in the paper

    img1= [[1,2,3],
           [4,5,6],
           [7,8,9]]

    img2= [[9,8,7],
           [6,5,4],
           [3,2,1]]

    out = sum([sum(absolute(image1[pos]-image2[pos]))
               for pos in range(len(img1))]
    """

    diff = absolute(image1 - image2)

    return sum(diff)


def complete_percent(base_image: ndarray, comp_image: ndarray, l_func=sad) -> float:
    """
    Compute the complete percentage loss metric

    This value is the difference between the maximum loss between the base image
    and the canvas, minus the loss of the comparison and base images, normalized
    as a percentage.
    """

    blank = zeros(base_image.shape)
    max_l = l_func(base_image, blank)

    if max_l == 0:
        raise Exception(
            "The images provided are identical,\npreventing divide by 0 error"
        )
    l_best = l_func(base_image, comp_image)
    # print(f"Complete Loss: {l_func.__name__}")
    # print(f"max_diff: {max_l}")
    # print(f"l_best: {l_best}")

    return (absolute(max_l - l_best) / max_l) * 100


if __name__ == "__main__":
    # test case of comparing two images
    one = img.imread("../img/1.png")
    diamond = img.imread("../img/diamond.png")
    b = zeros(one.shape)
    w = ones(one.shape)

    print(one.shape)
    print("ORIGINAL INTERPRETATION")
    print("absdiff of:\n\twhite, black:", complete_percent(w, b, image_diff))
    print("absdiff of:\n\twhite, 1.png", complete_percent(w, one, image_diff))
    print(
        "absdiff of:\n\tblack, diamond.png",
        complete_percent(diamond, zeros(diamond.shape), image_diff),
    )
    print(
        "absdiff of:\n\twhite, diamond.png",
        complete_percent(diamond, ones(diamond.shape), image_diff),
    )

    print("PAPER LOSS FUNCTION")
    print("absdiff of:\n\twhite, black:", complete_percent(w, b))
    print("absdiff of:\n\twhite, 1.png", complete_percent(w, one))
    print(
        "absdiff of:\n\tblack, diamond.png",
        complete_percent(diamond, zeros(diamond.shape)),
    )
    print(
        "absdiff of:\n\twhite, diamond.png",
        complete_percent(
            diamond,
            ones(diamond.shape),
        ),
    )

    print("SAD")
    print(
        "absdiff of:\n\twhite, diamond.png",
        complete_percent(diamond, ones(diamond.shape), sad),
    )
    print(
        "absdiff of:\n\tblack, diamond.png",
        complete_percent(diamond, zeros(diamond.shape), sad),
    )

    windows = img.imread("../img/windows.jpg")
    blk = zeros(windows.shape)
    wht = ones(windows.shape)
    print(f"SAD of windows img and black: {sad(windows,blk)}")
    print(f"SAD of windows img and white: {sad(windows,wht)}")
    print(f"SAD of windows img and one: {sad(windows,one)}")
# check to see if opacity should weight the color values for comparison (SAD may not work as expected)
