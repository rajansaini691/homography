"""
Source for programming assignment in hw 2 of CS 181 W20
Author: Rajan Saini

Assignment description:
    - [done] Take two pictures as input
    - [done] Manually identify a set of corresponding points
      - [done] Color selected dots
    - Solve the homography problem (compute the H matrix)
      - [done] Create a system of equations
      - [done] Solve using solution of minimal norm
    - [done] Apply the transformation on one of the images in the pair to
      synthesize the other image, and vice versa
    - Repeat this for two other image pair examples

Report should contain:
    - The two image pairs
    - At least four corresponding points annotated, with labeled coordinates
    - Transformation parameters for each pair
    - Synthesized images
    - This source code (when complete)
"""
import sys
import getopt
import numpy as np
import cv2
from helpers import RawImage, ginput


def get_H(original, transformed):
    """
    Calculates the H matrix using the given coordinate pairs

    Parameters:
        original            Coordinates from the original image, that we are
                            trying to distort
        transformed         Coordinates from the transformed image, functioning
                            as our target
    """
    # The A matrix
    A = []

    # The b vector
    b = []

    # p and p_prime are individual coordinates
    for p, p_prime in zip(original, transformed):
        # Points from the original image
        x = p[0]
        y = p[1]

        # Points from the transformed image
        x_prime = p_prime[0]
        y_prime = p_prime[1]

        # Populate A
        A_i = [[x, y, 1, 0, 0, 0, -x*x_prime, -y*y_prime],
               [0, 0, 0, x, y, 1, -x*y_prime, -y*y]]
        A += A_i

        # Populate b
        b += [x_prime, y_prime]

    # Convert to np array
    A = np.array(A)
    b = np.array(b)

    # Calculate minimum norm solution for H
    h = np.linalg.lstsq(A, b, rcond=None)
    h = np.append(h[0], 1)
    h = h.reshape((3, 3))
    return h


if __name__ == "__main__":
    """
    Argument parsing
    """
    leftimage = ''
    rightimage = ''

    # Number of common points
    num_points = 4

    # Path to directory to generate the report
    report_path = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hl:r:n:", ["limg=", "rimg=",
                                   "data-path="])
    except getopt.GetoptError:
        print("""Usage: hw2.py -l <leftimage> -r <rightimage> -n <numpoints>
                 --data-path <path>""")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-l", "--limg"):
            leftimage = arg
        elif opt in ("-r", "--rimg"):
            rightimage = arg
        elif opt in ("-n"):
            num_points = arg
        elif opt in ("--data-path"):
            report_path = arg

    if report_path == "":
        print("woeijf")
        exit(1)
    else:
        print(report_path)

    """
    Get coordinates
    (note to grader: RawImage and ginput are my own functions, implemented in
    helper.py)
    """
    left = RawImage(leftimage, num_points, "left")
    right = RawImage(rightimage, num_points, "right")

    coords = ginput(left, right)

    """
    Calculate H Matrices going both ways
    """
    # Transforming left to right
    H_lr = get_H(coords[0], coords[1])

    # Transforming right to left
    H_rl = get_H(coords[1], coords[0])

    """
    Warp the images
    """
    left.transform(H_lr, right.image)
    right.transform(H_rl, left.image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    """
    Generate the report (puts all of the data into a single location)
    """
    left.write(report_path)
    right.write(report_path)

    f = open(report_path + "report.txt", "w")
    f.write("Points on the left image:\n")
    f.write(str(coords[0]))
    f.write("\n")
    f.write("Points on the right image:\n")
    f.write(str(coords[1]))
    f.write("\n")
    f.write("H matrix when transforming left to match right:\n")
    f.write(str(H_lr))
    f.write("\n")
    f.write("H matrix when transforming right to match left:\n")
    f.write(str(H_rl))
    f.write("\n")
    f.close()
