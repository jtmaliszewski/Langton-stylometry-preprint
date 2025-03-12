'''
Unfortunately, this repo does not include the raw data due to copyright limitations. 
The below code was used for its preprocessing; I disclose it mostly to document the normalization steps.

If you would like to consult the raw data, please email me at j.maliszewski@uw.edu.pl

'''

import string, re, os
from collections import Counter 


def preprocess(raw_txt):
	'''Reads in a string, strips all punctuation and case.
	I remove also the numerals, since they will otherwise end up on MFW list and are used inconsistently in the data. 
	Most of these constitute editorial additions, uneven accros the corpus, 
	so it is a reasonable normalization to ommit them.
	I normalize ae >> e (relevant in 'quae' and 'haec' occurences), sed >> set, and u/v.'''

	non_letters = re.compile(r"[^A-Za-z\s]")
	raw_txt = re.sub(non_letters, " ",raw_txt) # remove all special characters; add spaces, so as not to accidentaly meld words.
	raw_txt = re.sub(" +", " ", raw_txt).lower() # remove any resulting double spaces, normalize case.
	
	# normalize ortography
	raw_txt = re.sub("quae", "que", raw_txt)
	raw_txt = re.sub("haec", "hec", raw_txt)
	raw_txt = re.sub("\bsed\b", "set", raw_txt)
	raw_txt = re.sub("v", "u", raw_txt)

	out_txt = raw_txt
	
	return(out_txt)


def save_processed_data(directory_in, directory_out):
	# Process and save raw data. After the process, all characters in the files match [a-z\n ].

	for filename in os.listdir(directory_in):
			with open(directory_in+"/"+filename, 'r') as file_in:
				processed_text = preprocess(file_in.read())

			with open(f"{directory_out}/{os.path.splitext(filename)[0]}_processed.txt", 'w') as file_out:
				file_out.write(processed_text)


# declare directories
raw_data = "../data_full_summae/corpus_full_summae/"
processed_data = "../data_full_summae/corpus_processed/"

# call preprocessing function
save_processed_data(raw_data, processed_data)