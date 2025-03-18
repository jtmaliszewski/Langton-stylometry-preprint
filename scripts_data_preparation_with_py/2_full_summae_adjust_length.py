# Used to draw samples for the test presented in Figure 2.

import os

def get_x_words(filename, word_target=150000):
# Draws texts from the indicated source until the indicated word count is reached.
# Returns the result overwriting any original whitespace, separating each word with a " ".
	with open(filename, 'r') as file:
		full_file_word_by_word = file.read().split()

		word_count = 0
		shortened_text = ""

		while word_count < word_target:
			shortened_text += full_file_word_by_word[word_count] + " "
			word_count += 1

		return(shortened_text)

# select the relevant full-size texts and declare where to save shortened texts
repository_in = "../data_full_summae/corpus_processed"
files_to_shorten = ["Aquinas_STh_prima_pars_processed.txt", "Courson_Summa_cleaner_processed.txt", "Langton_all_qq_processed.txt"]

repository_out = "../data_full_summae/corpus_Aquinas_Courson_Langton"

# Adjust length of files in repository_in; result saved in repository_out
for filename in files_to_shorten:
	shortened_text = get_x_words(f"{repository_in}/{filename}", 150000)

	with open(f"{repository_out}/{os.path.splitext(filename)[0]}_short.txt", "w") as out:
		out.write(shortened_text)	
