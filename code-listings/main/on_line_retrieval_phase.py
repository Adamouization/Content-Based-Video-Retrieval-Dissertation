def on_line_retrieval_phase():
    directory = "../recordings/"
    file = "butterfly_recording.mp4"  

    # ask user to stabilise the input query video or not (see code in section below)
    print("\nUsing query: '{}'".format(file))
    print("\nPlease crop the recorded query video for the signature to be generated.")

    start_time = time.time()
    histogram_generator_gray = HistogramGenerator(directory, file)
    histogram_generator_gray.generate_video_greyscale_histogram( is_query=True)
    cur_reference_points = histogram_generator_gray.get_current_reference_points()
    histogram_generator_rgb = HistogramGenerator(directory, file)
    histogram_generator_rgb.generate_video_rgb_histogram( is_query=True, cur_ref_points=cur_reference_points)
    histogram_generator_hsv = HistogramGenerator(directory, file)
    histogram_generator_hsv.generate_video_hsv_histogram( is_query=True, cur_ref_points=cur_reference_points)
    histogram_generator_gray.match_histograms(cur_all_model='gray')
    histogram_generator_rgb.match_histograms(cur_all_model='rgb')
    histogram_generator_hsv.match_histograms(cur_all_model='hsv')

    # Combine matches from all 3 histogram models
    all_results = histogram_generator_hsv.get_results_array()  
    results_count = Counter(all_results)  # count matches
    # convert from count to %
    results_percentage = dict()
    for match in results_count:
        percentage = round((results_count[match] / len(all_results)) * 100.0, 2)
        results_percentage[match] = percentage
    display_results_histogram(results_percentage)
    print("Matches made: {}".format(results_count))
    print("% of matches made: {}".format(results_percentage))

    # find best result
    final_result_name = ""
    final_result_count = 0
    for i, r in enumerate(results_count):
        if i == 0:
            final_result_name = r
            final_result_count = results_count[r]
        else:
            if results_count[r] > final_result_count:
                final_result_name = r
                final_result_count = results_count[r]

    # print results
    runtime = round(time.time() - start_time, 2)
    accuracy = final_result_count / len(all_results)
    get_video_first_frame(directory + file, "../results", is_query=True)
    get_video_first_frame("../footage/{}".format(final_result_name), "../results", is_result=True)
    show_final_match(final_result_name, "../results/query.png", "../results/result.png", runtime, accuracy)
    print_finished_training_message(final_result_name, config.model, runtime, accuracy)