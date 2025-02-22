import os
import fitz  # PyMuPDF para leitura de PDFs
from text_analyzer.core.analyzer import TextAnalyzer
from text_analyzer.visualizers.word_cloud import WordCloudGenerator
from text_analyzer.visualizers.frequency_charts import FrequencyVisualizer
from text_analyzer.utils.file_handler import read_file
from text_analyzer.job_matcher.candidate_matcher import CandidateMatcher

def read_pdf(pdf_path):
    """Lê e extrai texto de um arquivo PDF."""
    try:
        texto = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                texto += page.get_text("text") + "\n"
        return texto.strip()
    except Exception as e:
        print(f"Erro ao ler PDF {pdf_path}: {str(e)}")
        return ""

def analisar_arquivo_unico(caminho_arquivo: str, nome_saida: str = None):
    """
    Analisa um único arquivo de texto ou PDF e compara com vagas de emprego.
    """
    analyzer = TextAnalyzer()
    wc_generator = WordCloudGenerator()
    viz = FrequencyVisualizer()
    nome_saida = nome_saida or os.path.splitext(os.path.basename(caminho_arquivo))[0]
    
    try:
        # Identifica formato e lê o arquivo
        if caminho_arquivo.endswith(".pdf"):
            texto = read_pdf(caminho_arquivo)
        else:
            texto = read_file(caminho_arquivo)
        
        if not texto:
            raise ValueError("O arquivo está vazio ou não pode ser lido.")
        
        analyzer.load_text(texto)
        print(f"\nAnálise do arquivo: {caminho_arquivo}")
        print(f"Total de palavras únicas: {len(analyzer.word_frequencies)}")

        sorted_words = sorted(analyzer.word_frequencies.items(), key=lambda x: x[1], reverse=True)
        print("\nPalavras mais frequentes:")
        for palavra, frequencia in sorted_words[:10]:
            print(f"- {palavra}: {frequencia} vezes")
        
        # Gerar visualizações
        wordcloud = wc_generator.generate(analyzer.word_frequencies)
        wordcloud.to_file(f'{nome_saida}_nuvem.png')

        plt = viz.create_bar_chart(analyzer.word_frequencies, top_n=10)
        plt.savefig(f'{nome_saida}_frequencia.png')
        plt.close()
        
        return analyzer.word_frequencies
    except Exception as e:
        print(f"Erro ao processar {caminho_arquivo}: {str(e)}")
        return None

def analisar_pasta(caminho_pasta: str, extensoes=['.txt', '.pdf']):
    """
    Analisa todos os arquivos de texto e PDF em uma pasta.
    """
    frequencias_totais = {}
    arquivos_processados = 0

    for arquivo in os.listdir(caminho_pasta):
        if any(arquivo.endswith(ext) for ext in extensoes):
            caminho_completo = os.path.join(caminho_pasta, arquivo)
            frequencias = analisar_arquivo_unico(caminho_completo)
            
            if frequencias:
                for palavra, freq in frequencias.items():
                    frequencias_totais[palavra] = frequencias_totais.get(palavra, 0) + freq
                arquivos_processados += 1

    if arquivos_processados > 0:
        print(f"\nAnálise consolidada de {arquivos_processados} arquivos:")
        wc_generator = WordCloudGenerator()
        viz = FrequencyVisualizer()

        wordcloud = wc_generator.generate(frequencias_totais)
        wordcloud.to_file('analise_consolidada_nuvem.png')

        plt = viz.create_bar_chart(frequencias_totais, top_n=15)
        plt.savefig('analise_consolidada_frequencia.png')
        plt.close()

def comparar_com_vagas(curriculo_path: str, urls_vagas: list):
    print(f"[DEBUG] Criando CandidateMatcher com currículo: {curriculo_path}")
    """
    Compara um currículo com múltiplas vagas e gera recomendações.
    """
    matcher = CandidateMatcher(curriculo_path)
    print("[DEBUG] CandidateMatcher criado! Classificando vagas...")
    
    resultados = matcher.classificar_vagas([{ 'id': i+1, 'titulo': f'Vaga {i+1}', 'url': url} for i, url in enumerate(urls_vagas)])
    print(f"[DEBUG] Resultados recebidos: {resultados}")
    
    for resultado in resultados:
        print(f"\nVaga: {resultado['titulo']}")
        print(f"Compatibilidade: {resultado['compatibilidade']:.2f}")
        print(f"Nível de Match: {resultado['nivel_match']}")
        print(f"Habilidades correspondentes: {', '.join(resultado['analise_detalhada'].get('habilidades_correspondentes', []))}")
        print(f"Recomendações: {resultado['analise_detalhada'].get('recomendacoes', [])}")
    
    return resultados

def main():
    print("Iniciando...")  # <- Adicionado para verificar se o script roda
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),))
    print(f"[DEBUG] BASE_DIR corrigido: {BASE_DIR}")

  # Diretório onde está o script
    curriculo_pdf = os.path.join(BASE_DIR, "test_files", "curriculo_test_ramiro.pdf")
    pasta_textos = os.path.join(BASE_DIR, "test_files")
    urls_vagas = [
    "https://www.infojobs.com.br/vaga-de-programador-desenvolvedor-back-end-ruby-full-stack-em-sao-paulo__10245359.aspx",
    "https://br.indeed.com/viewjob?jk=34b10817655112cc&from=shareddesktop",
    "https://www.linkedin.com/jobs/view/4158768068",
    "https://radixeng.gupy.io/job/eyJqb2JJZCI6Nzc4MzQwNiwic291cmNlIjoiZ3VweV9wb3J0YWwifQ==?jobBoardSource=share_link"
    ]
    
    print(f"[DEBUG] Verificando se {curriculo_pdf} existe...")
    if os.path.exists(curriculo_pdf):
        print(f"Arquivo encontrado: {curriculo_pdf}")
        analisar_arquivo_unico(curriculo_pdf)
        comparar_com_vagas(curriculo_pdf, urls_vagas)
    
    if os.path.exists(pasta_textos):
        print(f"Pasta encontrada: {pasta_textos}")
        analisar_pasta(pasta_textos, extensoes=['.txt', '.pdf'])

if __name__ == "__main__":
    main()
