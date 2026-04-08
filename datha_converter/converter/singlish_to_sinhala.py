"""
Offline Singlish to Sinhala Unicode Converter
Based on phonetic transliteration rules

Supports:
- Consonants (k, g, ng, ch, j, etc.)
- Vowels (a, aa, i, ii, u, uu, e, ee, o, oo, au)
- Special characters (rakaransaya, yansaya, etc.)
- Mixed English-Sinhala text
"""

class SinhalaUnicodeConverter:
    def __init__(self):
        # Sinhala Unicode ranges: 0D80-0DFF
        
        # Consonants (හල්)
        self.consonants = {
            'k': 'ක', 'K': 'ක',
            'g': 'ග', 'G': 'ග',
            'ng': 'ං', 'N': 'ං',
            'ch': 'ච', 'Ch': 'ච',
            'j': 'ජ', 'J': 'ජ',
            'ny': 'ඤ', 'gn': 'ඤ',
            't': 'ට', 'T': 'ට',
            'd': 'ඩ', 'D': 'ඩ',
            'n': 'න', 'N': 'ණ',
            'th': 'ත', 'Th': 'ත',
            'dh': 'ද', 'Dh': 'ද',
            'p': 'ප', 'P': 'ප',
            'b': 'බ', 'B': 'බ',
            'm': 'ම', 'M': 'ම',
            'y': 'ය', 'Y': 'ය',
            'r': 'ර', 'R': 'ර',
            'l': 'ල', 'L': 'ල',
            'v': 'ව', 'w': 'ව', 'V': 'ව', 'W': 'ව',
            'sh': 'ශ', 'Sh': 'ශ',
            's': 'ස', 'S': 'ස',
            'h': 'හ', 'H': 'හ',
            'f': 'ෆ', 'F': 'ෆ',
            'z': 'ඤ', 'Z': 'ඤ',
            'x': 'ක්ෂ',
        }
        
        # Independent vowels (ස්වර)
        self.vowels = {
            'a': 'අ', 'A': 'අ',
            'aa': 'ආ', 'Aa': 'ආ', 'AA': 'ආ',
            'ae': 'ඇ', 'Ae': 'ඇ',
            'aae': 'ඈ', 'Aae': 'ඈ',
            'i': 'ඉ', 'I': 'ඉ',
            'ii': 'ඊ', 'Ii': 'ඊ', 'II': 'ඊ', 'ee': 'ඊ',
            'u': 'උ', 'U': 'උ',
            'uu': 'ඌ', 'Uu': 'ඌ', 'UU': 'ඌ', 'oo': 'ඌ',
            'e': 'එ', 'E': 'එ',
            'ee': 'ඒ', 'Ee': 'ඒ', 'EE': 'ඒ',
            'ai': 'ඓ', 'Ai': 'ඓ',
            'o': 'ඔ', 'O': 'ඔ',
            'oo': 'ඕ', 'Oo': 'ඕ', 'OO': 'ඕ',
            'au': 'ඖ', 'Au': 'ඖ', 'ow': 'ඖ',
        }
        
        # Dependent vowel signs (පිළි)
        self.vowel_signs = {
            'a': '',  # inherent vowel
            'aa': 'ා', 'A': 'ා',
            'ae': 'ැ', 'Ae': 'ැ',
            'aae': 'ෑ', 'Aae': 'ෑ',
            'i': 'ි', 'I': 'ි',
            'ii': 'ී', 'Ii': 'ී', 'II': 'ී', 'ee': 'ී',
            'u': 'ු', 'U': 'ු',
            'uu': 'ූ', 'Uu': 'ූ', 'UU': 'ූ',
            'e': 'ෙ', 'E': 'ෙ',
            'ee': 'ේ', 'Ee': 'ේ', 'EE': 'ේ',
            'ai': 'ෛ', 'Ai': 'ෛ',
            'o': 'ො', 'O': 'ො',
            'oo': 'ෝ', 'Oo': 'ෝ', 'OO': 'ෝ',
            'au': 'ෞ', 'Au': 'ෞ', 'ow': 'ෞ',
        }
        
        # Special symbols
        self.special = {
            'Ng': 'ඟ',
            'nng': 'ඬ',
            'ndh': 'ඳ',
            'mb': 'ඹ',
            'Lu': 'ළ',
        }
        
        # Hal kirīma (්)
        self.hal_kirima = '්'
        
        # Rakaransaya (්‍ර)
        self.rakaransaya = '\u0dca\u200d\u0dbb'
        
        # Yansaya (්‍ය)
        self.yansaya = '\u0dca\u200d\u0dba'

        # Common word mappings (for frequently misspelled words)
        self.word_mappings = {
            'katha': 'කතා',
            'kathaa': 'කථා',
            'gatha': 'ගත',
            'mama': 'මම',
            'api': 'අපි',
            'eka': 'එක',
            'meka': 'මේක',
            'oya': 'ඔය',
            'eyaa': 'එයා',
            'mokada': 'මොකද',
            'kohomada': 'කොහොමද',
            'dumriya': 'දුම\u0dcaරිය',  # Exception: no Rakaransaya for දුම්රිය
        }
    
    def _convert_word(self, word):
        if not word:
            return word
        if word.lower() in self.word_mappings:
            return self.word_mappings[word.lower()]

        result = []
        i = 0
        
        while i < len(word):
            # Check for special multi-character sequences first
            matched = False
            
            # Try longest matches first (3 chars, 2 chars, 1 char)
            for length in [3, 2, 1]:
                if i + length <= len(word):
                    substring = word[i:i+length]
                    
                    # Check special symbols
                    if substring in self.special:
                        result.append(self.special[substring])
                        i += length
                        matched = True
                        break
                    
                    # Check consonant clusters (e.g., "kra", "ndu", "pra")
                    if length == 3:
                        cons_str = substring[:2]
                        vowel = substring[2]
                        
                        # Generate Rakaransaya dynamically for any consonant + r
                        if cons_str[1] == 'r' and cons_str[0] in self.consonants:
                            result.append(self.consonants[cons_str[0]])
                            result.append(self.rakaransaya)
                            if vowel in self.vowel_signs and vowel != 'a':
                                result.append(self.vowel_signs[vowel])
                            i += length
                            matched = True
                            break
                        
                        elif cons_str in self.consonants:
                            # Consonant with vowel
                            result.append(self.consonants[cons_str])
                            if vowel in self.vowel_signs:
                                result.append(self.vowel_signs[vowel])
                            else:
                                result.append(vowel)  # Keep as-is (English)
                            i += length
                            matched = True
                            break
                    
                    # Check consonant + vowel
                    if length == 2:
                        cons = substring[0]
                        vowel = substring[1]
                        
                        if cons in self.consonants:
                            result.append(self.consonants[cons])
                            
                            if vowel in self.vowel_signs:
                                result.append(self.vowel_signs[vowel])
                                i += length
                                matched = True
                                break
                    
                    # Check standalone vowel
                    if substring in self.vowels:
                        result.append(self.vowels[substring])
                        i += length
                        matched = True
                        break
                    
                    # Check standalone consonant
                    if substring in self.consonants:
                        result.append(self.consonants[substring])
                        i += length
                        matched = True
                        break
            
            if not matched:
                # No Sinhala match - keep character as-is (English, numbers, punctuation)
                result.append(word[i])
                i += 1
        
        return ''.join(result)

    def convert(self, text):
        """
        Convert Singlish text to Sinhala Unicode
        
        Args:
            text: Singlish text (can include English words)
        
        Returns:
            Sinhala Unicode text
        """
        if not text:
            return text
        
        words = []
        # Support basic word splitting to apply WORD_MAPPINGS
        current_word = []
        for char in text:
            if char.isspace() or not char.isalnum():
                if current_word:
                    words.append(self._convert_word(''.join(current_word)))
                    current_word = []
                words.append(char)
            else:
                current_word.append(char)
        if current_word:
            words.append(self._convert_word(''.join(current_word)))
            
        return ''.join(words)
    
    def is_sinhala_word(self, word):
        """Check if word contains Sinhala characters"""
        for char in word:
            if '\u0D80' <= char <= '\u0DFF':
                return True
        return False

# Global instance
_converter = SinhalaUnicodeConverter()

def convert_singlish_to_sinhala(text):
    """
    Convert Singlish to Sinhala Unicode
    Convenience function for external use
    """
    return _converter.convert(text)
