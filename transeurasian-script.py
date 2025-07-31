# This is the complete script that pre-processes the data needed for the program GOBLIN to perform its 
# statistical analysis for the thesis of Katharina Will submitted in partial fulfilment of the 
# requirements for the degree of Bachelor of Arts in International Studies in 
# Computational Linguistics at the University of Tübingen.

# imports
import pandas as pd
import sys
import re
import csv
import string
import shutil

# example: python3 transeurasian-script.py transeurasian.csv transeurasian.cog

# lowercase all entries in the dataframe
def lowercase(df):
    for col in df.columns:
        if col != '#id' and col != 'Meaning':
            df[col] = df[col].apply(lambda x: x.lower() if isinstance(x, str) else x)
    return df
    
# remove digits and punctuation
remove_chars = "=-/ (){}[]'.ˈ+*#;,=’~<>\""

remove_chars += string.digits

def remove_digits_punctuation(cell):
    return cell.translate(str.maketrans('', '', remove_chars))

def clean_cell(df):
    id_index, meaning_index = df.columns.get_loc('#id'), df.columns.get_loc('Meaning')
    
    for i, row in df.iterrows():
        for j, cell in enumerate(row):
            if j not in [id_index, meaning_index]:
                if pd.isna(cell):
                    df.iat[i, j] = ''
                else:
                    df.iat[i, j] = remove_digits_punctuation(str(cell))

# IPA transcription dictionaries
koreanic = {
    'ay': 'ɛ', 'ya': 'ja', 'yay': 'jɛ', 'wa': 'wa', 'way': 'wɛ', 'e': 'ʌ', 'ey': 'e', 'ye': 'jʌ', 
    'yey': 'je', 'we': 'wʌ', 'wey': 'we', 'oy': 'ø', 'yo': 'jo', 'wu': 'u', 'wi': 'y', 'yu': 'ju', 
    'u': 'ɯ', 'uy': 'ɰi', 'ng': 'ŋ', 't': 'd', 'k': 'g', 'ph': 'pʰ', 'th': 'tʰ', 'kh': 'kʰ', 
    'pp': 'p͈', 'tt': 't͈', 'kk': 'k͈', 'ch': 'tɕʰ', 'cc': 'tɕ͈', 'c': 'tɕ', 's': 'sʰ', 'ss': 's͈', 'l': 'ɾ',
    'k̚': 'g', 't̕': 'd'
}

koreanic2 = {
    'ay': 'ɛ', 'ya': 'ja', 'yay': 'jɛ', 'wa': 'wa', 'way': 'wɛ', 'e': 'ʌ', 'ey': 'e', 'ye': 'jʌ', 
    'yey': 'je', 'we': 'wʌ', 'wey': 'we', 'oy': 'ø', 'yo': 'jo', 'wu': 'u', 'wi': 'y', 'yu': 'ju', 
    'u': 'ɯ', 'uy': 'ɰi', 'ng': 'ŋ', 't': 'd', 'k': 'g', 'ph': 'p', 'th': 't', 'kh': 'k', 
    'pp': 'p', 'tt': 't', 'kk': 'k', 'ch': 'tɕ', 'cc': 'tɕ', 'c': 'tɕ', 's': 's', 'ss': 's', 'l': 'ɾ',
    'k̚': 'g', 't̕': 'd', 'ː': ''
}

japonic = {
    'by': 'bʲ', 'h': 'ç', 'hy': 'ç', 'sh': 'ɕ', 'ssh': 'ɕ', 'z': 'dz', 
    'zz': 'dz', 'j': 'dʑ', 'jj': 'dʑ', 'f': 'ɸ', 'gy': 'ɡʲ', 'y': 'j', 
    'kk': 'k', 'ky': 'kʲ', 'kky': 'kʲ', 'my': 'mʲ', 'ny': 'ɲ', 'i̥': 'i', 
    'py': 'pʲ', 'ppy': 'pʲ', 'r': 'ɾ', 'ry': 'ɾʲ', 'ss': 's', 
    'tt': 't', 'ch': 'tɕ', 'tch': 'tɕ', 'tts': 'ts', 'shi': 'ɕi', 
    'u': 'ɯ', 'su': 'sɯ', 'u̥': 'u', 'ɯ̥': 'ɯ', 'ɴɴ': 'ɴ', 'nn': 'n',
    'ï': 'ɨ', 'μ': 'm', 'c': 'tʃʰ', 'k': 'kʰ', 't': 'tʰ', 
    'p': 'pʰ', 'j': 'dz', 'ë': 'ɘ', 'C': 'tʃ', 'K': 'k', 
    'T': 't', 'P': 'p', 'π': 'ɸ', 'κ': 'kʷ', 'gw': 'ɡʷ', 
    'τ': 't', 'ii': 'iː', 'aa': 'aː', 'ee': 'eː', 'uu': 'uː', 
    'oo': 'oː', 'ïï': 'iː', 'si': 'ʃi', 'se': 'ʃe', 'sya': 'ʃa', 
    'syu': 'ʃu', 'dy': 'dʑ', 'ni': 'ɲi', 'hi': 'çi', 'hw': 'ɸ', 
    'hu': 'ɸu', 'he': 'çe', 'v': 'ʋ', 'h̥': 'h', 't̥': 't', 
    'kh': 'kʰ', 'th': 'tʰ', 'cc': 'tsˀ', 'tt': 'tˀ', 'kk': 'kˀ', 
    'pp': 'pˀ', 'ïï': 'ɨː', 'í': 'i', 'ì': 'i',
    'i̥̥': 'i', 'á': 'a', 'à': 'a', 'â': 'a', 'ú': 'u', 'μ': 'm',
    'ù': 'u', 'û': 'u', 'oo': 'oː', 'ee': 'eː', 
    'ddz': 'dz', 'ɘɘ': 'ɘː', 'ɂ': 'ʔ', 'ɯɯ': 'ɯː', 'ç̥': 'ç'
}

japonic2 = {
    'by': 'b', 'h': 'ç', 'hy': 'ç', 'sh': 'ɕ', 'ssh': 'ɕ', 'z': 'dz', 
    'zz': 'dz', 'j': 'dʑ', 'jj': 'dʑ', 'f': 'ɸ', 'gy': 'ɡ', 'y': 'j', 
    'kk': 'k', 'ky': 'k', 'kky': 'k', 'my': 'm', 'ny': 'ɲ', 'i̥': 'i', 
    'py': 'p', 'ppy': 'p', 'r': 'ɾ', 'ry': 'ɾ', 'ss': 's', 
    'tt': 't', 'ch': 'tɕ', 'tch': 'tɕ', 'tts': 'ts', 'shi': 'ɕi', 
    'u': 'ɯ', 'su': 'sɯ', 'u̥': 'u', 'ɯ̥': 'ɯ', 'ɴɴ': 'ɴ', 'nn': 'n',
    'ï': 'ɨ', 'μ': 'm', 'c': 'tʃ', 'k': 'k', 't': 't', 
    'p': 'p', 'j': 'dz', 'ë': 'ɘ', 'C': 'tʃ', 'K': 'k', 
    'T': 't', 'P': 'p', 'π': 'ɸ', 'κ': 'k', 'gw': 'ɡ', 
    'τ': 't', 'ii': 'i', 'aa': 'a', 'ee': 'e', 'uu': 'u', 
    'oo': 'o', 'ïï': 'i', 'si': 'ʃi', 'se': 'ʃe', 'sya': 'ʃa', 
    'syu': 'ʃu', 'dy': 'dʑ', 'ni': 'ɲi', 'hi': 'çi', 'hw': 'ɸ', 
    'hu': 'ɸu', 'he': 'çe', 'v': 'ʋ', 'h̥': 'h', 't̥': 't', 
    'kh': 'k', 'th': 't', 'cc': 'ts', 'tt': 't', 'kk': 'k', 
    'pp': 'p', 'ïï': 'ɨ', 'í': 'i', 'ì': 'i',
    'i̥̥': 'i', 'á': 'a', 'à': 'a', 'â': 'a', 'ú': 'u', 'μ': 'm',
    'ù': 'u', 'û': 'u', 'oo': 'o', 'ee': 'e', 
    'ddz': 'dz', 'ɘɘ': 'ɘ', 'ɂ': 'ʔ', 'ɯɯ': 'ɯ', 'ç̥': 'ç', 'ː': ''
}

fix_japonic = {
    'i̥': 'i', 'ɯ̥': 'ɯ', 'î': 'i'
}

mongolic = {
    'å': 'a', 'åå': 'aː', 'ë': 'e', 'ëː': 'eː', 'ee': 'eː', 'ɯɯ': 'ɯː', 'oo': 'oː', 'Ï': 'I', 'ï': 'i', 'ÏÏ': 'iː', 'ïï': 'iː', 'ɨɨ': 'ɨː', 'aa': 'aː', 'ɒ': 'ɒ',
    'â': 'a', 'ã': 'a', 'ä': 'a', 'î': 'i', 'ĭ': 'i', 'ii': 'iː', 'ā': 'aː', 'ē': 'eː', 'ė': 'ə', 'ğ': 'ɣ', 'ġ': 'g', 'ǧ': 'g', 'ī': 'i', 'ĭ': 'ɪ', 'ı': 'ɯ', 'ɒɒ': 'ɒː',
    'ĺ': 'ɮ', 'ō': 'o', 'ś': 'ʃ', 'ŭ': 'ʊ', 'ź': 'ʒ', 'ž': 'ʒ', 'ǯ': 'ʒ', 'ʉ:': 'ʉː', 'ǖ': 'ʉː', '\:': 'ː', 'ǰ': 'dʒ', 'ǵ': 'g', 'ȵ': 'ɲ', 'n̥': 'ɲ', 'ɒɒ': 'ɒː',
    'ɵ': 'ɔ', 'ɿ': 'i', 'ʣ': 'dz', 'ʤ': 'dʒ', 'ʥ': 'dʑ', 'ʦ': 'ts', 'ʧ': 'tʃ', 'ʨ': 'tɕ', 'δ': 'ð', 'ε': 'ɛ', 'б': 'b', 'μ': 'm', 'а': 'a', 'в': 'w', 'ʊʊ': 'ʊː', 'y:': 'j',
    'г': 'ʁ', 'д': 'd', 'е': 'eː', 'ж': 'tʃ', 'з': 'z', 'и': 'i', 'к': 'k', 'л': 'ɮ', 'н': 'n', 'о': 'ɔ', 'р': 'r', 'с': 's', 'у': 'u', 'ф': 'f', 'х': 'x', 'øø': 'øː',
    'ч': 'tʃ', 'ш': 'ʃ', 'ş': 'ʃ', 'ы': 'ɨ', 'э': 'e', 'ё': 'jɵ', 'ө': 'o', 'ẹ': 'ɛ', 'ị': 'i', 'ọ': 'o', 'ụ': 'u', 'U': 'ʏ','ȷ': 'j', 'κ': 'k', 'oo': 'ɔː', 'ːː': 'ː',
    't́': 't', 'ǝ': 'ə', 'ɴɴ': 'ɴ', 'nn': 'n', 'ɯ̥': 'ɯ', 'ɘɘ': 'ɘː', "'": 'ʔ', ':': 'ː', '­': '', 'ś': 's', 'ē̆': 'e', 'ā': 'a', 'ī': 'i', 'x́': 'x', 'ʉʉ': 'ʉː', 'ʹ': '',
    'ü': 'ʉ', 'üü': 'ʉː', 'u': 'ʊ', 'uu': 'ʊː', 'í': 'i', 'v': 'w', 'ʒ': 'ts', 'z': 'ts', 'ǯ': 'tʃ', 'y': 'j', 'č': 'tʃ', 'š': 'ʃ', 'ǰ': 'tʃ', 'ö': 'ɵ', '˳': '', '́': '',
    'öö': 'oː', 'o': 'ɔ', 'ū': 'uː', 'ǟ': 'æː', 'l': 'ɮ', 'c': 'tsʰ', 'yy': 'yː', 'ḿ': 'm', 'ȧ': 'a', 'ƺ': 'ʑʷ', 'sh': 'ʃ', 'ɵɵ': 'ɵː', 'əə': 'əː', 'ɛɛ': 'ɛː', '：': 'ː'
}

mongolic2 = {
    'å': 'a', 'åå': 'a', 'ë': 'e', 'ëː': 'e', 'ee': 'e', 'ɯɯ': 'ɯ', 'oo': 'o', 'Ï': 'I', 'ï': 'i', 'ÏÏ': 'i', 'ïï': 'i', 'ɨɨ': 'ɨ', 'aa': 'a', 'ɒ': 'ɒ',
    'â': 'a', 'ã': 'a', 'ä': 'a', 'î': 'i', 'ĭ': 'i', 'ii': 'i', 'ā': 'a', 'ē': 'e', 'ė': 'ə', 'ğ': 'ɣ', 'ġ': 'g', 'ǧ': 'g', 'ī': 'i', 'ĭ': 'ɪ', 'ı': 'ɯ', 'ɒɒ': 'ɒ',
    'ĺ': 'ɮ', 'ō': 'o', 'ś': 'ʃ', 'ŭ': 'ʊ', 'ź': 'ʒ', 'ž': 'ʒ', 'ǯ': 'ʒ', 'ʉ:': 'ʉ', 'ǖ': 'ʉ', '\:': '', 'ǰ': 'dʒ', 'ǵ': 'g', 'ȵ': 'ɲ', 'n̥': 'ɲ', 'ɒɒ': 'ɒ',
    'ɵ': 'ɔ', 'ɿ': 'i', 'ʣ': 'dz', 'ʤ': 'dʒ', 'ʥ': 'dʑ', 'ʦ': 'ts', 'ʧ': 'tʃ', 'ʨ': 'tɕ', 'δ': 'ð', 'ε': 'ɛ', 'б': 'b', 'μ': 'm', 'а': 'a', 'в': 'w', 'ʊʊ': 'ʊ', 'y:': 'j',
    'г': 'ʁ', 'д': 'd', 'е': 'e', 'ж': 'tʃ', 'з': 'z', 'и': 'i', 'к': 'k', 'л': 'ɮ', 'н': 'n', 'о': 'ɔ', 'р': 'r', 'с': 's', 'у': 'u', 'ф': 'f', 'х': 'x', 'øø': 'ø',
    'ч': 'tʃ', 'ш': 'ʃ', 'ş': 'ʃ', 'ы': 'ɨ', 'э': 'e', 'ё': 'jɵ', 'ө': 'o', 'ẹ': 'ɛ', 'ị': 'i', 'ọ': 'o', 'ụ': 'u', 'U': 'ʏ','ȷ': 'j', 'κ': 'k', 'oo': 'ɔ', 'ːː': '',
    't́': 't', 'ǝ': 'ə', 'ɴɴ': 'ɴ', 'nn': 'n', 'ɯ̥': 'ɯ', 'ɘɘ': 'ɘ', "'": 'ʔ', ':': '', '­': '', 'ś': 's', 'ē̆': 'e', 'ā': 'a', 'ī': 'i', 'x́': 'x', 'ʉʉ': 'ʉ', 'ʹ': '',
    'ü': 'ʉ', 'üü': 'ʉ', 'u': 'ʊ', 'uu': 'ʊ', 'í': 'i', 'v': 'w', 'ʒ': 'ts', 'z': 'ts', 'ǯ': 'tʃ', 'y': 'j', 'č': 'tʃ', 'š': 'ʃ', 'ǰ': 'tʃ', 'ö': 'ɵ', '˳': '', '́': '',
    'öö': 'o', 'o': 'ɔ', 'ū': 'u', 'ǟ': 'æ', 'l': 'ɮ', 'c': 'ts', 'yy': 'y', 'ḿ': 'm', 'ȧ': 'a', 'ƺ': 'ʑ', 'sh': 'ʃ', 'ɵɵ': 'ɵ', 'əə': 'ə', 'ɛɛ': 'ɛ', '：': '', 'ː': ''
}

tungusic = {
    'č': 'ts', 'š': 'ʃ', 'ś': 'ʃ', 'y': 'j', 'ị': 'i', 'ịị': 'iː', 'ɨ': 'i', 'ɨɨ': 'iː', 'ď': 'dʒ', 'oo': 'oː', 'uu': 'uː', 'ee': 'eː', 'ii': 'iː', 'ɔɔ': 'ɔː',
    'ö': 'œ', 'öö': 'œː', 'ọ': 'ɵ', 'ọọ': 'ɵː', 'ü': 'ʉ', 'üü': 'ʉː', 'ụ': 'u', 'ụụ': 'uː', 'û': 'ʊ', 'ûû': 'ʊː', 'ń': 'ɲ', 'ň': 'ŋ', 'è': 'e', 'èè': 'eː',
    'aa': 'aː', 'ä': 'æ', 'ää': 'æː', 'ụ': 'u', 'ọ': 'o', 't͡ʃ': 'tʃ', ':': 'ː', 'ú': 'u', 'á': 'a', 'ń': 'ɲ', 'ͻ': 'ɔ', 'əə': 'əː', 'ʤ': 'dʒ', 'ɒɒ': 'ɒː',
    'ˀ': 'ʔ', 'ё': 'jɵ', 'oo': 'oː', 'ʧ': 'tʃ', 'ǯ': 'ʒ', 'ʣ': 'dz', 'ǝ': 'ə', 'yː': 'yː', 'pʰ': 'pʰ', 'ó': 'o', 'ə́': 'ə', 'е': 'eː', 'е': 'e', 'ǰ': 'dʒ',
    'ė': 'e', 'é': 'e', 'ō': 'o', 'ị': 'i', 'ʾ': '', '̣': ''
}

tungusic2 = {
    'č': 'ts', 'š': 'ʃ', 'ś': 'ʃ', 'y': 'j', 'ị': 'i', 'ịị': 'i', 'ɨ': 'i', 'ɨɨ': 'i', 'ď': 'dʒ', 'oo': 'o', 'uu': 'u', 'ee': 'e', 'ii': 'i', 'ɔɔ': 'ɔ',
    'ö': 'œ', 'öö': 'œ', 'ọ': 'ɵ', 'ọọ': 'ɵ', 'ü': 'ʉ', 'üü': 'ʉ', 'ụ': 'u', 'ụụ': 'u', 'û': 'ʊ', 'ûû': 'ʊ', 'ń': 'ɲ', 'ň': 'ŋ', 'è': 'e', 'èè': 'e',
    'aa': 'a', 'ä': 'æ', 'ää': 'æ', 'ụ': 'u', 'ọ': 'o', 't͡ʃ': 'tʃ', ':': '', 'ú': 'u', 'á': 'a', 'ń': 'ɲ', 'ͻ': 'ɔ', 'əə': 'ə', 'ʤ': 'dʒ', 'ɒɒ': 'ɒ',
    'ˀ': 'ʔ', 'ё': 'jɵ', 'oo': 'o', 'ʧ': 'tʃ', 'ǯ': 'ʒ', 'ʣ': 'dz', 'ǝ': 'ə', 'yː': 'y', 'pʰ': 'p', 'ó': 'o', 'ə́': 'ə', 'е': 'e', 'е': 'e', 'ǰ': 'dʒ',
    'ė': 'e', 'é': 'e', 'ō': 'o', 'ị': 'i', 'ʾ': '', '̣': '', 'ː': ''
}

turkic = {
    'dd': 'd', 'c': 'dʒ', 'y': 'ɯ', 'ý': 'j', 'r': 'ɾ', 'ş': 'ʃ', 'š': 'ʃ', 'ç': 'tʃ', 'č': 'tʃ', 'j': 'ʒ', 'ǰ': 'ʒ', 'L': 'l', 'l': 'ɫ', 'ḳ': 'q', 
    'ö': 'œ', 'ı': 'ɯ', 'ü': 'ʏ', 'ğ': 'ɣ', 'â': 'aː', 'î': 'iː', 'û': 'uː', 'ï': 'i', ':': 'ː', 'w': 'β', 'ġ': 'g', 'ň': 'ŋ', 'ń': 'ɲ', 's': 'θ', 
    'g': 'ɢ', 'z': 'ð', 'x': 'χ', 'ś': 'ʃ', 'ỹ': 'ȷ̃', 'ii': 'iː', 'ïï': 'ɯː', 'ïa': 'ɯa', 'e': 'ɛ', 'ee': 'eː', 'aa': 'aː', 'ää': 'æː', 'üü': 'yː',
    'üö': 'yø', 'uu': 'uː', 'uo': 'uɔ', 'öö': 'øː', 'o': 'ɔ', 'oo': 'ɔː', 'üý': 'ʏː', 'a': 'ɑ', 'u': 'ʊ', 'ĕ': 'e', 'ĕĕ': 'eː', 'ɣ': 'ʁ', 'ọ': 'o', 
    '\?': '', 'ź': 'ʒ', 'ǧ': 'g', '2': 'ø', 'j̃': 'ȷ̃', 'əʷ': 'ə', 'ǵ': 'g', 'ĭ': 'i', 'ɑɑ': 'ɑː', 'œː': 'øː', 'ń': 'n', 'ž': 'ʒ', 'ˁ': 'ʕ', 'δ': 'ð',
    'ụ': 'u', 'ɘʷ': 'ɘ', '́': '', 'd́': 'd', 'ɛɛ': 'ɛː', '?': 'ɣ', '`': '', 'ŭ': 'u', 'ẹ': 'e', 't́': 't', 'ʊʊ': 'ʊː', 'ō': 'o', 'å': 'ɑ',
    'ǯ': 'ʒ', 'ж': 'tʃ', 'и': 'i', 'ää': 'äː', 'ā': 'a', 'ọr': 'ɔɾ', 'р': 'p', 'œœ': 'œː', 'ọ': 'ɔ'
}

turkic2 = {
    'dd': 'd', 'c': 'dʒ', 'y': 'ɯ', 'ý': 'j', 'r': 'ɾ', 'ş': 'ʃ', 'š': 'ʃ', 'ç': 'tʃ', 'č': 'tʃ', 'j': 'ʒ', 'ǰ': 'ʒ', 'L': 'l', 'l': 'ɫ', 'ḳ': 'q', 
    'ö': 'œ', 'ı': 'ɯ', 'ü': 'ʏ', 'ğ': 'ɣ', 'â': 'a', 'î': 'i', 'û': 'u', 'ï': 'i', ':': '', 'w': 'β', 'ġ': 'g', 'ň': 'ŋ', 'ń': 'ɲ', 's': 'θ', 
    'g': 'ɢ', 'z': 'ð', 'x': 'χ', 'ś': 'ʃ', 'ỹ': 'ȷ̃', 'ii': 'i', 'ïï': 'ɯ', 'ïa': 'ɯa', 'e': 'ɛ', 'ee': 'e', 'aa': 'a', 'ää': 'æ', 'üü': 'y',
    'üö': 'yø', 'uu': 'u', 'uo': 'uɔ', 'öö': 'ø', 'o': 'ɔ', 'oo': 'ɔ', 'üý': 'ʏ', 'a': 'ɑ', 'u': 'ʊ', 'ĕ': 'e', 'ĕĕ': 'e', 'ɣ': 'ʁ', 'ọ': 'o', 
    '\?': '', 'ź': 'ʒ', 'ǧ': 'g', '2': 'ø', 'j̃': 'ȷ̃', 'əʷ': 'ə', 'ǵ': 'g', 'ĭ': 'i', 'ɑɑ': 'ɑ', 'œː': 'ø', 'ń': 'n', 'ž': 'ʒ', 'ˁ': 'ʕ', 'δ': 'ð',
    'ụ': 'u', 'ɘʷ': 'ɘ', '́': '', 'd́': 'd', 'ɛɛ': 'ɛ', '?': 'ɣ', '`': '', 'ŭ': 'u', 'ẹ': 'e', 't́': 't', 'ʊʊ': 'ʊ', 'ō': 'o', 'å': 'ɑ',
    'ǯ': 'ʒ', 'ж': 'tʃ', 'и': 'i', 'ää': 'ä', 'ā': 'a', 'ọr': 'ɔɾ', 'р': 'p', 'œœ': 'œ', 'ọ': 'ɔ', 'ː': '', 'ị': 'i'
}

simplified_IPA = {
    'ː': '', 'sʰ͈': 's', 'p͈': 'p', 't͈': 't', 'k͈': 'k', 's͈': 's', 'tɕ͈': 'tɕ', 'ɡʲ': 'ɡ', 'kʲ': 'k', 'mʲ': 'm',
    'pʲ': 'p', 'ɾʲ': 'ɾ', 'bʲ': 'b', 'kʷ': 'k', 'ɡʷ': 'ɡ', 'ʑʷ': 'ʑ', 'tsˀ': 'ts', 'tˀ': 't', 'kˀ': 'k', 'pˀ': 'p'
}

# define language groups, using their Glottolog ID, for the transcription process
kor_fam = ['jeju1234', 'seou1239', 'midd1372']

jap2 = ['nucl1643', 'oldj1239']
okinawan2 = ['cent2126']
sRyukyuan = ['sats1241', 'hach1239', 'ikem1234', 'yaey1239'] 
jap_fam = [*jap2, *okinawan2, *sRyukyuan]

mon_fam = ['kham1281', 'daur1238', 'east2337', 'mogh1245', 'midd1351', 'bona1250', 'buri1258', 'halh1238', 'kalm1244', 'dong1285', 'minh1238', 'huzh1238']

turk_fam = ['oldu1238', 'bash1264', 'chuv1255', 'dolg1241', 'kara1464', 'khak1248', 'turk1304', 'kirg1245', 'sala1264', 'west2402', 'kaza1248', 
            'tuvi1240', 'uigh1240', 'uzbe1247', 'yaku1245', 'nort2697', 'nucl1301', 'turk1303']

tung_fam = ['nana1257', 'jurc1239', 'manc1252', 'xibe1242', 'even1259', 'oroq1238', 'orok1265', 'ulch1241', 'oroc1248', 'udih1248']

all_fam = [*kor_fam, *jap_fam, *mon_fam, *turk_fam, *tung_fam]

# use greedy matching to transcribe every entry into IPA
def greedy_transcription(text, transcription_dict):
    result = []
    i = 0
    while i < len(text):
        match = None
        for j in range(len(text), i, -1):
            substring = text[i:j]
            if substring in transcription_dict:
                match = transcription_dict[substring]
                result.append(match)
                i = j - 1
                break
        if match is None:
            result.append(text[i])
        i += 1
    return ''.join(result)

def transcribe(file_path, transcription_dict, columns_to_transcribe):
    with open(file_path, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter='\t')
        rows = list(reader)

    header = rows[0]

    for row in rows[1:]:
        for i, cell in enumerate(row):
            if header[i] in columns_to_transcribe:
                row[i] = greedy_transcription(cell, transcription_dict)

    with open(file_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerows(rows)

# add the IDs for every cognate set and remove the 'Meaning' column from the CSV file
def generate_id(meaning, meaning_count):
    if "?" in meaning:
        cleaned_meaning = meaning.replace("?", "").strip()
    
    elif "pronoun" in meaning:
        cleaned_meaning = meaning.replace("pronoun", "").strip()
    
    elif "/" in meaning:
        cleaned_meaning = re.sub(r'\s*\(.*?\)', '', meaning).strip()
        cleaned_meaning = cleaned_meaning.replace(" / ", "_")
        
    elif "(" in meaning:
        match = re.match(r"(\w+\s*\w*)\((\w+)\)\s*(.*)", meaning)
        if match:
            base, parenthetical, rest = match.groups()
            cleaned_meaning = f"{base.strip().replace(' ', '_')}_{parenthetical}_{rest.strip().replace(' ', '_')}"
        else:
            match = re.match(r"(\w+)\s*\((\w+)\)", meaning)
            if match:
                term1, term2 = match.groups()
                cleaned_meaning = f"{term1}_{term2}"
            else:
                match = re.match(r"(\w+)\s+(\w+)", meaning)
                if match:
                    cleaned_meaning = meaning.replace(" ", "_")
                else:
                    cleaned_meaning = re.sub(r'\s*\(.*?\)', '', meaning).strip()
    
    elif re.match(r'\w+\s+\w+', meaning):
        cleaned_meaning = meaning.replace(" ", "_")
    else:
        cleaned_meaning = re.sub(r'\s*\(.*?\)', '', meaning).strip()

    cleaned_meaning = re.sub(r'\s*\(.*?\)', '', cleaned_meaning).strip()
    cleaned_meaning = re.sub(r'__+', '_', cleaned_meaning).strip('_')

    if cleaned_meaning in meaning_count:
        meaning_count[cleaned_meaning] += 1
    else:
        meaning_count[cleaned_meaning] = 1
        
    return f"{cleaned_meaning}_{meaning_count[cleaned_meaning]}"

def apply_generate_id(file_path):
    meaning_count = {}
    df = pd.read_csv(file_path, encoding='utf-8', sep='\t')
    df['#id'] = df['Meaning'].apply(lambda meaning: generate_id(meaning, meaning_count))
    df.to_csv(file_path, index=False, encoding='utf-8', sep='\t')
    
def drop_meaning_column(file_path):
    df = pd.read_csv(file_path, encoding='utf-8', sep='\t')
    df.drop(columns=['Meaning'], inplace=True)
    df.to_csv(file_path, encoding='utf-8', sep='\t', index=False)

# add question marks to every empty cell in the CSV file
def fill_empty_cells_with_question_mark(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        rows = list(reader)

    for row_index, row in enumerate(rows):
        for col_index, cell in enumerate(row):
            if not cell.strip():
                rows[row_index][col_index] = '?'

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerows(rows)
        
# copy the final CSV files to a new format
def copy_file(current_name, new_name):
    try:
        shutil.copyfile(current_name, new_name)
        print(f"File copied from {current_name} to {new_name}")
    except FileNotFoundError:
        print(f"Error: The file {current_name} does not exist.")
    except PermissionError:
        print("Error: You do not have permission to copy this file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# add every method to be executed here#
def main(long_vowels): 
    
    # define columns to be read in for the reduced transeurasian data set
    columns = ['#id', 'Meaning', *kor_fam, *jap_fam, *mon_fam, *turk_fam, *tung_fam]
    
    # read in the initial CSV file with all languages
    csv_file_path = sys.argv[1]
    df = pd.read_csv(csv_file_path, encoding='utf-8', sep='\t', usecols=columns)
    
    # lowercase every entry and clean the cells from digits and punctuation
    lowercase(df) 
    df.to_csv(csv_file_path, index=False, encoding='utf-8', sep='\t')
    
    df2 = pd.read_csv(csv_file_path, encoding='utf-8', sep='\t')
    clean_cell(df2)
    df2.to_csv(csv_file_path, index=False, encoding='utf-8', sep='\t')
    
    output = csv_file_path
    
    language_family = [kor_fam, jap_fam, mon_fam, tung_fam, turk_fam, jap_fam]
      
    # transcribe each entry in the 5 files into IPA
    if long_vowels:
        dictionary = [koreanic, japonic, mongolic, tungusic, turkic, fix_japonic]
    else:
        dictionary = [koreanic2, japonic2, mongolic2, tungusic2, turkic2, fix_japonic]
    
    for dict_, family in zip(dictionary, language_family):
        transcribe(output, dict_, family)
      
    # generate the IDs and drop the 'Meaning' column
    apply_generate_id(output)
      
    drop_meaning_column(output)
        
    # fill every empty cell with a question mark
    fill_empty_cells_with_question_mark(output)
    
    # copy the CSV file to a new .cog file
    cog_filename = sys.argv[2]
    copy_file(output, cog_filename)

if __name__ == "__main__":
    main(long_vowels=False)