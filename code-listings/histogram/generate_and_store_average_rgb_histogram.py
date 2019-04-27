def generate_and_store_average_rgb_histogram(self):
    avg_histogram = np.zeros(shape=(255, 1))
    for col, hists in self.histograms_rgb_dict.items():
        for i in range(0, 255):  # loop through all bins
            bin_sum = 0
            # get value for each colour histogram in bin i
            for arr_index in range(0, len(hists)):
                bin_value = hists[arr_index].item(i)
                bin_sum += bin_value
            # average all bins values to store in new histogram
            new_bin_value = bin_sum / len(hists)
            avg_histogram[i] = new_bin_value
        # normalise averaged histogram
        avg_histogram = _normalise_histogram(avg_histogram)
        # write to file
        if not os.path.exists("../histogram_data/{}/".format(self.file_name)):
            os.makedirs("../histogram_data/{}/".format(self.file_name))
        with open("../histogram_data/{}/hist-{}".format(self.file_name, col), 'w') as file:
            file.write("# '{}' channel of RGB histogram ({} bins) [normalised]\n".format(
                col.upper(),
                avg_histogram.shape[0]
            ))
            np.savetxt(file, avg_histogram, fmt='%f')