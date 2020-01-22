"""
Source for programming assignment in hw 2 of CS 181 W20
Author: Rajan Saini

Assignment description:
    - [done] Take two pictures as input
    - [done] Manually identify a set of corresponding points
    - Solve the homography problem (compute the H matrix)
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
from rawimg import RawImage, ginput


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
    """
    left = RawImage(leftimage, num_points, "left")
    right = RawImage(rightimage, num_points, "right")

    coords = ginput(left, right)
