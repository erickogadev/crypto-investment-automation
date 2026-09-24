#!/usr/bin/env python3
"""
update_crypto_investments.py

Monthly updater for a crypto investments spreadsheet (crypto_investments.csv),
designed to be opened in LibreOffice Calc.

WHAT IT DOES EACH RUN
----------------------
1. Reads the CONTRIBUTIONS dict below (edit it every month with the new
   Min_Moeda amount you want to invest in each asset) and writes it into
   Column C.
2. Fetches the current price in BRL for every asset from the CoinGecko public
   API and writes it into Column D (Cotacao_BRL).
3. Preserves Column B (Rentabilidade) from the existing file if present,
   otherwise uses the DEFAULT_RENTABILIDADE below.
4. Writes Column E (Minimo p/ Aportar) and Column F (Projecao 1 Ano) as REAL
   spreadsheet formulas ("=C2*D2", "=E2*(1+B2)") instead of plain numbers, so
   LibreOffice recalculates them automatically whenever C, D or B change.

HOW TO USE
----------
1. Edit CONTRIBUTIONS below with this month's amounts (in coin units) before
   the 6th of the month.
2. Run manually with: python3 update_crypto_investments.py
3. Schedule automatically with cron (see SCHEDULING section at the bottom of
   this file / README notes) to run every month on the 6th day.

CRITICAL FORMATTING NOTE
-------------------------
Formula cells are written WITHOUT surrounding quotes and WITHOUT a leading
apostrophe. This has been verified against LibreOffice's CSV import: an
unquoted cell whose content starts with "=" is imported as a live formula
(type "f" internally), not as a text string. Do NOT wrap the formula strings
in quotes when editing this script, or LibreOffice will lock them as text.
"""

import csv
import json
import os
import sys
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# CONFIGURATION - edit this section every month
# ---------------------------------------------------------------------------

CSV_PATH = "/home/ghost/Documents/crypto_investments.csv"

# Order of assets in the spreadsheet (Column A).
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

# CoinGecko API ids used to fetch live prices (Column D, in BRL).
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

# >>> EDIT THIS EVERY MONTH <<<
# New Min_Moeda (Column C) contribution amount, in units of each coin, that
# you want to buy this month.
CONTRIBUTIONS = {
    "Tether": 10.0,         # Equivale a U$ 10.00 (Tether vale sempre 1 dólar)
    "USD Coin": 10.0,       # Equivale a U$ 10.00 (USDC vale sempre 1 dólar)
    "Ethereum": 0.0037,     # Equivale a U$ 10.00 em frações de Ether
    "Solana": 0.067,        # Equivale a U$ 10.00 em frações de Solana
    "Near": 2.22,           # Equivale a U$ 10.00 em moedas NEAR
    "Cardano": 14.28,       # Equivale a U$ 5.00 em moedas ADA (Cardano)
    "Chiliz": 100.0,        # Equivale a U$ 5.00 em moedas CHZ (Chiliz)
    "Avalanche": 0.21,      # Equivale a U$ 5.00 em frações de AVAX
    "Polkadot": 1.11,       # Equivale a U$ 5.00 em moedas DOT
    "Cosmos": 0.83,         # Equivale a U$ 5.00 em moedas ATOM (Cosmos)
}


# Used only when the CSV does not exist yet / an asset has no prior value.
# Expressed as a decimal (e.g. 0.12 = 12% a.a.). Existing values already in
# the CSV (Column B) are preserved automatically on every run.
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

COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids={ids}&vs_currencies=brl"
)


# ---------------------------------------------------------------------------
# CORE LOGIC
# ---------------------------------------------------------------------------

def fetch_prices_brl(asset_names):
    """Fetch current BRL price for each asset from CoinGecko. Returns a dict
    asset_name -> price (float). Falls back to 0.0 per-asset on failure so
    the script never crashes the whole run because of one bad lookup."""
    ids = ",".join(COINGECKO_IDS[name] for name in asset_names)
    url = COINGECKO_URL.format(ids=ids)
    prices = {name: 0.0 for name in asset_names}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "crypto-updater/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())
        for name in asset_names:
            cg_id = COINGECKO_IDS[name]
            prices[name] = float(data.get(cg_id, {}).get("brl", 0.0))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as exc:
        print(f"WARNING: failed to fetch live prices from CoinGecko: {exc}", file=sys.stderr)
        print("Existing/zero prices will be used instead.", file=sys.stderr)
    return prices


def read_existing_rentabilidade(path):
    """Read Column B (Rentabilidade) values for each asset already present in
    the CSV, so re-running the script never wipes out manual edits there."""
    existing = {}
    if not os.path.isfile(path):
        return existing
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return existing
    for row in rows[1:]:
        if len(row) < 2 or not row[0]:
            continue
        try:
            existing[row[0]] = float(row[1])
        except ValueError:
            continue
    return existing


def build_rows(assets, contributions, rentabilidade, prices):
    rows = []
    for i, asset in enumerate(assets):
        row_num = i + 2  # header is row 1
        b = rentabilidade.get(asset, DEFAULT_RENTABILIDADE.get(asset, 0.0))
        c = contributions.get(asset, 0)
        d = prices.get(asset, 0.0)
        e_formula = f"=C{row_num}*D{row_num}"
        f_formula = f"=E{row_num}*(1+B{row_num})"
        rows.append([asset, b, c, d, e_formula, f_formula])
    return rows


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    print(f"Updating {CSV_PATH} ...")

    existing_rentabilidade = read_existing_rentabilidade(CSV_PATH)
    merged_rentabilidade = dict(DEFAULT_RENTABILIDADE)
    merged_rentabilidade.update(existing_rentabilidade)

    prices = fetch_prices_brl(ASSETS)

    rows = build_rows(ASSETS, CONTRIBUTIONS, merged_rentabilidade, prices)
    write_csv(CSV_PATH, HEADER, rows)

    print("Done. Column C updated from CONTRIBUTIONS, Column D refreshed from")
    print("CoinGecko, Columns E/F written as live formulas (=C*D, =E*(1+B)).")


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# SCHEDULING (run automatically on the 6th of every month)
# ---------------------------------------------------------------------------
# Install with:
#   (crontab -l 2>/dev/null; echo "0 9 6 * * /usr/bin/python3 /home/ghost/Documents/update_crypto_investments.py >> /home/ghost/Documents/update_crypto_investments.log 2>&1") | crontab -
#
# This runs at 09:00 on day 6 of every month. Verify with: crontab -l
