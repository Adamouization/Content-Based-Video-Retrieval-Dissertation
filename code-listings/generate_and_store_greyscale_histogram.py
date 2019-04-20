def generate_and_store_average_greyscale_histogram(self):
    # array to store average histogram values
    avg_histogram = np.zeros(shape=(255, 1))
    for i in range(0, 255):  # loop through all bins
        bin_sum = 0
        # get value for each colour histogram in bin i
        for arr_index in range(0, len(self.histograms_grey_dict)):
            bin_value = self.histograms_grey_dict[arr_index].item(i)
            bin_sum += bin_value
        # average all bins values to store in new histogram
        new_bin_value = bin_sum / len(self.histograms_grey_dict)
        avg_histogram[i] = new_bin_value
    np.savetxt("../histogram_data/{}/hist-{}".format(self.file_name, "gray"), avg_histogram, fmt='%f')