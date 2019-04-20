from pyspin.spin import make_spin, Box1
from vidstab import VidStab


class VideoStabilizer:
def __init__(self, directory, file_name):
    """
    Initialise variables and call the function to stabilise the  video.
    """
    self.directory = directory
    self.file = file_name

    self.stabilizer = VidStab()
    self.stabilize_video()

@make_spin(Box1, "Stabilizing video...")
def stabilize_video(self):
    self.stabilizer.stabilize(input_path="{}/{}.mp4".format(self.directory, self.file), output_path="{}/stable-{}.avi".format(self.directory, self.file), border_type="reflect")
    print("\nVideo stabilized!")