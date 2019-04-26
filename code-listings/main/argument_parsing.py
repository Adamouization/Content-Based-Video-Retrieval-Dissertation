import argparse
import app.config as config

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help="The histogram model to use. Choose from the following options: 'rgb', 'hsv' or 'gray'. Leave empty to train using all 3 histogram models.")
    parser.add_argument("--mode", required=True, help="The mode to run the code in. Choose from the following options: 'train', 'test' or 'segment'.")
    parser.add_argument("--showhists", action="store_true", help="Specify whether you want to display each generated histogram.")
    parser.add_argument("-d", "--debug", action="store_true", help="Specify whether you want to print additional logs for debugging purposes.")
    args = parser.parse_args()
    config.debug = args.debug
    config.mode = args.mode
    config.show_histograms = args.showhists
    config.model = args.model
    if config.mode == "train":
        off_line_colour_based_feature_extraction_phase()
    elif config.mode == "test":
        on_line_retrieval_phase()
    elif config.mode == "segment":
        segment_video()
    else:
        print("Wrong mode chosen. Choose from the following options: 'train', 'test' or 'segment'.")
        exit(0)