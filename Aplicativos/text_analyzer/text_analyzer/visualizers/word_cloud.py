from wordcloud import WordCloud
import matplotlib.pyplot as plt

class WordCloudGenerator: 
    def __init__(self, width=800, height=400): 
        self.width = width
        self.height = height
    
    def generate(self, word_frequencies: dict) -> WordCloud:
        """Gera uma nuvem de palavras a partir das frequências"""
        wordcloud = WordCloud(
            width=self.width,
            height=self.height,
            background_color='white'
        ).generate_from_frequencies(word_frequencies)
        return wordcloud