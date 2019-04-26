class HistogramGenerator:
    colours = ('b', 'g', 'r')  # RGB channels
    bins = (8, 12, 3)  # 8 Hue, 12 Saturation, 3 Value
    histcmp_methods = [cv2.HISTCMP_CORREL, cv2.HISTCMP_CHISQR, cv2.HISTCMP_INTERSECT, cv2.HISTCMP_HELLINGER]
    histcmp_3d_methods = ["earths_mover_distance", "energy_distance"]
    histogram_comparison_weigths = {
        'gray': 1,
        'rgb': 5,
        'hsv': 10
    }
    results_array = list()
    
    def __init__(self, directory, file_name):
    def generate_video_rgb_histogram(self, is_query=False, cur_ref_points=None):
    def generate_video_greyscale_histogram(self, is_query=False):
    def generate_video_hsv_histogram(self, is_query=False, cur_ref_points=None):
    def generate_and_store_average_rgb_histogram(self):
    def generate_and_store_average_greyscale_histogram(self):
    def generate_and_store_average_hsv_histogram(self):
    def match_histograms(self, cur_all_model="all"):
    def rgb_histogram_shot_boundary_detection(self, threshold):
    def check_video_capture(self):
    def destroy_video_capture(self):
    def get_video_capture(self):
    def get_current_reference_points(self):
    def get_results_array(self):

def _normalise_histogram(hist):
def _get_frames_to_process(vc):
def _get_chosen_model_string(model):