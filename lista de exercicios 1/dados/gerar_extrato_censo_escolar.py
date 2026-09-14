"""
Extrai as escolas do Amazonas dos Microdados do Censo Escolar 2024 (INEP).

O arquivo microdados_ed_basica_2024.csv tem uma linha por escola do Brasil
(cerca de 218 MB e 426 colunas). Este script lê o CSV diretamente de dentro do
ZIP, mantém apenas as escolas do Amazonas (SG_UF = AM) e as colunas usadas na
análise, e salva o resultado em censo_escolar_2024_am.csv.

Fonte: https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2024.zip
Página: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar

Uso:
    python gerar_extrato_censo_escolar.py caminho/para/microdados_censo_escolar_2024.zip
"""

import csv
import io
import os
import sys
import zipfile

ARQUIVO_NO_ZIP = "microdados_censo_escolar_2024_defeso/dados/microdados_ed_basica_2024.csv"
ARQUIVO_SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "censo_escolar_2024_am.csv")

COLUNAS = [
    "CO_ENTIDADE",                  # código da escola
    "NO_MUNICIPIO",                 # município
    "TP_DEPENDENCIA",               # 1 Federal, 2 Estadual, 3 Municipal, 4 Privada
    "TP_LOCALIZACAO",               # 1 Urbana, 2 Rural
    "TP_LOCALIZACAO_DIFERENCIADA",  # 0 Não se aplica, 1 Área de assentamento, 2 Terra indígena, 3 Comunidade quilombola, 8 Comunidade tradicional
    "TP_SITUACAO_FUNCIONAMENTO",    # 1 Em atividade, 2 Paralisada, 3 Extinta, 4 Extinta no ano anterior
    "QT_MAT_BAS",                   # matrículas na educação básica
    "QT_DOC_BAS",                   # docentes na educação básica
    "QT_TUR_BAS",                   # turmas na educação básica
    "QT_SALAS_UTILIZADAS",          # salas de aula utilizadas
    "IN_INTERNET",                  # possui internet (0/1)
    "IN_BIBLIOTECA",                # possui biblioteca (0/1)
    "IN_AGUA_POTAVEL",              # fornece água potável (0/1)
    "IN_ENERGIA_INEXISTENTE",       # não possui energia elétrica (0/1)
]


def main(caminho_zip):
    total = 0
    escolas_am = []

    with zipfile.ZipFile(caminho_zip) as arquivo_zip:
        with arquivo_zip.open(ARQUIVO_NO_ZIP) as arquivo_binario:
            leitor = csv.DictReader(io.TextIOWrapper(arquivo_binario, encoding="latin-1"), delimiter=";")
            for linha in leitor:
                total += 1
                if linha["SG_UF"] == "AM":
                    escolas_am.append([linha[coluna] for coluna in COLUNAS])

    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8") as saida:
        escritor = csv.writer(saida, delimiter=";")
        escritor.writerow(COLUNAS)
        escritor.writerows(escolas_am)

    print(f"Escolas no arquivo original: {total:,}")
    print(f"Escolas do Amazonas salvas em: {ARQUIVO_SAIDA} ({len(escolas_am):,} escolas)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
