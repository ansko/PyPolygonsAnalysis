class OptionsParser:
    """
    Reader of a file with options.
    By default its name is 'options.ini'.
    Format is .ini (key=value,
                    #comment)
    """
    def __init__(self, options_fname='options.ini'):
        self.options = dict()
        with open(options_fname, 'r') as f:
            for line in f:
                self.__process_line(line)

    def __process_line(self, line):
        if line.startswith('#') or line.startswith('\n'):
            return
        line = line[:-1] # to remove terminating '\n'
        ls = line.split('=')
        if len(ls) < 2:
            return
        key = ls[0]
        try:
            value = int(ls[1])
        except:
            try:
                value = float(ls[1])
            except:
                value = str(ls[1])
        self.options[key] = value
