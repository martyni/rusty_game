import datetime


class Logerer(object):

    def __init__(self):
        self.format = '%H:%M:%S %d/%m/%y '

    def log(self, name, message):
        message = " : " + str(message)
        full_message = datetime.datetime.now().strftime(self.format) + name + message
        print full_message
        return full_message


def main():
    l = Logerer()
    l.log("dave", "dave is fine")

if __name__ == "__main__":
    main()
