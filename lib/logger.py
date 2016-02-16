from datetime import datetime

# Three log levels, ERROR enforced by default
messages = {
    0: "ERROR",
    1: "INFO",
    2: "DEBUG",
}

class logger:
    def __init__(self, level, logfile=None):
        if logfile:
            self.logfile = open(logfile, "wb")
        else:
            self.logfile = None
        if level == "info":
            self.level = 1
            self.str = "INFO"
        elif level == "debug":
            self.level = 2
            self.str = "DEBUG"
        else:
            self.level = 0
    def log(self, level, mssg):
        if level <= self.level:
            entry = "%s: %s, %s" % (messages[level], datetime.now(), mssg)
            if self.logfile:
                self.logfile.write(("%s\n" % entry).encode())
                self.logfile.flush()
            else:
                print(entry)
