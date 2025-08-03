# This is the program that calculates the best reconstruction of a number of samples 
# for the thesis of Katharina Will submitted in partial fulfilment of the 
# requirements for the degree of Bachelor of Arts in International Studies in 
# Computational Linguistics at the University of Tübingen.

# imports
from itertools import product
import sys

# example: python3 parse-sample-combine-substrings.py file_path output_file

# sys.argv[0] = this python file
file_path = sys.argv[1]
output_file = sys.argv[2]

def greedy_match(word, sound_inventory_set):
    matched, i = [], 0
    max_length = min(3, len(word))  # max match length is 3
    
    while i < len(word):
        for j in range(max_length, 0, -1):
            candidate = word[i:i + j]
            if candidate in sound_inventory_set:
                matched.append(candidate)
                i += j
                break
        else:
            i += 1  # move forward if no match
    
    return matched

def generate_substrings(word_list, sound_inventory_set):
    substring_set = set()
    cache = {}

    for word in word_list:
        if word in cache:
            split = cache[word]
        else:
            split = greedy_match(word, sound_inventory_set)
            cache[word] = split
        for i in range(len(split)):
            for j in range(i+1,len(split)):
                substring_set.update([tuple(split[i:j])])

    return sorted(substring_set)

def generate_combinations(substrings, k, longest_substring):
    combinations = []
    for seq in product(substrings, repeat=k):
        combination = "".join(["".join(s) for s in seq])
        if len(combination) <= longest_substring:
            combinations.append(combination)
    return sorted(combinations)

def levenshtein_distance(s1, s2):
    len_s1, len_s2 = len(s1), len(s2)
    
    dp = [[0 for _ in range(len_s2 + 1)] for _ in range(len_s1 + 1)]
    
    for i in range(len_s1 + 1):
        dp[i][0] = i
    for j in range(len_s2 + 1):
        dp[0][j] = j

    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # deletion
                dp[i][j - 1] + 1,      # insertion
                dp[i - 1][j - 1] + cost  # substitution
            )
    
    return dp[len_s1][len_s2]

def levenshtein_minimization(samples, candidates):
    min_distance = float('inf')
    best_candidate = None
    
    for candidate in candidates:
        distance_sum = sum(levenshtein_distance(candidate, sample[0]) * sample[1] for sample in samples)
        
        if distance_sum < min_distance:
            min_distance = distance_sum
            best_candidate = candidate
    
    return best_candidate

def parse_samples_file(file_path, max_samples=None, ignore_max_samples=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    
    all_samples = []
    current_samples = []
    word_list = []
    in_samples_section = False
    current_id = None

    for line in data:
        line = line.strip()
        if line == "----":
            if current_samples:
                all_samples.append(current_samples)
                current_samples = []
            in_samples_section = False
            current_id = None
            continue
        if line.startswith("ID "):
            current_id = (line.split(" ")[1],)
            word_list.append(current_id[0])
            continue
        if line == "SAMPLES":
            if current_id:
                current_samples.append(current_id)
            in_samples_section = True
            continue
        if in_samples_section and line:
            parts = line.split("\t")
            if len(parts) == 2:
                word, weight = parts[0], float(parts[1])
                current_samples.append((word, weight))
    
    if current_samples:
        all_samples.append(current_samples)
    
    return all_samples, word_list

max_samples = 100
ignore_max_samples = True
sound_inventory = [
    'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z', 
    'ç', 'ð', 'ħ', 'ŋ', 'ɕ', 'ɡ', 'ɢ', 'ɣ', 'ɫ', 'ɬ', 'ɮ', 'ɰ', 'ɲ', 'ɴ', 'ʋ', 'ɸ', 'ɾ', 'ʁ', 'ʂ', 'ʃ', 
    'ʐ', 'ʑ', 'ʒ', 'ʔ', 'ʕ', 'ʝ', 'ȷ̃', 'β', 'γ', 'θ', 'χ', 'pʰ', 'tʰ', 'kʰ', 'gʰ', 'sʰ', 'sʰ͈', 'tsʰ', 
    'tʃʰ', 'tɕʰ', 'p͈', 't͈', 'k͈', 's͈', 'tɕ͈', 'dz', 'dʑ', 'dʒ', 'ɡʲ', 'kʲ', 'mʲ', 'pʲ', 'ɾʲ', 'bʲ', 
    'ts', 'tɕ', 'tʃ', 'kʷ', 'ɡʷ', 'ʑʷ', 'tsˀ', 'tˀ', 'kˀ', 'pˀ', 'a', 'ɑ', 'ɐ', 'ɒ', 'ä', 'e', 'i', 'o', 'u', 'ɔ', 'y', 'æ', 'ø', 'œ', 'ɵ', 
    'ə', 'ɨ', 'ɪ', 'ɯ', 'ʉ', 'ʊ', 'ʌ', 'ɛ', 'ɘ', 'ʏ', 'aː', 'ɑː', 'ɐː', 'ɒː', 'äː', 'eː', 'iː', 'oː', 'uː', 'ɔː', 'yː', 'æː', 'øː', 'œː', 'ɵː', 
    'əː', 'ɨː', 'ɪː', 'ɯː', 'ʉː', 'ʊː', 'ʌː', 'ɛː', 'ɘː', 'ʏː'
]

sound_inventory_set = set(sound_inventory)

samples_data, word_list = parse_samples_file(file_path, max_samples, ignore_max_samples)

# process each block separately and write results to file
with open(output_file, "w", encoding="utf-8") as f:
    for sample_block in samples_data:
        substrings = generate_substrings([sample[0] for sample in sample_block[1:]], sound_inventory_set)
        longest_substring = 8
        for substring in substrings:
            if len(substring) > longest_substring:
                longest_substring = len(substring)
        combination_results = generate_combinations(substrings, 2, longest_substring)
        print(len(combination_results))
        
        best_reconstruction = levenshtein_minimization(sample_block[1:], combination_results)
        
        f.write(f"Best reconstruction for {sample_block[0][0]}: {best_reconstruction}\n")
        f.flush()

