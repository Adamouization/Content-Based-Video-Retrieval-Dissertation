def get_video_filenames(directory):
    """Returns a list containing all the mp4 files in a directory"""
    list_of_videos = list()
    for filename in os.listdir(directory):
        if filename == ".DS_Store":
            pass  # ignoring .DS_Store file (for macOS)
        elif filename.endswith(".mp4"):
            list_of_videos.append(filename)
        else:
            print("no mp4 files found in directory '{}'".format(directory))
    return list_of_videos

def print_terminal_table(table_data, method_used):
    """Prints a table with the results in the terminal."""
    table = DoubleTable(table_data)
    table.title = method_used
    table.inner_heading_row_border = False
    table.inner_row_border = True
    print(table.table)

def print_finished_training_message(answer, model, runtime, accuracy=None):
    """Prints a message at the end of the training function."""
    print("\n\nGenerated " + "\x1b[1;31m" + "{}".format(model) + "\x1b[0m" + " histograms for all videos")
    if accuracy is not None:
        print("\n\n" + "\x1b[1;31m" + "MATCH FOUND: {}".format(answer) + "\x1b[0m")
    print("\n--- Runtime: {} seconds ---".format(runtime))
    if accuracy is not None:
        print("--- Accuracy: {} % ---".format(round(accuracy * 100, 2)))

def get_video_first_frame(video, path_output_dir, is_query=False, is_result=False):
    """Retrieves the first frame from a video and saves it as a PNG."""
    vc = cv2.VideoCapture(video)
    frame_counter = 0
    while vc.isOpened():
        ret, image = vc.read()
        if ret and frame_counter == 0:
            if is_query:
                cv2.imwrite(os.path.join(path_output_dir, "query.png"), image)
            elif is_result:
                cv2.imwrite(os.path.join(path_output_dir, "result.png"), image)
            frame_counter += 1
        else:
            break
    cv2.destroyAllWindows()
    vc.release()

def show_final_match(result_name, query_frame, result_frame, runtime, accuracy):
    """Plots the query image and the matched video."""
    query_img = mpimg.imread(query_frame)
    result_img = mpimg.imread(result_frame)
    plt.subplot(2, 1, 1)
    plt.imshow(query_img)
    plt.title("Original Query Video", fontSize=16), plt.xticks([]), plt.yticks([])
    plt.subplot(2, 1, 2)
    plt.imshow(result_img)
    plt.title(
        "Match '{}' found in {}s with {}% accuracy".format(result_name, runtime, round(accuracy * 100, 2)),
        fontSize=13)
    plt.xticks([])
    plt.yticks([])
    plt.show()

def display_results_histogram(results_dict):
    """Displays the results in the form of a histogram."""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(list(results_dict.keys()), results_dict.values())
    plt.title("Probability of a match for most likely videos")
    plt.ylabel("%")
    plt.tight_layout()
    plt.setp(ax.get_xticklabels(), fontsize=10, rotation='vertical')
    plt.show()

def get_number_of_frames(vc):
    """Retrieves the total number of frames in a video using OpenCV's VideoCapture object cv2.CAP_PROP_FRAME_COUNT attribute."""
    return int(vc.get(cv2.CAP_PROP_FRAME_COUNT))

def get_video_fps(vc):
    """Retrieves the frame rate (Frames Per Second) of a video using OpenCV's VideoCapture object cv2.CAP_PROP_FPS"""
    return round(vc.get(cv2.CAP_PROP_FPS), 2)

def terminal_yes_no_question(question, default="no"):
    """Ask a yes/no question via input() and return the answer as a boolean."""
    valid = {"yes": True, "y": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")

def video_file_already_stabilised(filepath):
    """Checks if the path to a stable version of the video already exists."""
    if os.path.isfile(filepath):
        return True
    return False