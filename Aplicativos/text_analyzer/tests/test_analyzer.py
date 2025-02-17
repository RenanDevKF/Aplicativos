import pytest
from text_analyzer.core.analyzer import TextAnalyzer

def test_load_text():
    analyzer = TextAnalyzer()
    
    texto = """
    Estamos em busca de um Desenvolvedor Python para integrar nossa equipe de tecnologia!  
    Se você é apaixonado por desenvolvimento de software e tem experiência com Python, essa vaga pode ser para você.  

    Requisitos:  
    - Experiência com Python e frameworks como Django ou Flask.  
    - Conhecimento em bancos de dados SQL e NoSQL.  
    - Experiência com APIs REST e integração de sistemas.  
    - Familiaridade com testes automatizados e boas práticas de desenvolvimento.  

    Diferenciais:  
    - Experiência com Cloud (AWS, GCP ou Azure).  
    - Conhecimento em Docker e Kubernetes.  
    - Vivência com metodologias ágeis como Scrum ou Kanban.  

    Benefícios:  
    - Trabalho remoto ou híbrido.  
    - Plano de carreira e incentivo a certificações.  
    - Ambiente colaborativo e inovador.  

    Venha fazer parte do nosso time e construir soluções escaláveis com Python!  
    """

    analyzer.load_text(texto)

    # Verifica se o texto foi armazenado corretamente
    assert analyzer.text == texto

    # Testa se algumas palavras-chave foram registradas corretamente
    assert "python" in analyzer.word_frequencies
    assert analyzer.word_frequencies["python"] >= 2  # Pode ser mais, dependendo da limpeza do texto
    assert "desenvolvedor" in analyzer.word_frequencies
    assert "vaga" in analyzer.word_frequencies
    assert "experiência" in analyzer.word_frequencies
