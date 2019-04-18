def __init__(self, directory, file_name):
    # ...
    # read the video and store the histograms for each frame per colour channel in a dict
    self.histograms_rgb_dict = {
        'b': list(),
        'g': list(),
        'r': list()
    }
    # ...

def generate_video_rgb_histogram(self):
    # keep track of current frame ID to know to process it or not
    frame_counter = 0 
    
    while self.video_capture.isOpened():
        # read capture frame by frame
        ret, frame = self.video_capture.read()
        if ret:
            frame_counter += 1
            # process one frame per second
            if frame_counter in _get_frames_to_process(self.video_capture):
                for i, col in enumerate(('b', 'g', 'r')):
                    histogram = cv2.calcHist([frame], [i], None, [256], [0, 256])
                    histogram = _normalize_histogram(histogram)
                    self.histograms_rgb_dict[col].append(histogram)
        else:
            break
    self.generate_and_store_average_rgb_histogram()