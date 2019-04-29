def generate_video_hsv_histogram(self, is_query=False, cur_ref_points=None):
    frame_counter = 0  # cur frame ID
    while self.video_capture.isOpened():
        ret, frame = self.video_capture.read()
        if ret:
            if is_query and frame_counter == 0:
                if cur_ref_points is None:
                    cad = ClickAndDrop(frame)
                    self.reference_points = cad.get_reference_points()
                else:
                    self.reference_points = cur_ref_points
            frame_counter += 1
            if frame_counter in _get_frames_to_process(self.video_capture):
                if is_query and len(self.reference_points) == 2:
                    roi = frame[self.reference_points[0][1]:self.reference_points[1][1], self.reference_points[0][0]:self.reference_points[1][0]]
                    roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                    histogram = cv2.calcHist([roi_hsv], [0, 1, 2], None, self.bins, [0, 180, 0, 256, 0, 256])
                else:
                    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    histogram = cv2.calcHist([hsv_frame], [0, 1, 2], None, self.bins, [0, 180, 0, 256, 0, 256])
                self.histograms_hsv_dict.append(histogram)
        else:
            break
    self.generate_and_store_average_hsv_histogram()
    self.destroy_video_capture()