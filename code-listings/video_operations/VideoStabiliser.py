from pyspin.spin import make_spin, Box1
from vidstab import VidStab

class VideoStabiliser:
    def __init__(self, directory, file_name):
        """Initialise variables and start stabilising"""
        self.directory = directory
        self.file = file_name
        self.new_file = file_name[:-4]
        self.stabiliser = VidStab()
        self.stabilise_video()

    @make_spin(Box1, "Stabilising video...")
    def stabilise_video(self):
        self.stabiliser.stabilize(input_path="{}{}".format( self.directory, self.file), output_path="{}/stable-{}.avi".format(self.directory, self.new_file), border_type="reflect")
        print("\nVideo stabilised!")