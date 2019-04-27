def rgb_histogram_shot_boundary_detection(self, threshold):
    x_axis = list()
    y_axis = list()
    is_under_threshold = True
    ret, frame = self.video_capture.read()  # get initial frame
    frame_counter = 0  # cur frame ID
    shot_changes_detected = 0  # No. shot boundaries detected
    while self.video_capture.isOpened():
        prev_frame = frame[:]  # previous frame
        ret, frame = self.video_capture.read()  # read video
        if ret:
            frame_counter += 1
            cur_rgb_hist = {
                'b': list(),
                'g': list(),
                'r': list()
            }
            prev_rgb_hist = {
                'b': list(),
                'g': list(),
                'r': list()
            }
            for i, col in enumerate(self.colours):
                # calculate RGB histograms
                cur_frame_hist = cv2.calcHist([frame], [i], None, [256], [0, 256])
                prev_frame_hist = cv2.calcHist([prev_frame], [i], None, [256], [0, 256])
                # normalise histograms
                cur_frame_hist = _normalise_histogram(cur_frame_hist)
                prev_frame_hist = _normalise_histogram(prev_frame_hist)
                # save histograms in dict
                cur_rgb_hist[col].append(cur_frame_hist)
                prev_rgb_hist[col].append(prev_frame_hist)

            # calculate Intersection between consecutive frames
            comparison_r = cv2.compareHist(prev_rgb_hist['r'][0], cur_rgb_hist['r'][0], cv2.HISTCMP_INTERSECT)
            comparison_g = cv2.compareHist(prev_rgb_hist['g'][0], cur_rgb_hist['g'][0], cv2.HISTCMP_INTERSECT)
            comparison_b = cv2.compareHist(prev_rgb_hist['b'][0], cur_rgb_hist['b'][0], cv2.HISTCMP_INTERSECT)
            comparison = (comparison_b + comparison_g + comparison_r) / 3
            # For KL Divergence, use cv2.HISTCMP_KL_DIV

            # append data to lists for plot
            x_axis.append(frame_counter)
            y_axis.append(comparison)
            
            # check if difference big enough for shot boundary
            if comparison < threshold and is_under_threshold:
                shot_changes_detected += 1
                is_under_threshold = False
                print("Scene Change detected at Frame {}".format(frame_counter))
            elif comparison > threshold:
                is_under_threshold = True
        else:
            break

    # Plot results
    plt.plot(x_axis, y_axis)
    plt.plot(x_axis, np.full(frame_counter, threshold))
    plt.title("Intersection Between Consecutive Frame RGB Histogram")
    plt.xlabel("Frame")
    plt.ylabel("Intersection")
    plt.show()
    print("\n--- Number of shot changes detected: {} ---".format(shot_changes_detected))