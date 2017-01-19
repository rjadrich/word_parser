import re
import sys

#extracts the words using a very basic regex
def GetWordsFromFile(filename):
    data = open(filename, 'r')
    text = data.read().lower()
    words = re.findall(r'[a-z]+(?:(?:\-|\')[a-z]+)?', text)
    text = None
    word_dict = {}
    for word in words:
        if word in word_dict:
            word_dict[word] = word_dict[word] + 1
        else:
            word_dict[word] = 1    
    return word_dict

#pass the dict of words and write the file
def WriteWordsToFile(filename, word_dict):
    data = open(filename, 'w')
    for word in word_dict:
        entry = '%s,%i\n' % (word, word_dict[word])
        data.write(entry)
    data.close()
    return None

if __name__ == '__main__':
    try:
        print 'Reading in %s...' % sys.argv[1]
        word_dict = GetWordsFromFile(sys.argv[1])
        print 'Writing to %s...' % sys.argv[2]
        WriteWordsToFile(sys.argv[2], word_dict)
    except:
        print 'Make sure you provided valid in and out filenames'