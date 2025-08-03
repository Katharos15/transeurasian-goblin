# This is the program that extracts the samples for a specified ID from the log data 
# for the thesis of Katharina Will submitted in partial fulfilment of the 
# requirements for the degree of Bachelor of Arts in International Studies in 
# Computational Linguistics at the University of Tübingen.

from collections import Counter
import sys
import re

# example: python3 sample-file-extractor.py filename_log output_file_txt bolg1249 kipc1240 oghu1243

# sys.argv[0] = this python file
filename_log = sys.argv[1] # log data
output_file_txt = sys.argv[2]
lang_ids = set(sys.argv[3:])
lang_to_pattern = dict()

ipa_symbols = "bcdfghjklmnpqrstvwxyzçðħŋɕɡɢɣɫɬɮɰɲɴʋɸɾʁʂʃʐʑʒʔʕʝȷ̃βγθχʰp͈t͈k͈s͈tɕ͈ʲʷˀaɑɐɒäeiouɔyæøœɵəɨɪɯʉʊʌɛɘʏː"

for lang_id in lang_ids:
  lang_to_pattern[lang_id] = re.compile(lang_id + ":([" + ipa_symbols + "]+)")

with open(output_file_txt, "w") as output_file:
    step = -1
    lang_to_concept_to_counter = dict()

    def print_sample_file(prefix, lang_to_concept_to_counter):
        for lang_id in lang_ids:
            with open(prefix + "-" + lang_id + ".samples", "w") as sample_file:
                concept_to_counter = lang_to_concept_to_counter[lang_id]
                for concept in concept_to_counter.keys():
                    sample_file.write("----\nID " + concept + "\nSAMPLES\n")
                    counter = concept_to_counter[concept]
                    for sample, count in counter.most_common():
                        sample_file.write(sample + "\t" + str(count) + "\n")
                    sample_file.write("\n")

    with open(filename_log, 'r') as log_file:
        for line in log_file:
            if "E step" in line:
                if step >= 0: 
                    print_sample_file("iteration000" + str(step), lang_to_concept_to_counter)
                step += 1
                lang_to_concept_to_counter = dict()
                for lang_id in lang_ids:
                    lang_to_concept_to_counter[lang_id] = dict()
            if "Sampling cognate" in line:
                concept_id = line[line.find("[") + 1:line.find("]")]
            for lang_id in lang_ids:
                match = lang_to_pattern[lang_id].search(line)
                if match:
                    output_line = f"sample000{step}\t{concept_id}\t{lang_id}\t{match.group(1)}"
                    print(output_line)
                    output_file.write(output_line + "\n")
                    if concept_id not in lang_to_concept_to_counter[lang_id]:
                        lang_to_concept_to_counter[lang_id][concept_id] = Counter()
                    lang_to_concept_to_counter[lang_id][concept_id].update([match.group(1)])
        print_sample_file("iteration000" + str(step), lang_to_concept_to_counter)

