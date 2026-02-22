def classify_opportunity(text):
    """
    Simple AI/Rule-based classification for opportunity domains.
    In a real-world scenario, this could use a pre-trained NLP model.
    """
    text = text.lower()
    
    domains = {
        'AI': ['artificial intelligence', 'machine learning', 'deep learning', 'nlp', 'data science', 'neural networks', 'robotics', 'computer vision', 'big data'],
        'LAW': ['law', 'legal', 'justice', 'policy', 'human rights', 'court', 'litigation', 'jurisprudence', 'constitutional', 'advocacy'],
        'BIO': ['biomedical', 'biology', 'medicine', 'health', 'genetics', 'pharmaceutical', 'biotech', 'neuroscience', 'bioinformatics', 'clinical'],
        'ENG': ['engineering', 'mechanical', 'civil', 'chemical', 'aerospace', 'structural', 'nanotechnology', 'sustainable energy'],
        'ECE': ['electronics', 'communication', 'circuit', 'signal processing', 'microelectronics', 'hardware', 'semiconductor', 'wireless'],
    }
    
    for domain, keywords in domains.items():
        if any(keyword in text for keyword in keywords):
            return domain
            
    return 'OTHER'
