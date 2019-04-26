def database_preprocessing_phase():
    shot_boundary_detector = HistogramGenerator("../recordings/", "scene-segmentation.mp4")
    video_capture = shot_boundary_detector.get_video_capture()
    frame_count = get_number_of_frames(vc=video_capture)
    fps = get_video_fps(vc=video_capture)
    print("Total Frames: {}".format(frame_count))
    print("FPS: {}\n".format(fps))

    # start processing video for shout boundary detection
    print("Starting to process video for shot boundary detection...")
    start_time = time.time()
    shot_boundary_detector.rgb_histogram_shot_boundary_detection( threshold=7)

    # print final results
    runtime = round(time.time() - start_time, 2)
    print("--- Number of frames in video: {} ---".format(frame_count))
    print("--- Runtime: {} seconds ---".format(runtime))