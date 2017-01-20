from copy import deepcopy

#convert the dictionary of words with counts into a tries data structure for rapid prefix searching
def ConvertWordDictToTries(word_dict):
    tries = {}
    for word in word_dict:
        count = word_dict[word]
        tries = AddWordToTries(word, tries, count)
    return tries

#adds a single word to the tries parse tree using a recursive scheme
def AddWordToTries(word, word_tries, count):
    letter = word[0]
    if letter in word_tries:
        sub_tries = word_tries[letter][1]
        if len(word) == 1:
            word_tries[letter][0] = count
        if len(word) > 1:
            word_tries[letter][1] = AddWordToTries(word[1:], sub_tries, count)
        return word_tries
    else:
        if len(word) == 1:
            word_tries[letter] = [count, {}]
        else:
            word_tries[letter] = [0, {}]
        sub_tries = word_tries[letter][1]
        if len(word) > 1:
            word_tries[letter][1] = AddWordToTries(word[1:], sub_tries, count)
        return word_tries

#recursively crawl the tries tree building back up a simple count dictionary
def ExtractRemainders(prefix, tries, word_dict, prev_letters):
    for letter in tries:
        sub_tries = deepcopy(tries[letter][1])
        if tries[letter][0] > 0:
            key = prefix + prev_letters + letter
            word_dict[key] = tries[letter][0]
        new_letters = prev_letters + letter    
        word_dict = ExtractRemainders(prefix, sub_tries, deepcopy(word_dict), new_letters)
    return word_dict

#extract words and counts
def MatchPrefixInTries(prefix, tries):
    #first extract the relevant subtree based on prefix
    prefix_letters = [letter for letter in prefix]
    #only use the portion of the tries tree that is needed
    sub_tries = tries
    while prefix_letters:
        letter = prefix_letters.pop(0)
        if letter in sub_tries:
            sub_tries = sub_tries[letter][1]
        else:
            return {}
    #function to parse tries tree and return valid remainders
    word_dict = {}
    word_dict = ExtractRemainders(prefix, sub_tries, {}, '')
    return word_dict