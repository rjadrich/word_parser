# Below I provide details for each version
### Each has its own folder and some example output files with appropriate names to differentiate
### To run the code just use the format I discuss for each version under 'Command line input'
### V2 and above will require NLTK (Natural Language Toolkit)

### Example input for V4 
#### python word_parser_v2.py lower 1000 alice30.txt word_count.txt

# V1
### Assumptions
#### (1) Lowercase all text to merge words with different cases
#### (2) Account for hyphenated and apostrophed words via regex
#### (3) Hyphenated words that are naturally broken accross lines will be split 
#### (4) Anything with numbers is ignored (whether this is desirable or not may be context dependent)
### Command line input
#### python word_parser_v1.py 'input_file' 'output_file'

# V2
### New stuff
#### (1) Detect end of line and merge words split accross lines
##### This uses an NLTK word dictionary to see if the words split across lines are complete words or not. If both are not words then it is likely that they need to be merged. If both are complete words I leave the hyphen assuming the line split was fortuitous and coincided with a real hyphenated word. This is not always true but oftentimes this will work (or so I think).
### Command line input
#### python word_parser_v1.py 'input_file' 'output_file'

# V3
### New stuff
#### (1) Added option to command line input to keep case or lower everything
### Command line input
#### python word_parser_v2.py 'case_option' 'input_file' 'output_file'
#### case_option = {none, lower}

# V4
### New stuff
#### (1) Added the ability to chunk the file into reasonable sized portions for processing
##### This uses a generator to only keep that portion in memory for processing; however, it comes at the cost of possibly getting garbage words due to splitting the file.
##### The larger the chunks the less of an issue this will be of course. Such issues are also present when using technologies like MapReduce. 
##### I have not programmed the thing to balance the chunks so the final one may be very short.
##### Input chunk size is in bytes 
### Command line input
#### python word_parser_v2.py 'case_option' 'chunk_size' 'input_file' 'output_file'
#### case_option = {none, lower}
#### chunk_size = {5 or greater}

# Things that should be done
#### (1) Add the ability to hande text encodings like UTF-8. Right now it assume ASCII
#### (2) Could parallelize the chunking step 
#### (3) Add options for including numbers and alpha-numeric quantities
#### (4) Enable the user to provide a pre-specified dictionary of valid words