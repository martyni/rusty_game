import datetime


class Logerer(object):

    def __init__(self):
        self.format = '%H:%M:%S %d/%m/%y '
        self.last_logs = [None, None]
        self.current_log_count = 0
        self.verbosity = 100

    def log(self, name, message):
        message = " : " + str(message)
        full_message = datetime.datetime.now().strftime(self.format) + name + message
        if name + message in self.last_logs: 
           self.current_log_count += 1
        else: 
           self.current_log_count = 0
           print full_message
        self.last_logs.append(name + message)
        self.last_logs = self.last_logs[-5::]
        return full_message


def main():
    l = Logerer()
    l.log("dave", "dave is fine")

if __name__ == "__main__":
    main()
