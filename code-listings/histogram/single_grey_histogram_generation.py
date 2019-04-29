def generate_video_greyscale_histogram(self, is_query=False):
    frame_counter = 0  # cur frame ID
    while self.video_capture.isOpened():
        ret, frame = self.video_capture.read()
        if ret:
            if is_query and frame_counter == 0:
                cad = ClickAndDrop(frame)
                self.reference_points = cad.get_reference_points()
            frame_counter += 1
            if frame_counter in _get_frames_to_process(self.video_capture):
                if is_query and len(self.reference_points) == 2:
                    roi = frame[self.reference_points[0][1]:self.reference_points[1][1], self.reference_points[0][0]:self.reference_points[1][0]]
                    roi_grey = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                    histogram = cv2.calcHist([roi_grey], [0], None, [256], [0, 256])
                else:
                    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    histogram = cv2.calcHist([grey_frame], [0], None, [256], [0, 256])
                self.histograms_grey_dict.append(histogram)
        else:
            break
    self.generate_and_store_average_greyscale_histogram()
    self.destroy_video_capture()