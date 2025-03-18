'''
Code used to mask the processed corpus.

'''


import string, re, os
from collections import Counter 


def get_mfw(directory, integer):
	# merges all txt's in a directory and returns top words, length indicated by integer, 

	# collect preprocessed txt's from the directory
	full_corpus = ''
	for filename in os.listdir(directory):
		with open(directory+"/"+filename, 'r') as file:
			processed_text = file.read() # at this point data should be already processed
			full_corpus += "\n"+processed_text

	# split the full corpus and count occurrences
	Freq = Counter(full_corpus.split())
	most_occur = Freq.most_common(integer)

	# returns a list of pairs ('word', #of_occurences)
	return(most_occur)


def mask_corpus(directory_in, directory_out, mfw_list):

    # Define protected words and word-matching regex pattern
    protected_words = set(word[0] for word in mfw_list)
    single_word_pattern = re.compile(r'\b[a-z]+\b') 

    # Defines replacement function to call for each matched word
    def mask_match(match):
        word = match.group(0)  # Extract the matched word
        return word if word in protected_words else "MASKEDTOKEN"

    # Open unmasked files
    for filename in os.listdir(directory_in):
        with open(directory_in+"/"+filename, 'r') as file:
            text_unmasked = file.read()
            text_masked = single_word_pattern.sub(mask_match, text_unmasked)

        with open(directory_out+"/"+filename[:-4]+"_masked.txt", 'w') as file:
            file.write(text_masked)


unmasked_data = "../data_Langton_only/corpus_Langton_by_stemma_processed"
masked_data = "../data_Langton_only/corpus_Langton_by_stemma_processed_masked"


mfw_list = get_mfw(unmasked_data, 200)


# safety check: compare the mfw list generated here and in stylo
# declare the two lists - stylo by default saves its in wordlist.txt

List_from_stylo = ["et","est","in","quod","non","ad","ergo","de","si","hoc","quia","sed","ut","per","uel","cum","secundum","a","esse","sit","ex","sunt","sicut","que","qui","item","deus","potest","enim","dicitur","sic","autem","set","quam","deo","hec","se","ita","unde","dicit","tamen","ab","contra","pro","dicendum","eius","nec","nisi","ei","scilicet","aut","aliquid","habet","dei","peccatum","uidetur","illud","modo","eo","propter","iste","illa","dicimus","pater","ratione","ideo","tantum","causa","filius","omnia","uero","utrum","etiam","deum","nomen","fuit","quo","bonum","eum","licet","uult","quid","homo","alia","uera","spiritus","idem","praeterea","eadem","essentia","esset","primum","similiter","uerbum","aliud","ibi","debet","essentiam","magis","solutio","siue","aliquis","ea","dictum","dominus","unum","pena","persona","ille","primo","res","falsa","uerum","ipse","potentia","ipsum","inquantum","ubi","omnis","peccat","augustinus","id","facit","supra","tenetur","responsio","super","diuina","igitur","nichil","qua","idest","omnibus","filium","filio","diuinis","hic","motus","principium","sint","tunc","aliqua","sine","patre","alio","quando","una","queritur","sequitur","possit","quedam","rei","quantum","ecclesie","rationem","patet","actio","fit","quis","respondeo","prius","oportet","eis","illo","sub","nam","solum","inter","ne","sibi","aliquo","intellectus","neque","ecclesia","ratio","sanctus","illis","significat","quare","dici","suam","matrimonium","talis","falsum","illum","forma","eam","omne","modum","mortale","erit","quandoque","suum","uoluntas","effectus","te","huiusmodi","peccati","eorum","nobis"]
my_list = [entry[0] for entry in mfw_list]

# The List below should be empty if both lists are identical; otherwise, it will indicate different records.
all_differences = [[i,j[0]] for i, j in zip(my_list, mfw_list) if i != j[0]]

# nonempty list is automatically assumed to be TRUE, empty is FALSE
if all_differences:
	print(f"Note the following differences: {all_differences}")
else:
	print("The two lists are identical.")


# save_processed_data(actual_data, actual_processed_data)
mask_corpus(unmasked_data, masked_data, mfw_list)
