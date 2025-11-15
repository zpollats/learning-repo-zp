from collections import defaultdict
import string

class WordCounter:
    """Class to count words in a file"""

    STOPWORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been', 'have', 'has', 'had', 'this', 'that', 'it'
    }

    def __init__(self, filepath: str):
        self.filepath = filepath 
        try:
            with open(self.filepath, 'r') as f:
                self._lines = [line.strip() for line in f]
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.filepath}")

    def top_words(self, n: int = 10):
        """Returns the top n words in the file"""
        word_counts = defaultdict(int)

        for line in self._lines:
            # Remove puncuation and convert to lowecase for consistency
            cleaned = line.lower().translate(str.maketrans('', '', string.punctuation))
            words = cleaned.split()

            for word in words:
                if word and word not in self.STOPWORDS:
                    word_counts[word] += 1

        if not word_counts:
            return []
        
        return sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:n]

if __name__ == '__main__':
    word_counter = WordCounter('sample_file.txt')
    print(word_counter.top_words())