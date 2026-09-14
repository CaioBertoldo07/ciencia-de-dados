"""
Gera um extrato da Série Histórica de Preços de Combustíveis da ANP.

A ANP publica, para cada mês, dois arquivos CSV com os preços coletados em
postos de todo o Brasil: um de gasolina e etanol e outro de diesel e GNV
(cerca de 11 MB por mês). Este script baixa os 24 arquivos mensais de
2024 e 2025 de cada tipo, mantém apenas:

- as coletas feitas nas 27 capitais;
- os produtos gasolina comum, etanol e diesel S10;
- as colunas usadas na análise;

e salva o resultado em precos_combustiveis_capitais_2024_2025.csv.

Fonte: https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis

Uso:
    python gerar_extrato_precos_anp.py
"""

import csv
import io
import os
import urllib.request

URL_BASE = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsan/{ano}/{arquivo}-{mes:02d}.csv"
ARQUIVOS = ["precos-gasolina-etanol", "precos-diesel-gnv"]
ANOS = [2024, 2025]
PRODUTOS = {"GASOLINA", "ETANOL", "DIESEL S10"}
ARQUIVO_SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "precos_combustiveis_capitais_2024_2025.csv")

# O site da ANP recusa requisições sem cabeçalhos de navegador
CABECALHOS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

CAPITAIS = {
    "AC": "RIO BRANCO", "AL": "MACEIO", "AM": "MANAUS", "AP": "MACAPA", "BA": "SALVADOR",
    "CE": "FORTALEZA", "DF": "BRASILIA", "ES": "VITORIA", "GO": "GOIANIA", "MA": "SAO LUIS",
    "MG": "BELO HORIZONTE", "MS": "CAMPO GRANDE", "MT": "CUIABA", "PA": "BELEM", "PB": "JOAO PESSOA",
    "PE": "RECIFE", "PI": "TERESINA", "PR": "CURITIBA", "RJ": "RIO DE JANEIRO", "RN": "NATAL",
    "RO": "PORTO VELHO", "RR": "BOA VISTA", "RS": "PORTO ALEGRE", "SC": "FLORIANOPOLIS", "SE": "ARACAJU",
    "SP": "SAO PAULO", "TO": "PALMAS",
}

COLUNAS_SAIDA = ["REGIAO", "UF", "MUNICIPIO", "PRODUTO", "DATA_COLETA", "VALOR_VENDA", "BANDEIRA"]


def sem_acentos(texto):
    trocas = str.maketrans("ÁÀÂÃÉÊÍÓÔÕÚÇ", "AAAAEEIOOOUC")
    return texto.upper().translate(trocas).strip()


def main():
    linhas_saida = []
    for ano in ANOS:
        for mes in range(1, 13):
            for arquivo in ARQUIVOS:
                url = URL_BASE.format(ano=ano, arquivo=arquivo, mes=mes)
                requisicao = urllib.request.Request(url, headers=CABECALHOS)
                with urllib.request.urlopen(requisicao, timeout=300) as resposta:
                    conteudo = resposta.read().decode("utf-8-sig")

                leitor = csv.DictReader(io.StringIO(conteudo), delimiter=";")
                mantidas = 0
                for linha in leitor:
                    uf = (linha["Estado - Sigla"] or "").strip()
                    municipio = sem_acentos(linha["Municipio"] or "")
                    produto = (linha["Produto"] or "").strip()
                    if produto in PRODUTOS and CAPITAIS.get(uf) == municipio:
                        linhas_saida.append([
                            linha["Regiao - Sigla"].strip(), uf, municipio, produto,
                            linha["Data da Coleta"].strip(), linha["Valor de Venda"].strip(),
                            (linha["Bandeira"] or "").strip(),
                        ])
                        mantidas += 1
                print(f"{ano}-{mes:02d} {arquivo}: {mantidas} coletas mantidas")

    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8") as saida:
        escritor = csv.writer(saida, delimiter=";")
        escritor.writerow(COLUNAS_SAIDA)
        escritor.writerows(linhas_saida)

    print(f"Extrato salvo em: {ARQUIVO_SAIDA} ({len(linhas_saida):,} coletas)")


if __name__ == "__main__":
    main()
