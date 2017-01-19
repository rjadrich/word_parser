import re
import sys
from nltk.corpus import words

#create a library of common words to detect if hyphen break accross lines needs to be merged
words_lib = set([]) 
[words_lib.add(word.lower()) for word in words.words()]

#finds hypenated words split accross a line and merges the words if one or both are not complete words
def DetectAndFixHyphenBreaks(text):
    global words_lib
    matches = re.findall(r'[a-zA-Z]+\s*\-\s*\n+\s*[a-zA-Z]+', text)
    for match in matches:
        word_1, word_2 = re.findall(r'[a-zA-Z]+', match)
        if (word_1.lower() not in words_lib) or (word_2.lower() not in words_lib):
            text = re.sub(match, word_1 + word_2, text)
    return text

#extracts the words using a very basic regex
def GetWordsFromFile(filename, case_setting, word_check_setting):
    global words_lib
    #read in data
    data = open(filename, 'r')
    if case_setting == 'lower':
        text = data.read().lower()
    elif case_setting == 'none':
        text = data.read()
    #find words separated by a hyphen and a newline and merge if not complete words
    text = DetectAndFixHyphenBreaks(text)
    #extract words
    words = re.findall(r'[a-zA-Z]+(?:(?:\-|\')[a-zA-Z]+)?', text)
    text = None
    word_dict = {}
    #adds words to dictionary and will keep or remove non-library words according to NLTK
    if word_check_setting == 'word_check':
        for word in words:
            if word in word_dict:
                word_dict[word] = word_dict[word] + 1
            else:
                if word.lower() in words_lib:
                    word_dict[word] = 1  
    elif word_check_setting == 'no_word_check':
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
    #there are four settings to read in so make sure we get that + 1 for program name as 0'th entry
    if len(sys.argv) == 5: 
        #case setting
        print 'Case setting: %s ...' % sys.argv[1]
        if sys.argv[1] != 'lower' and sys.argv[1] != 'none':
            print 'Bad case setting!'
            sys.exit()        
        #word check setting
        print 'Word check setting: %s ...' % sys.argv[2]
        if sys.argv[2] != 'word_check' and sys.argv[2] != 'no_word_check':
            print 'Bad word check setting!'
            sys.exit()   
        #extract words
        print 'Reading in %s ...' % sys.argv[3]
        word_dict = GetWordsFromFile(sys.argv[3], sys.argv[1], sys.argv[2])
        #write words
        print 'Writing to %s ...' % sys.argv[4]
        WriteWordsToFile(sys.argv[4], word_dict)
    else:
        print 'Make sure you provided all settings!'
