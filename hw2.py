"""
Source for programming assignment in hw 2 of CS 181 W20
Author: Rajan Saini

Assignment description:
    - [done] Take two pictures as input
    - Manually identify a set of corresponding points [done]
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
import cv2


class RawImage:
    def __init__(self, path, num_points, name):
        """
        Wrapper for OpenCV image
        """
        self.name = name
        self.image = cv2.imread(path)
        cv2.imshow(self.name, self.image)
        cv2.setMouseCallback(self.name, self.on_click)
        cv2.moveWindow(self.name, 0, 0)
        cv2.resizeWindow(self.name, 300, 300)

        # Possible states are WAITING, FINISHED
        self.state = "WAITING"

        # TODO Remove once list is finished
        # Keeps track of number of clicks seen
        self.clicks = 0

        # Stores the maximum number of points
        self.max_points = int(num_points)

        # Stores the coordinates clicked
        self.coords = []

    def on_click(self, event, x, y, flags, param):
        """
        Called when the image is clicked. Adds to the list of common
        coordinates if the list size is less than the maximum size and draws a
        dot. Otherwise, closes the image.
        """
        # Ensure we only process a click when an actual click happens
        if event != cv2.EVENT_LBUTTONDBLCLK:
            return

        self.coords.append((x, y))

        # TODO Draw dots on image

        if len(self.coords) == self.max_points:
            print(f"Coords: {self.coords}")
            # Remove callback
            cv2.setMouseCallback(self.name, lambda *args: None)

            # Transition to COMPUTING state
            self.state = "COMPUTING"

    def ready(self):
        return self.state != "WAITING"


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

    while not (left.ready() and right.ready()):
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
