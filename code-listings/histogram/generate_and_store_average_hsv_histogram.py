def generate_and_store_average_hsv_histogram(self):
    avg_histogram = np.zeros(shape=(8, 12, 3))
    hist = self.histograms_hsv_dict
    for h in range(0, self.bins[0]):  # loop through hue bins
        for s in range(0, self.bins[1]):  # loop through saturation bins
            for v in range(0, self.bins[2]):  # loop through value bins
                bin_sum = 0
                # get value for each colour histogram in bin [h][s][v]
                for arr_index in range(0, len(hist)):
                    bin_value = hist[arr_index][h][s][v]
                    bin_sum += bin_value
                # average all bins values to store in new histogram
                new_bin_value = bin_sum / len(hist)
                avg_histogram[h][s][v] = new_bin_value
    # normalise averaged histogram
    avg_histogram = _normalise_histogram(avg_histogram)
    # write to file
    if not os.path.exists("../histogram_data/{}/".format(self.file_name)):
        os.makedirs("../histogram_data/{}/".format(self.file_name))
    with open("../histogram_data/{}/hist-{}.txt".format(self.file_name, "hsv"), 'w') as file:
        file.write("# HSV Histogram shape: {0} [normalised]\n".format(avg_histogram.shape))
        for arr_2d in avg_histogram:
            file.write("# New slice\n")
            np.savetxt(file, arr_2d)