# V1
## Assumptions
### (1) Lowercase all text to merge words with different cases
### (2) Account for hyphenated and apostrophed words via regex
### (3) Hyphenated words that are naturally broken accross lines will be split 
### (4) Anything with numbers is ignored (whether this is desirable or not may be context dependent)
## Command line input
### python word_parser.py input_file output_file

# V2
## Assumptions
### (1) detect end of line and merge words split accross lines