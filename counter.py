class Counter():
    feedback_interval = 50 # Show status update every n successful tests
    feedback_triggered = True # Show the first status update

    def __init__(self):
        self.num_tests = 0
        self.num_successful = 0
        self.num_error = 0
        self.num_cant_reproduce = 0
        self.num_no_mod_styles_bugs = 0
    
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
    
    def getStatusString(self):
        interval_triggered = self.num_successful % self.feedback_interval == 0
        if self.feedback_triggered or interval_triggered:
            self.feedback_triggered = False
            return f"Success: {self.num_successful};  Failed: {self.num_error};  Bugs With No Modified Styles: {self.num_no_mod_styles_bugs};  Can't Reproduce: {self.num_cant_reproduce}"
        else:
            return None
            

