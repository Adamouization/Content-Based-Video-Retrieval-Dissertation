from pyspin.spin import make_spin, Spin2
from app.histogram import HistogramGenerator

@make_spin(Spin2, "Generating histograms for database videos...".format(config.model))
def off_line_colour_based_feature_extraction_phase():
    files = get_video_filenames("../footage/")
    start_time = time.time() # start measuring runtime
    for file in files:
        histogram_generator_gray = HistogramGenerator(directory, file)
        histogram_generator_gray.generate_video_greyscale_histogram()
        histogram_generator_rgb = HistogramGenerator(directory, file)
        histogram_generator_rgb.generate_video_rgb_histogram()
        histogram_generator_hsv = HistogramGenerator(directory, file)
        histogram_generator_hsv.generate_video_hsv_histogram()
    runtime = round(time.time() - start_time, 2)
    print_finished_training_message(config.model, directory, runtime)