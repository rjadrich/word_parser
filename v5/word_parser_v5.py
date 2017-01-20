import re
import sys
import tries
from nltk.corpus import words

#create a library of common words to detect if hyphen break accross lines needs to be merged
words_lib = set([]) 
[words_lib.add(word.lower()) for word in words.words()]

#this is a nice generator to read in only a manageable sized chunk at a time
#borrowed from http://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python
#this does not account for words that might get chopped!
def ReadChunks(file_object, chunk_size):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

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
def GetWordsFromFile(filename, case_setting, chunk_size):
    #dictionary to store our words
    word_dict = {}
    #read in data
    data = open(filename, 'r')
    #loop over individual chunks provided by the generator
    chunk_num = 1
    for text_chunk in ReadChunks(data, chunk_size):
        print 'Processing chunk %i ...' % chunk_num
        if case_setting == 'lower':
            text = text_chunk.lower()
        elif case_setting == 'none':
            text = text_chunk
        #find words separated by a hyphen and a newline and merge if not complete words
        text = DetectAndFixHyphenBreaks(text)
        #extract words
        words = re.findall(r'[a-zA-Z]+(?:(?:\-|\')[a-zA-Z]+)?', text)
        text = None
        for word in words:
            if word in word_dict:
                word_dict[word] = word_dict[word] + 1
            else:
                word_dict[word] = 1   
        chunk_num = chunk_num + 1
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
    if len(sys.argv) == 6: 
        #case setting
        print 'Case setting %s...' % sys.argv[1]
        if sys.argv[1] != 'lower' and sys.argv[1] != 'none':
            print 'Bad case setting!'
            sys.exit()
        else:
            None    
        #chunk size for large files
        print 'Chunk size %i...' % int(sys.argv[2])
        if int(sys.argv[2]) < 5:
            print 'Did not meet minimum chunk size of 5!'
            sys.exit()
        else:
            None    
        #extract words
        print 'Reading in %s...' % sys.argv[3]
        word_dict = GetWordsFromFile(sys.argv[3], sys.argv[1], int(sys.argv[2]))
        #prefix search
        print 'Finding words with prefix %s...' % sys.argv[5]
        word_tries = tries.ConvertWordDictToTries(word_dict)
        prefix_word_dict = tries.MatchPrefixInTries(sys.argv[5], word_tries)
        #write words
        print 'Writing to %s...' % sys.argv[4]
        WriteWordsToFile(sys.argv[4], prefix_word_dict)
    else:
        print 'Make sure you provided case setting as well as valid in and out filenames'
