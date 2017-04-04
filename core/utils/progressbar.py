import sys

# TODO: Refactor!
class ProgressBar:

    counter   = 0
    increment = 1
    step      = 1
    width     = 10

    def setup(self, number):
        self.increment = 1 if number >= self.width else self.width / number
        self.step      = number / self.width if number >= self.width else self.width / number
        # self.width     = self.step * number

    # TODO: Change name, e.g., print skeleton.
    def skeleton(self):
        print '[          ]',
        print '\b' * (self.width + 2),
        sys.stdout.flush()

    def progress(self):
        self.counter += self.increment
        if self.counter % self.step == 0:
            for _ in range(self.increment):
                print '\b.',
                sys.stdout.flush()

    # TODO: Needs to be smarter!
    def done(self):
        print '\b] DONE!'

    def error(self):
        for _ in range(self.width - self.counter):
            print '\b.',
            sys.stdout.flush()
            self.counter += 1
        print '\b] ERROR!'