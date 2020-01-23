"""
Source for programming assignment in hw 2 of CS 181 W20
Author: Rajan Saini

Assignment description:
    - [done] Take two pictures as input
    - [done] Manually identify a set of corresponding points
      - [done] Color selected dots
    - Solve the homography problem (compute the H matrix)
      - [done] Create a system of equations
      - Solve using solution of minimal norm
    - Apply the transformation on one of the images in the pair to synthesize
      the other image, and vice versa
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

    # Solve for H


if __name__ == "__main__":
    """
    Argument parsing
    """
    leftimage = ''
    rightimage = ''

    # Number of common points
    num_points = 4

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hl:r:n:", ["limg=", "rimg="])
    except getopt.GetoptError:
        print("Usage: hw2.py -l <leftimage> -r <rightimage> -n <numpoints>")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-l", "--limg"):
            leftimage = arg
        elif opt in ("-r", "--rimg"):
            rightimage = arg
        elif opt in ("-n"):
            num_points = arg

    """
    Get coordinates
    (note to grader: RawImage and ginput are my own functions, implemented in
    helper.py)
    """
    left = RawImage(leftimage, num_points, "left")
    right = RawImage(rightimage, num_points, "right")

    coords = ginput(left, right)

    """
    Calculate H Matrix
    """
    get_H(coords[0], coords[1])
