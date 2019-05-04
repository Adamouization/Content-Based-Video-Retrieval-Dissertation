def match_histograms(self, cur_all_model="all"):
    # variables used for finding the match to the recorded video
    video_match = ""
    video_match_value = 0
    # get histogram for the recorded video to match
    if config.model == "gray":
        query_histogram = {
            'gray': np.loadtxt(
                "../histogram_data/{}/hist-gray.txt".format(self.file_name), dtype=np.float32, unpack=False)
        }
    elif config.model == "rgb":
        query_histogram = {
            'b': np.loadtxt("../histogram_data/{}/hist-b.txt".format( self.file_name), dtype=np.float32, unpack=False),
            'g': np.loadtxt("../histogram_data/{}/hist-g.txt".format( self.file_name), dtype=np.float32, unpack=False),
            'r': np.loadtxt("../histogram_data/{}/hist-r.txt".format( self.file_name), dtype=np.float32, unpack=False)
        }

    print("\n{} Histogram Comparison Results:\n".format(_get_chosen_model_string(cur_all_model)))
    method = ""
    csv_field_names = ["video", "score"]
    if config.model == "rgb" or config.model == "gray":
        for m in self.histcmp_methods:
            if m == 0:
                method = "CORRELATION"
            elif m == 1:
                method = "CHI-SQUARE"
            elif m == 2:
                method = "INTERSECTION"
            elif m == 3:
                method = "HELLINGER"
            # CSV file to write data to for each method
            csv_file = open("../results/csv/{}-{}-{}.csv".format(config.model, cur_all_model, method), 'w')
            with csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=csv_field_names)
                writer.writeheader()
                table_data = list()
                for i, file in enumerate(get_video_filenames("../footage/")):
                    comparison = 0
                    if config.model == "gray":
                        dbvideo_greyscale_histogram = np.loadtxt("../histogram_data/{}/hist-gray.txt".format(file), dtype=np.float32, unpack=False)
                        comparison = cv2.compareHist(query_histogram['gray'], dbvideo_greyscale_histogram, m)
                    elif config.model == "rgb":
                        dbvideo_b_histogram = np.loadtxt("../histogram_data/{}/hist-b.txt".format(file), dtype=np.float32, unpack=False)
                        dbvideo_g_histogram = np.loadtxt("../histogram_data/{}/hist-g.txt".format(file), dtype=np.float32, unpack=False)
                        dbvideo_r_histogram = np.loadtxt("../histogram_data/{}/hist-r.txt".format(file), dtype=np.float32, unpack=False)
                        comparison_b = cv2.compareHist(query_histogram['b'], dbvideo_b_histogram, m)
                        comparison_g = cv2.compareHist(query_histogram['g'], dbvideo_g_histogram, m)
                        comparison_r = cv2.compareHist(query_histogram['r'], dbvideo_r_histogram, m)
                        comparison = (comparison_b + comparison_g + comparison_r) / 3

                    # append data to table
                    table_data.append([file, round(comparison, 5)])
                    # write data to CSV file
                    writer.writerow({"video": file, "score": round(comparison, 5)})

                    if i == 0:
                        video_match = file
                        video_match_value = comparison
                    else:
                        # Higher score = better match (Correlation and Intersection)
                        if m in [0, 2] and comparison > video_match_value:
                            video_match = file
                            video_match_value = comparison
                        # Lower score = better match
                        # (Chi-square, Alternative chi-square, Hellinger and KL Divergence)
                        elif m in [1, 3, 4, 5] and comparison < video_match_value:
                            video_match = file
                            video_match_value = comparison

            # append video match found to results list (using weights)
            if cur_all_model == "gray":
                for _ in range(0, self.histogram_comparison_weigths['gray'], 1):
                    self.results_array.append(video_match)
            elif cur_all_model == "rgb":
                for _ in range(0, self.histogram_comparison_weigths['rgb'], 1):
                    self.results_array.append(video_match)

            print_terminal_table(table_data, method)
            print("{} {} match found: ".format(_get_chosen_model_string(cur_all_model), method) + "\x1b[1;31m" + video_match + "\x1b[0m" + "\n\n")