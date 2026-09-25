#!/usr/bin/env python3
"""
tracker.py - Gerenciador seguro de requisições para a API CoinGecko.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3/simple/price"


class CoinGeckoTracker:
    def __init__(self, api_key: str = None, max_retries: int = 3):
        # Lê de argumento ou variável de ambiente COINGECKO_API_KEY
        self.api_key = api_key or os.getenv("COINGECKO_API_KEY", "").strip()
        self.max_retries = max_retries
        self.headers = {
            "User-Agent": "CryptoPortfolioTracker/2.0 (+https://github.com)",
            "Accept": "application/json",
        }
        # Utiliza o header oficial para contas Demo gratuitas
        if self.api_key:
            self.headers["x-cg-demo-api-key"] = self.api_key

    def fetch_prices_brl(self, coin_id_map: dict) -> dict:
        """
        Recebe um dicionário {Nome_Exibicao: coingecko_id} e retorna {Nome_Exibicao: preco_brl}.
        Faz requisição em lote com backoff exponencial para evitar bloqueios de 429.
        """
        prices = {name: 0.0 for name in coin_id_map.keys()}
        unique_ids = list(set(coin_id_map.values()))

        query_params = {
            "ids": ",".join(unique_ids),
            "vs_currencies": "brl",
        }
        url = f"{COINGECKO_BASE_URL}?{urllib.parse.urlencode(query_params)}"

        attempt = 0
        backoff_seconds = 2

        while attempt < self.max_retries:
            attempt += 1
            try:
                req = urllib.request.Request(url, headers=self.headers, method="GET")
                with urllib.request.urlopen(req, timeout=15) as resp:
                    if resp.status == 200:
                        payload = json.loads(resp.read().decode("utf-8"))
                        for name, cg_id in coin_id_map.items():
                            prices[name] = float(payload.get(cg_id, {}).get("brl", 0.0))
                        return prices

            except urllib.error.HTTPError as err:
                if err.code == 429:
                    print(
                        f"[tracker] Aviso: Limite de requisição atingido (429). Aguardando {backoff_seconds}s...",
                        file=sys.stderr,
                    )
                    time.sleep(backoff_seconds)
                    backoff_seconds *= 2
                elif err.code in (401, 403):
                    print(
                        f"[tracker] Erro de autenticação/permissão ({err.code}). Verifique sua chave de API.",
                        file=sys.stderr,
                    )
                    break
                else:
                    print(f"[tracker] Erro HTTP {err.code}: {err.reason}", file=sys.stderr)
                    break

            except (urllib.error.URLError, TimeoutError, ValueError) as err:
                print(f"[tracker] Falha de conexão na tentativa {attempt}: {err}", file=sys.stderr)
                time.sleep(backoff_seconds)
                backoff_seconds *= 2

        print("[tracker] Não foi possível obter cotações atualizadas. Preços mantidos em zero.", file=sys.stderr)
        return prices
