def __init__(self, directory, file_name):
    # dicts of lists to store histograms for each frame
    self.histograms_grey_dict = list()
    self.histograms_rgb_dict = {
        'b': list(),
        'g': list(),
        'r': list()
    }
    self.histograms_hsv_dict = list()

def generate_video_histogram(self):
    frame_counter = 0  # current frame ID to know to process it or not
    while self.video_capture.isOpened():
        # read capture frame by frame
        ret, frame = self.video_capture.read()
        if ret:
            frame_counter += 1
            # process one frame per second
            if frame_counter in _get_frames_to_process(self.video_capture):
                # Greyscale Histogram
                grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                histogram = cv2.calcHist([grey_frame], [0], None, [256], [0, 256])
                self.histograms_grey_dict.append(histogram)
                # RGB Histogram
                for i, col in enumerate(('b', 'g', 'r')):
                    histogram = cv2.calcHist([frame], [i], None, [256], [0, 256])
                    self.histograms_rgb_dict[col].append(histogram)
                #HSV Histogram
                hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                histogram = cv2.calcHist([hsv_frame], [0, 1, 2], None, self.bins, [0, 180, 0, 256, 0, 256])
                self.histograms_hsv_dict.append(histogram)
        else:
            break
    self.generate_and_store_average_histogram()