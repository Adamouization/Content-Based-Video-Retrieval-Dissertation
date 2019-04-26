def _get_frames_to_process(vc):
    frame_ids = list()
    total_frames = vc.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = vc.get(cv2.CAP_PROP_FPS)
    for i in range(1, int(total_frames) + 1, math.ceil(fps)):
        frame_ids.append(i)
    return frame_ids