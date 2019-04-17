def generate_video_rgb_histogram(self):
    # determine which frames to process for histograms
    frames_to_process = _get_frames_to_process(self.video_capture)

    # keep track of current frame ID to know to process it or not
    frame_counter = 0 
    
    hile self.video_capture.isOpened():
        # read capture frame by frame
        ret, frame = self.video_capture.read()
        if ret:
            frame_counter += 1
            if frame_counter in frames_to_process:
                for i, col in enumerate(self.colours):
                    histogram = cv2.calcHist([frame], [i], None, [256], [0, 256])
                    histogram = _normalize_histogram(histogram)
                    self.histograms_rgb_dict[col].append(histogram)
        else:
            break
    self.generate_and_store_average_rgb_histogram()