#!/usr/bin/env python3
"""
main.py - Orquestrador de aportes mensais e geração de planilha CSV.
"""

import csv
import os
from tracker import CoinGeckoTracker

CSV_PATH = os.path.expanduser("~/Documents/crypto_investments.csv")

ASSETS = [
    "Tether",
    "USD Coin",
    "Ethereum",
    "Solana",
    "Near",
    "Cardano",
    "Chiliz",
    "Avalanche",
    "Polkadot",
    "Cosmos",
]

COINGECKO_IDS = {
    "Tether": "tether",
    "USD Coin": "usd-coin",
    "Ethereum": "ethereum",
    "Solana": "solana",
    "Near": "near",
    "Cardano": "cardano",
    "Chiliz": "chiliz",
    "Avalanche": "avalanche-2",
    "Polkadot": "polkadot",
    "Cosmos": "cosmos",
}

# Aportes mensais (quantidades de moedas)
CONTRIBUTIONS = {
    "Tether": 10.0,
    "USD Coin": 10.0,
    "Ethereum": 0.0037,
    "Solana": 0.067,
    "Near": 2.22,
    "Cardano": 14.28,
    "Chiliz": 100.0,
    "Avalanche": 0.21,
    "Polkadot": 1.11,
    "Cosmos": 0.83,
}

DEFAULT_RENTABILIDADE = {
    "Tether": 0.0,
    "USD Coin": 0.0,
    "Ethereum": 0.10,
    "Solana": 0.0,
    "Near": 0.0,
    "Cardano": 0.0,
    "Chiliz": 0.0,
    "Avalanche": 0.0,
    "Polkadot": 0.0,
    "Cosmos": 0.0,
}

HEADER = [
    "Ativo",
    "Rentabilidade",
    "Min_Moeda",
    "Cotacao_BRL",
    "Minimo p/ Aportar",
    "Projecao 1 Ano",
]


def read_existing_rentabilidade(path: str) -> dict:
    existing = {}
    if not os.path.isfile(path):
        return existing
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return existing
    for row in rows[1:]:
        if len(row) >= 2 and row[0]:
            try:
                existing[row[0]] = float(row[1])
            except ValueError:
                continue
    return existing


def build_rows(assets, contributions, rentabilidade, prices):
    rows = []
    for i, asset in enumerate(assets):
        row_num = i + 2  # Cabeçalho na linha 1
        b = rentabilidade.get(asset, DEFAULT_RENTABILIDADE.get(asset, 0.0))
        c = contributions.get(asset, 0)
        d = prices.get(asset, 0.0)
        e_formula = f"=C{row_num}*D{row_num}"
        f_formula = f"=E{row_num}*(1+B{row_num})"
        rows.append([asset, b, c, d, e_formula, f_formula])
    return rows


def write_csv(path: str, header: list, rows: list):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    print(f"Atualizando {CSV_PATH} ...")

    # 1. Carrega dados pré-existentes
    existing_rentabilidade = read_existing_rentabilidade(CSV_PATH)
    merged_rentabilidade = dict(DEFAULT_RENTABILIDADE)
    merged_rentabilidade.update(existing_rentabilidade)

    # 2. Executa a requisição protegida pelo tracker
    tracker = CoinGeckoTracker()
    prices = tracker.fetch_prices_brl(COINGECKO_IDS)

    # 3. Monta e grava o CSV
    rows = build_rows(ASSETS, CONTRIBUTIONS, merged_rentabilidade, prices)
    write_csv(CSV_PATH, HEADER, rows)

    print("Planilha atualizada com sucesso.")


if __name__ == "__main__":
    main()
