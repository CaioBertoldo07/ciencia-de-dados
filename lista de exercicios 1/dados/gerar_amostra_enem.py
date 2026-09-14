"""
Gera uma amostra aleatória dos Microdados do ENEM 2024 (INEP).

O arquivo RESULTADOS_2024.csv tem cerca de 1,7 GB e mais de 4 milhões de linhas,
o que é grande demais para carregar inteiro com NumPy. Este script percorre o
arquivo linha a linha, direto de dentro do ZIP (sem descompactá-lo em disco), e
sorteia uma amostra aleatória simples de TAMANHO_AMOSTRA participantes usando
amostragem por reservatório (reservoir sampling). A semente fixa garante que a
mesma amostra seja gerada sempre que o script for executado.

Fonte: https://download.inep.gov.br/microdados/microdados_enem_2024.zip
Página: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem

Uso:
    python gerar_amostra_enem.py caminho/para/microdados_enem_2024.zip
"""

import csv
import io
import os
import random
import sys
import zipfile

TAMANHO_AMOSTRA = 20_000
SEMENTE = 2024

ARQUIVO_NO_ZIP = "microdados_enem_2024/DADOS/RESULTADOS_2024.csv"
ARQUIVO_SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "amostra_enem_2024.csv")

COLUNAS = [
    "NU_SEQUENCIAL",           # identificador do participante
    "SG_UF_PROVA",             # UF onde fez a prova
    "TP_DEPENDENCIA_ADM_ESC",  # 1 Federal, 2 Estadual, 3 Municipal, 4 Privada (vazio: sem escola informada)
    "TP_LOCALIZACAO_ESC",      # 1 Urbana, 2 Rural (vazio: sem escola informada)
    "TP_PRESENCA_CN",          # 0 Faltou, 1 Presente, 2 Eliminado
    "TP_PRESENCA_CH",
    "TP_PRESENCA_LC",
    "TP_PRESENCA_MT",
    "NU_NOTA_CN",              # Ciências da Natureza
    "NU_NOTA_CH",              # Ciências Humanas
    "NU_NOTA_LC",              # Linguagens e Códigos
    "NU_NOTA_MT",              # Matemática
    "TP_STATUS_REDACAO",
    "NU_NOTA_REDACAO",
]


def main(caminho_zip):
    gerador = random.Random(SEMENTE)
    amostra = []

    with zipfile.ZipFile(caminho_zip) as arquivo_zip:
        with arquivo_zip.open(ARQUIVO_NO_ZIP) as arquivo_binario:
            leitor = csv.DictReader(io.TextIOWrapper(arquivo_binario, encoding="latin-1"), delimiter=";")
            total_linhas = 0
            for linha in leitor:
                registro = [linha[coluna] for coluna in COLUNAS]
                if total_linhas < TAMANHO_AMOSTRA:
                    amostra.append(registro)
                else:
                    posicao = gerador.randint(0, total_linhas)
                    if posicao < TAMANHO_AMOSTRA:
                        amostra[posicao] = registro
                total_linhas += 1

    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8") as saida:
        escritor = csv.writer(saida, delimiter=";")
        escritor.writerow(COLUNAS)
        escritor.writerows(amostra)

    print(f"Linhas no arquivo original: {total_linhas:,}")
    print(f"Amostra salva em: {ARQUIVO_SAIDA} ({len(amostra):,} participantes)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
