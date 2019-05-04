def match_histograms(self, cur_all_model="all"):
    # variables used for finding the match to the recorded video
    video_match = ""
    video_match_value = 0
    # get histogram for the recorded video to match
    hsv_data = np.loadtxt("../histogram_data/{}/hist-hsv.txt".format( self.file_name))
    query_histogram = {
        'hsv': hsv_data.reshape((8, 12, 3))
    }

    print("\n{} Histogram Comparison Results:\n".format(_get_chosen_model_string(cur_all_model)))
    method = ""
    csv_field_names = ["video", "score"]
    if config.model == "hsv":
        for m in self.histcmp_3d_methods:
            if m == "earths_mover_distance":
                method = "EARTH'S MOVER DISTANCE"
            elif m == "energy_distance":
                method = "ENERGY DISTANCE"
            # CSV file to write data to for each method
            csv_file = open("../results/csv/{}-{}-{}.csv".format(config.model, cur_all_model, method), 'w')
            with csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=csv_field_names)
                writer.writeheader()
                table_data = list()
                for i, file in enumerate(get_video_filenames("../footage/")):
                    dbvideo_hsv_histogram_data = np.loadtxt("../histogram_data/{}/hist-hsv.txt".format(file))
                    dbvideo_hsv_histogram = dbvideo_hsv_histogram_data.reshape((8, 12, 3))
                    comparison = 0
                    for h in range(0, self.bins[0]):  # loop through hue bins
                        for s in range(0, self.bins[1]):  # loop through saturation bins
                            query_histogram_slice = query_histogram['hsv'][h][s]
                            dbvideo_histogram_slice = dbvideo_hsv_histogram[h][s]
                            if method == "EARTH'S MOVER DISTANCE":
                                comparison += wasserstein_distance(query_histogram_slice, dbvideo_histogram_slice)
                            elif method == "ENERGY DISTANCE":
                                comparison += energy_distance(query_histogram_slice, dbvideo_histogram_slice)

                    # append data to table
                    table_data.append([file, round(comparison, 5)])
                    # write data to CSV file
                    writer.writerow({"video": file, "score": round(comparison, 5)})

                    if i == 0:
                        video_match = file
                        video_match_value = comparison
                    else:
                        if comparison < video_match_value:
                            video_match = file
                            video_match_value = comparison

            # append video match found to results list (using weights)
            for _ in range(0, self.histogram_comparison_weigths['hsv']):
                self.results_array.append(video_match)

            print_terminal_table(table_data, method)
            print("{} {} Match found: ".format(_get_chosen_model_string(cur_all_model), method) + "\x1b[1;31m" + video_match + "\x1b[0m" + "\n\n")