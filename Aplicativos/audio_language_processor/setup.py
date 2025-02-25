from setuptools import setup, find_packages

setup(
    name="audio_language_processor",
    version="0.1.0",
    author="Renan Kirchmaier Fayer",
    author_email="renan.devkf@gmail.com",
    description="Um processador de áudio para análise linguística e estudo de idiomas.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seuusuario/copyaudio_language_processor",  # Atualize com o repositório correto
    packages=find_packages(),
    install_requires=[
        "librosa",
        "pydub",
        "SpeechRecognition",
        "openai-whisper",  # Caso utilize
        "nltk",
        "spacy",
        "textblob",
        "matplotlib",
        "seaborn",
        "click",
        "argparse",
    ],
    entry_points={
        "console_scripts": [
            "copyaudio=cli:main",  # Assume que sua CLI tem uma função main()
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
