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

    def prefix(self):
        print '[          ]',
        print '\b' * (self.width + 2),
        sys.stdout.flush()

    def progress(self):
        self.counter += self.increment
        if self.counter % self.step == 0:
            for _ in range(self.increment):
                print '\b.',
                sys.stdout.flush()

    def suffix(self):
        print '\b] DONE!'