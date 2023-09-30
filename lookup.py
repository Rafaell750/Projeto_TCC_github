def find_matches(chunks, keywords, padding=500):
    """
    Esta função encontra os melhores chunks de texto para responder à pergunta do usuário.

    Args:
        chunks (list): Lista de chunks de texto extraídos do arquivo PDF.
        keywords (list): Lista de palavras-chave extraídas da pergunta do usuário.
        padding (int): Número de caracteres a serem ignorados no início e no final de cada chunk.

    Returns:
        dict: Dicionário ordenado com os IDs dos chunks como chaves e a pontuação correspondente como valores.
    """

    df = {}  # Dicionário para armazenar a frequência do documento (df) de cada palavra-chave
    results = {}  # Dicionário para armazenar a pontuação de cada chunk

    # Crie uma versão em minúsculas de cada chunk, ignorando o padding no início e no final
    trimmed_chunks = []
    for i, chunk in enumerate(chunks):
        if i != 0:
            chunk = chunk[padding:]
        if i != len(chunks)-1:
            chunk = chunk[:-padding]
        trimmed_chunks.append(chunk.lower())

    # Calcule a df de cada palavra-chave
    for chunk in trimmed_chunks:
        for keyword in keywords:
            occurences = chunk.count(keyword)
            if keyword not in df:
                df[keyword] = 0
            df[keyword] += occurences

    # Calcule a pontuação de cada chunk
    for chunk_id, chunk in enumerate(trimmed_chunks):
        points = 0
        for keyword in keywords:
            occurences = chunk.count(keyword)
            if df[keyword] > 0:
                points += occurences / df[keyword]
        results[chunk_id] = points

    # Ordene os resultados por pontuação em ordem decrescente e retorne o dicionário ordenado
    return dict(sorted(results.items(), key=lambda item: item[1], reverse=True))