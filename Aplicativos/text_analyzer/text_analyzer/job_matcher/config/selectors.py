# job_matcher/config/selectors.py
SELECTORS = {
    "indeed.com": {
        "title": ".jobTitle span",
        "description": ".job-snippet",
        "company": ".companyName",
        "location": ".companyLocation"
    },
    "linkedin.com": {
        "title": "h1.top-card-layout__title",
        "description": "div.show-more-less-html__markup",
        "company": "a.topcard__org-name-link",
        "location": "span.topcard__flavor--bullet"
    },
    "gupy.io": {
        "title": "h1.sc-dkPtyc",  # Seletor para título da vaga
        "description": "div.sc-kOPcWc",  # Seletor para descrição
        "company": "span.sc-dtLLSn",  # Nome da empresa
        "location": "span.sc-bxivhb"  # Localização da vaga
    },
    "infojobs.com.br": {
        "title": "h1.job-title",  # Título da vaga
        "description": "div.job-description",  # Descrição da vaga
        "company": "a.company-name",  # Nome da empresa
        "location": "span.location"  # Localização
    }
}
