from wordcloud import WordCloud
import matplotlib.pyplot as plt

class WordCloudGenerator: 
    """
    Classe para gerar uma nuvem de palavras a partir de um dicionário de frequências.
    
    Attributes:
        width (int): Largura da imagem da nuvem de palavras. Padrão: 800.
        height (int): Altura da imagem da nuvem de palavras. Padrão: 400.
    """ 
    
    # Inicializa o gerador de nuvem de palavras com dimensões personalizáveis.
    def __init__(self, width=800, height=400): 
        self.width = width
        self.height = height
    
    def generate(self, word_frequencies: dict) -> WordCloud:
        """
        Gera uma nuvem de palavras a partir de um dicionário de frequências.

        Args:
            word_frequencies (dict): Dicionário onde as chaves são palavras e os valores são as frequências.

        Returns:
            WordCloud: Objeto da nuvem de palavras gerada.

        Exemplo:
            > word_freqeuncies = {'Python': 10, 'Programação': 8, 'Código': 5}
            > wc_generator = WordCloudGenerator()
            > wordcloud = wc_generator.generate(analyzer.word_frequencies)
        """
        wordcloud = WordCloud(
            width=self.width,
            height=self.height,
            background_color='white'
        ).generate_from_frequencies(word_frequencies)
        return wordcloud
    
    def show(self, word_frequencies: dict) -> None:
        """
        Gera e exibe a nuvem de palavras usando matplotlib.

        Args:
            word_frequencies (dict): Dicionário onde as chaves são palavras e os valores são as frequências.
        """
        wordcloud = self.generate(word_frequencies)
        plt.figure(figsize=(self.width / 100, self.height / 100))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()