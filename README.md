# transeurasian-goblin
This is the complete script that pre-processes the data needed for the program GOBLIN to perform its statistical analysis for the thesis of Katharina Celia Will submitted in partial fulfilment of the requirements for the degree of Bachelor of Arts in International Studies in Computational Linguistics at the University of Tübingen.

## First Steps
In order to start the proper reconstruction process with GOBLIN the following steps should be followed.
### Step 1
Compile a cognate table in a tab-separated CSV file.
### Step 2
Run the file script.py in the repository.\
This script will lowercase all entries in the cognate CSV file.\
Next, it will remove all digits and punctuation as well as create IDs for the 'Meaning' column of the CSV file. Question marks are added to empty cells.\
After this small cleaning session the script splits the cognate CSV file into five separate CSV files (Turkic, Mongolic, Tungusic, Koreanic, Japonic).\
Next, the script will convert every entry in each cognate CSV file (Turkic, Mongolic, Tungusic, Koreanic, Japonic) into their International Phonetic Alphabet (IPA) variant.\
After every entry has been converted into IPA, the sound inventory of each language family is created.
### Step ...
transeurasian-script.py runs all the steps mentions in Step 2, but keeping all languages in one CSV file and in one Transeurasian .cog file. This is for reconstructing a Transeurasian ancestor language.
### Step ...
sample-file-extractor.py extracts all entries of a specified Glottolog ID from a log file.
### Step ...
parse_sample_combine_substrings.py generates the best reconstruction for the samples of an ID.


### Add On
file path: python3 script.py\
sys.argv[0] = this python file\
sys.argv[1] = csv_file_path allLanguages.csv\
sys.argv[2] = output_file koreanic.csv\
sys.argv[3] = output_file japonic.csv\
sys.argv[4] = output_file mongolic.csv\
sys.argv[5] = output_file tungusic.csv\
sys.argv[6] = output_file turkic.csv\
sys.argv[7] = consonant_file consonants_ipa2.txt\
sys.argv[8] = vowel_file vowels_ipa2.txt\
sys.argv[9] = ipa_consonant_file kor-consonants.ipa\
sys.argv[10] = ipa_consonant_file jap-consonants.ipa\
sys.argv[11] = ipa_consonant_file mon-consonants.ipa\
sys.argv[12] = ipa_consonant_file tung-consonants.ipa\
sys.argv[13] = ipa_consonant_file turk-consonants.ipa\
sys.argv[14] = ipa_vowel_file kor-vowels.ipa\
sys.argv[15] = ipa_vowel_file jap-vowels.ipa\
sys.argv[16] = ipa_vowel_file mon-vowels.ipa\
sys.argv[17] = ipa_vowel_file tung-vowels.ipa\
sys.argv[18] = ipa_vowel_file turk-vowels.ipa\
sys.argv[19] = cog_filename kor.cog\
sys.argv[20] = cog_filename jap.cog\
sys.argv[21] = cog_filename mon.cog\
sys.argv[22] = cog_filename tung.cog\
sys.argv[23] = cog_filename turk.cog

