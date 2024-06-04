
import re

class PrePro(object):
    # remove all lua comments from a string
    @staticmethod
    def filter(string):
        # add /n before and after a =
        #string = re.sub(r'=', '\n=\n', string)
        string = string.split('\n')
        for i in range(len(string)):
            string[i] = re.sub(r'--.*', '', string[i])
        # remove elementos vazios da lista
        string = list(filter(None, string))
        #print('\n'.join(string))
        return '\n'.join(string)
    pass