# exemplo_uso.py
from text_analyzer.core.analyzer import TextAnalyzer
from text_analyzer.visualizers.word_cloud import WordCloudGenerator
from text_analyzer.visualizers.frequency_charts import FrequencyVisualizer

def main():
    # Criar uma instância do analisador
    analyzer = TextAnalyzer()

    # Texto de exemplo
    texto_exemplo = """
    Python é uma linguagem de programação de alto nível, interpretada de script, 
    imperativa, orientada a objetos, funcional, de tipagem dinâmica e forte. 
    Python é uma linguagem muito popular hoje em dia. Python é usado em análise 
    de dados, inteligência artificial e desenvolvimento web.
    """

    # Carregar e analisar o texto
    analyzer.load_text(texto_exemplo)

    # Imprimir as 5 palavras mais frequentes
    print("Top 5 palavras mais frequentes:")
    sorted_words = sorted(analyzer.word_frequencies.items(), 
                         key=lambda x: x[1], 
                         reverse=True)
    for palavra, frequencia in sorted_words[:5]:
        print(f"- {palavra}: {frequencia} vezes")

    # Gerar e salvar nuvem de palavras
    wc_generator = WordCloudGenerator()
    wordcloud = wc_generator.generate(analyzer.word_frequencies)
    wordcloud.to_file('nuvem_palavras.png')

    # Criar e salvar gráfico de frequência
    viz = FrequencyVisualizer()
    plt = viz.create_bar_chart(analyzer.word_frequencies, top_n=8)
    plt.savefig('grafico_frequencia.png')
    plt.close()

if __name__ == "__main__":
    main()