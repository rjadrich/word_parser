import re
import sys
from nltk.corpus import words

#create a library of common words to detect if hyphen break accross lines needs to be merged
words_lib = set([]) 
[words_lib.add(word.lower()) for word in words.words()]

#finds hypenated words split accross a line and merges the words if one or both are not complete words
def DetectAndFixHyphenBreaks(text):
    global words_lib
    matches = re.findall(r'[a-z]+\s*\-\s*\n+\s*[a-z]+', text)
    for match in matches:
        word_1, word_2 = re.findall(r'[a-z]+', match)
        if (word_1 not in words_lib) or (word_2 not in words_lib):
            text = re.sub(match, word_1 + word_2, text)
    return text

#extracts the words using a very basic regex
def GetWordsFromFile(filename):
    #read in data
    data = open(filename, 'r')
    text = data.read().lower()
    #find words separated by a hyphen and a newline and merge if not complete words
    text = DetectAndFixHyphenBreaks(text)
    #extract words
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