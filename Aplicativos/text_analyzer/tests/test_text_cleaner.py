import pytest
from text_analyzer.utils.text_cleaner import clean_text

@pytest.mark.parametrize("text, remove_stopwords, expected_words", [
    (
        "Estamos contratando um Desenvolvedor Python Pleno para atuar com APIs RESTful e Django. "
        "É essencial ter experiência com bancos de dados SQL e NoSQL, além de conhecimento em Docker e Git.",
        True,
        ["contratando", "desenvolvedor", "python", "pleno", "atuar", "apis", "restful",
         "django", "experiência", "bancos", "dados", "sql", "nosql", "conhecimento", "docker", "git"]
    ),
    (
        "Buscamos um Engenheiro de Dados com forte experiência em Python, Spark e AWS. "
        "A vaga é 100% remota e oferece ótimos benefícios!",
        True,
        ["buscamos", "engenheiro", "dados", "forte", "experiência", "python", "spark", "aws",
         "vaga", "100", "remota", "oferece", "ótimos", "benefícios"]
    ),
    (
        "Se você é um entusiasta de Machine Learning e IA, essa vaga pode ser para você! "
        "Trabalhe com modelos de aprendizado profundo utilizando TensorFlow e PyTorch.",
        True,
        ["entusiasta", "machine", "learning", "ia", "vaga", "trabalhe", "modelos",
         "aprendizado", "profundo", "tensorflow", "pytorch"]
    ),
    (
        "Venha fazer parte de nossa equipe de desenvolvimento Python! "
        "Aqui usamos FastAPI, Pandas e CI/CD para desenvolver soluções escaláveis.",
        True,
        ["venha", "parte", "equipe", "desenvolvimento", "python", "usamos",
         "fastapi", "pandas", "ci", "cd", "desenvolver", "soluções", "escaláveis"]
    ),
    (
        "Empresa líder no setor de tecnologia procura um Backend Developer Python. "
        "Requisitos: experiência com Flask, PostgreSQL e metodologias ágeis.",
        True,
        ["empresa", "líder", "setor", "tecnologia", "procura", "backend", "developer",
         "python", "requisitos", "experiência", "flask", "postgresql", "metodologias", "ágeis"]
    )
])
def test_clean_text(text, remove_stopwords, expected_words):
    result = clean_text(text, remove_stopwords=remove_stopwords)
    
    assert isinstance(result, list), "O resultado deve ser uma lista."
    assert set(expected_words).issubset(set(result)), f"Faltando palavras em {result}"
    