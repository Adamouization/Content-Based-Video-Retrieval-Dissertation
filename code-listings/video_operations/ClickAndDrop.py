import cv2

class ClickAndDrop:
    window_name = "Crop the recording (top-left click -> bottom-right drop) - 'C' to crop - 'R' to restart"

    def __init__(self, thumbnail):
        """Loads image to crop + controls the callback loop."""
        self.thumbnail = thumbnail
        self.reference_points = list()
        self.cropping = False

        # load image, clone it, setup the mouse callback
        self.image = cv2.resize(self.thumbnail, (1280, 720), interpolation=cv2.INTER_AREA)
        clone = self.image.copy()
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.click_and_crop)

        # keep looping until the 'q' key is pressed
        while True:
            # display the image and wait for a keypress
            cv2.imshow(self.window_name, self.image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("r"):  # reset the cropping region
                self.image = clone.copy()
            elif key == ord("c"):  # break from the loop
                break

        # crop the ROI from the image
        if len(self.reference_points) == 2:
            self.roi = clone[self.reference_points[0][1]:self.reference_points[1][1],
                             self.reference_points[0][0]:self.reference_points[1][0]]
        cv2.destroyAllWindows()

    def click_and_crop(self, event, x, y, flags, param):
        """
        Callback function for user to manually crop image.
        NOTE: must crop from top-left corner to bottom-right corner
        """
        # if left mouse button clicked, record the starting (x, y) coordinates and indicate that cropping is being performed
        if event == cv2.EVENT_LBUTTONDOWN:
            self.reference_points = [(x, y)]
            self.cropping = True

        # check if left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record ending (x, y) coordinates and indicate that the cropping operation is finished
            self.reference_points.append((x, y))
            self.cropping = False

            # draw a rectangle around the region of interest
            cv2.rectangle(self.image, self.reference_points[0], self.reference_points[1], (0, 255, 0), 2)
            cv2.imshow(self.window_name, self.image)

    def get_roi(self):
        return self.roi

    def get_reference_points(self):
        return self.reference_points  # ROI reference points