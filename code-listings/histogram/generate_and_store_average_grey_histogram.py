def generate_and_store_average_greyscale_histogram(self):
    avg_histogram = np.zeros(shape=(255, 1))
    hist = self.histograms_grey_dict
    for i in range(0, 255):  # loop through all bins
        bin_sum = 0
        # get value for each colour histogram in bin i
        for arr_index in range(0, len(hist)):
            bin_value = hist[arr_index].item(i)
            bin_sum += bin_value
        # average all bins values to store in new histogram
        new_bin_value = bin_sum / len(hist)
        avg_histogram[i] = new_bin_value
    # normalise
    avg_histogram = _normalise_histogram(avg_histogram)
    # write to file
    if not os.path.exists("../histogram_data/{}/".format(self.file_name)):
        os.makedirs("../histogram_data/{}/".format(self.file_name))
    with open("../histogram_data/{}/hist-{}.txt".format(self.file_name, "gray"), 'w') as file:
        file.write("# Greyscale Histogram ({} bins) [normalised]\n".format(avg_histogram.shape[0]))
        np.savetxt(file, avg_histogram, fmt='%f')