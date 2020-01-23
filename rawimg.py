import cv2
"""
Helper class to do all of the tedious interaction with OpenCV, like window
management, event handling, waiting for user input. The goal is to provide the
same interface as matlab, so that in the future I won't have to do any of the
ugly stuff below.
"""


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

        # Adds to list of coords
        self.coords.append((x, y))

        # Draws a different-colored circle on each selected coordinate
        b = 255 / self.max_points * len(self.coords)
        g = 255 - b
        dot_color = (b, g, 0)
        cv2.circle(self.image, (x, y), 3, dot_color, -1, cv2.LINE_AA)
        cv2.imshow(self.name, self.image)

        # Transition out when enough points have been selectd
        if len(self.coords) == self.max_points:
            print(f"Coords: {self.coords}")
            # Remove callback
            cv2.setMouseCallback(self.name, lambda *args: None)

            self.state = "COMPUTING"

    def ready(self):
        return self.state != "WAITING"


def ginput(left_image, right_image):
    """
    Functions like matlab's ginput, using OpenCV and the above RawImage class
    as a backend.

    Returns a tuple of the form (left_coords, right_coords), where the coords
    hold the coordinates of the points clicked by the user.
    """
    while not (left_image.ready() and right_image.ready()):
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
    return (left_image.coords, right_image.coords)
