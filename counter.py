class Counter():

    def __init__(self, bug_limit=None, test_limit=None, crash_limit=1, feedback_interval=100):

        # Counts
        self.num_tests = 0                  # Total number of tests
        self.num_successful = 0             # Number of tests that had no bug
        self.num_error = 0                  # Number of tests that had a bug
        self.num_cant_reproduce = 0         # Number of tests that initially had a bug that was later unreproducable
        self.num_no_mod_styles_bugs = 0     # Number of tests that showed signs of a bug, but during the minify step, all changes were eliminated
        self.num_crash = 0                  # Number of times the program crashed

        # Criteria for when to stop testing
        self.bug_limit = bug_limit          # Stop when the number of bugs found reaches bug_limit
        self.test_limit = test_limit        # Stop when the number of tests run reaches test_limit
        self.crash_limit = crash_limit      # Stop when the program has crashed crash_limit times
        self.crash_exceptions = []          # List of exceptions from crashes

        # Criteria for when to give feedback
        self.feedback_interval = feedback_interval      # Show status update every n successful tests
        self.feedback_triggered = True                  # Show the first status update

    
    def incTests(self):
        self.num_tests += 1
    
    def incSuccess(self):
        self.num_successful += 1

    def incError(self):
        self.num_error += 1
        self.feedback_triggered = True
    
    def incNoRepro(self):
        self.num_cant_reproduce += 1
        self.feedback_triggered = True
    
    def incNoMod(self):
        self.num_no_mod_styles_bugs += 1
        self.feedback_triggered = True
    
    def incCrash(self, exc=None):
        self.num_crash += 1
        self.feedback_triggered = True
        if exc:
            self.crash_exceptions.append(exc)

    def should_continue(self):
        if self.num_crash > self.crash_limit:
            return False
        if self.bug_limit > 0 and self.num_error >= self.bug_limit:
            return False
        if self.test_limit > 0 and self.num_tests >= self.test_limit:
            return False
        return True
    
    def getStatusString(self):
        interval_triggered = self.num_successful % self.feedback_interval == 0
        if self.feedback_triggered or interval_triggered:
            self.feedback_triggered = False
            return f"Passed: {self.num_successful};  Bugs: {self.num_error};  Bugs With No Modified Styles: {self.num_no_mod_styles_bugs};  Can't Reproduce: {self.num_cant_reproduce};  Crashes: {self.num_crash}"
        else:
            return None
            

