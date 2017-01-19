# V1
### Assumptions
#### (1) Lowercase all text to merge words with different cases
#### (2) Account for hyphenated and apostrophed words via regex
#### (3) Hyphenated words that are naturally broken accross lines will be split 
#### (4) Anything with numbers is ignored (whether this is desirable or not may be context dependent)
### Command line input
#### python word_parser_v1.py input_file output_file

# V2
### New stuff
#### (1) detect end of line and merge words split accross lines
##### This use NLTK and a word dictionary to see if the words split across lines are complete words or not. If both are not words then it is likely that they need to be merged. If both are complete words I leave the hyphen assuming the line split was fortuitous and coincided with a real hyphenated word.
### Command line input
#### python word_parser_v2.py input_file output_file

# V3
### New stuff