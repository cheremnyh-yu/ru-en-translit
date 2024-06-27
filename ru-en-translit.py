import re

def translit(word):
    word = word.lower()
    word = re.sub('[^A-Za-zА-Яа-яЁё ]', '', word)
    
    if bool(re.search('[\u0400-\u04FF]', word)):
        ru_en_transl = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh',
            'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
            'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
            'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'u', 'я': 'ya'}
        
        result = word
        sorted_keys = sorted(ru_en_transl.keys(), key=len, reverse=True)
        for key in sorted_keys:
            result = re.sub(key, ru_en_transl[key], result)

        return result

    elif bool(re.search('[A-Za-z]', word)):
            
        ending_rules =  {"tion": "шн", 
                    "sion": "жн", 
                    "ician" : "ишн"}

        for pattern, replacement in ending_rules.items():
            word = re.sub(pattern, replacement, word)

        #rules for diphthongs
        vowel_patterns = {
            'uou': 'юо', 'aa': 'а', 'ee': "и", 'ii': "йи", 'oo':'у', 'uu': 'уу', 'ae': 'э', 'ie': 'и', 'oe': 'о', 
            'ai': "эй", 'ay': 'эй', 'ei': 'эй', 'ey': 'ей', 'oi': 'ой', 'oy':'ой', 'ou':'ау', 'ow':'оу', 'au':'ау', 'aw':'о', 'ui': 'у', 
            'ogue': 'ог', 'nge': 'ндж', 'oa':'оа', 'qua': 'квэ'
        }

        for pattern, replacement in vowel_patterns.items():
            word = re.sub(pattern, replacement, word)
            
        #rule for iu+r
        vowel_r_patterns = {'ir': 'ер', 'ur': 'ер'}

        for pattern, replacement in vowel_r_patterns.items():
            if not re.search(pattern+'e', word):
                word = re.sub(pattern, replacement, word)

        #rules for single vowels
        vowel_pairs = {
            "i": ['и', 'ай'],
            "o": ['о', 'оу'],
            "u": ['а', 'ю'],
            "a": ['а', 'эй', "э"],
            "e": ["э"]
        }

        def translate_vowels(word):
            for letter in ["i", "o", "u"]:
                closed_syllable = rf'[^aeiouаеоуи]{letter}[^aeiouаеоуи]$|[^aeiouаеоуи]{letter}[^aeiouаеоуи][aiouаоуи]|[^aiouаоуи]{letter}[^aiouаоуи][^aiouаeоуи]'
                open_syllable = rf'[^{letter}]|[^aeiouаеоуи]{letter}[^aeiouаеоуи][e]$|[^aeiouаеоуи]{letter}[^aeiouаеоуи][aeiouаеоуи]|[^aeiouаеоуи]{letter}[gh]'
                if re.search(closed_syllable, word):
                    word = re.sub(letter, vowel_pairs[letter][0], word)
                elif re.search(open_syllable, word):
                    word = re.sub(letter, vowel_pairs[letter][1], word)

            if "a" in word:
                closed_syllable = r'[^aeiouаеоуи]a[^aeiouаеоуи]$'
                open_syllable = r'[^aeiouаеоуи]a[^aeiouаеоуи][e]'
                word_start = r'^a'
                word_end = r'a$'
                if re.search(word_start, word):
                    word = re.sub(word_start, vowel_pairs["a"][2], word)
                elif re.search(closed_syllable, word):
                    word = re.sub("a", vowel_pairs["a"][0], word)
                elif re.search(open_syllable, word):
                    word = re.sub("a", vowel_pairs["a"][1], word)
                elif re.search(word_end, word):
                    word = re.sub(word_end, vowel_pairs["a"][0], word)

            if "e" in word:
                pattern = r'[^aeiouаеоуи]e$'
                if re.search(pattern, word):
                    word = re.sub(r'e$', '', word) 
                else:
                    word = re.sub(r'e', 'е', word) 

            return word
            
        word = translate_vowels(word)

        #rules for double consonants
        consonant_patterns = {'ch': 'ч', 'sh': 'ш', 'zh': 'ж', 'th': 'т', 'ph': 'ф', 'wh': 'в', 'ck': 'к', 'ght': 'т', 'rz': 'рц', 'gg': 'гг'}

        for pattern, replacement in consonant_patterns.items():
            word = re.sub(pattern, replacement, word)

        #rules for single consonants
        consonant_pairs = {"c": ['к', 'с'], "g": ['г', 'дж'], "s": ['с', 'з']}
        hard_vowels = ['a','o','u','а','о','у']
        soft_vowels = ['i','e','y','и','е','й']

        def translate_consonant(word):  
            for letter in consonant_pairs.keys():
                if letter in word:
                    with_hard_vowels = r'{}[{}]|{}$'.format(letter, ''.join(hard_vowels), letter)
                    with_soft_vowels = r'{}[{}]'.format(letter, ''.join(soft_vowels))
                    if re.search(with_hard_vowels, word):
                        word = re.sub(letter, consonant_pairs[letter][0], word)
                    elif re.search(with_soft_vowels, word):
                        word = re.sub(letter, consonant_pairs[letter][1], word)
            return word
                            
        word = translate_consonant(word)

        #replacing remaining letters
        letters = { 
            'b': 'б', 'c': 'к', 'd': 'д', 'f': 'ф', 'g': 'г', 
            'h': 'х', 'j': 'дж', 'k': 'к', 'l': 'л', 'm': 'м', 
            'n': 'н', 'p': 'п', 'q': 'кв', 'r': 'р', 's': 'с', 
            't': 'т', 'v': 'в', 'w': 'в', 'x': 'кс', 'y': 'и', 'z': 'з'
        }

        for letter, replacement in letters.items():
            word = re.sub(letter, replacement, word)

    return word
