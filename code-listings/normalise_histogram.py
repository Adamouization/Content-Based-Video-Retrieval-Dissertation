def _normalize_histogram(hist):
    """
    Normalise a histogram using OpenCV's "normalise: function
    :param hist: the histogram to normalise
    :return: the normalised histogram
    """
    hist = cv2.normalize(hist, hist)
    return hist