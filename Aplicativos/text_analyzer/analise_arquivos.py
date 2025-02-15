# analise_arquivos.py
import os
from text_analyzer.core.analyzer import TextAnalyzer
from text_analyzer.visualizers.word_cloud import WordCloudGenerator
from text_analyzer.visualizers.frequency_charts import FrequencyVisualizer
from text_analyzer.utils.file_handler import read_file

def analisar_arquivo_unico(caminho_arquivo: str, nome_saida: str = None):
    """
    Analisa um único arquivo de texto
    """
    # Criar instâncias das classes necessárias
    analyzer = TextAnalyzer()
    wc_generator = WordCloudGenerator()
    viz = FrequencyVisualizer()

    # Definir nome de saída se não fornecido
    if nome_saida is None:
        nome_saida = os.path.splitext(os.path.basename(caminho_arquivo))[0]

    try:
        # Ler e analisar o arquivo
        texto = read_file(caminho_arquivo)
        analyzer.load_text(texto)

        # Imprimir estatísticas básicas
        print(f"\nAnálise do arquivo: {caminho_arquivo}")
        print(f"Total de palavras únicas: {len(analyzer.word_frequencies)}")
        
        # Mostrar top 10 palavras
        print("\nPalavras mais frequentes:")
        sorted_words = sorted(analyzer.word_frequencies.items(), 
                            key=lambda x: x[1], 
                            reverse=True)
        for palavra, frequencia in sorted_words[:10]:
            print(f"- {palavra}: {frequencia} vezes")

        # Gerar visualizações
        # Nuvem de palavras
        wordcloud = wc_generator.generate(analyzer.word_frequencies)
        wordcloud.to_file(f'{nome_saida}_nuvem.png')

        # Gráfico de barras
        plt = viz.create_bar_chart(analyzer.word_frequencies, top_n=10)
        plt.savefig(f'{nome_saida}_frequencia.png')
        plt.close()

        return analyzer.word_frequencies

    except Exception as e:
        print(f"Erro ao processar {caminho_arquivo}: {str(e)}")
        return None

def analisar_pasta(caminho_pasta: str, extensoes=['.txt']):
    """
    Analisa todos os arquivos de texto em uma pasta
    """
    frequencias_totais = {}
    arquivos_processados = 0

    # Percorrer todos os arquivos na pasta
    for arquivo in os.listdir(caminho_pasta):
        if any(arquivo.endswith(ext) for ext in extensoes):
            caminho_completo = os.path.join(caminho_pasta, arquivo)
            frequencias = analisar_arquivo_unico(caminho_completo)
            
            if frequencias:
                # Combinar frequências
                for palavra, freq in frequencias.items():
                    frequencias_totais[palavra] = frequencias_totais.get(palavra, 0) + freq
                arquivos_processados += 1

    # Gerar análise consolidada se houver arquivos processados
    if arquivos_processados > 0:
        print(f"\nAnálise consolidada de {arquivos_processados} arquivos:")
        
        # Criar visualizações consolidadas
        wc_generator = WordCloudGenerator()
        viz = FrequencyVisualizer()

        # Nuvem de palavras consolidada
        wordcloud = wc_generator.generate(frequencias_totais)
        wordcloud.to_file('analise_consolidada_nuvem.png')

        # Gráfico de frequência consolidado
        plt = viz.create_bar_chart(frequencias_totais, top_n=15)
        plt.savefig('analise_consolidada_frequencia.png')
        plt.close()

def main():
    # Exemplo de uso para um único arquivo
    arquivo_unico = "caminho/para/seu/arquivo.txt"
    if os.path.exists(arquivo_unico):
        analisar_arquivo_unico(arquivo_unico)

    # Exemplo de uso para uma pasta
    pasta_textos = "caminho/para/sua/pasta"
    if os.path.exists(pasta_textos):
        analisar_pasta(pasta_textos, extensoes=['.txt', '.md'])

if __name__ == "__main__":
    main()