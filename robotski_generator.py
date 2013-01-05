
import argparse
import cPickle

"""Handles the processing and creation of a pickle
    containing the robotski messages
"""


def pickle_it(object):
    try:
        with open(r'robotski.pkl', 'w') as robotski_pickle:
            cPickle.dump(object, robotski_pickle)
    except IOError:
        pass


def read_it(file_path):
    result = []
    try:
        with open(file_path, 'r') as read_file:
            for line in read_file:
                result.append(line.rstrip())
    except IOError:
        print 'Couldnt find the file you specified'
    return result


def map_it(list):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a robotski phrase list.')
    parser.add_argument('--filename', action='store', default='robotski.txt', type=str,
                        help='Select a txt file to generate phrases from. Defaults to robotski.txt')
    arguments = parser.parse_args()
    file_name = arguments.filename
    phrase_list = read_it(file_name)
    pickle_it(phrase_list)
