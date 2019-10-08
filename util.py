class GracefulShutdown(object):
    def __init__(self):
        self.is_shutdown = False

    def exit(self, signum, frame):
        self.is_shutdown = True

    def is_exit(self):
        return self.is_shutdown
