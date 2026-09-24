markdown# Crypto Investment Automation 🚀

Este repositório contém um script em Python desenvolvido para automatizar a manutenção e atualização de uma planilha de aportes diários de criptomoedas (`.csv`) no Linux. O script é integrado com o **LibreOffice Calc** e atualiza as cotações de mercado em tempo real.

## 🛠️ O que o Script Faz
1. **Atualização de Aportes (Coluna C):** Aplica a quantidade exata de frações/unidades de criptomoedas definidas para o mês atual na coluna `Min_Moeda`.
2. **Cotação em Tempo Real (Coluna D):** Consome a API pública do **CoinGecko** para buscar o preço atualizado de cada ativo diretamente em Reais (BRL).
3. **Preservação de Dados (Coluna B):** Mantém intactos os valores de `Rentabilidade` inseridos manualmente no arquivo.
4. **Fórmulas Dinâmicas (Colunas E e F):** Escreve fórmulas reais (`=C2*D2` e `=E2*(1+B2)`) compatíveis com o LibreOffice Calc, evitando erros de células travadas como texto.

---

## 📋 Estrutura da Planilha
O arquivo gerado é o `crypto_investments.csv` com as seguintes colunas:
* **A (Ativo):** Nome da Criptomoeda.
* **B (Rentabilidade):** Rendimento/Lucro (definido pelo usuário ou padrão).
* **C (Min_Moeda):** Quantidade da moeda a ser aportada (configurada no script).
* **D (Cotacao_BRL):** Preço atualizado do ativo em Reais via API.
* **E (Mínimo p/ Aportar):** Cálculo automático do valor total do aporte em Reais (`=C*D`).
* **F (Projeção 1 Ano):** Estimativa do valor futuro baseado na rentabilidade anual (`=E*(1+B)`).

---

## 🚀 Como Usar

### 1. Configurando Seus Aportes Mensais
Abra o arquivo `update_crypto_investments.py` e altere o dicionário `CONTRIBUTIONS` com a quantidade de moedas (frações) correspondentes ao seu plano de investimento em dólar ou valor nominal:

```python
CONTRIBUTIONS = {
    "Tether": 10.0,
    "USD Coin": 10.0,
    "Ethereum": 0.0037,
    "Solana": 0.067,
    # ... adicione as demais moedas
}
```

### 2. Execução Manual
Para testar ou rodar o script manualmente, execute o comando abaixo no terminal Linux:
```bash
python3 update_crypto_investments.py
```

### 3. Abrindo no LibreOffice Calc
Ao abrir o arquivo `.csv` gerado, certifique-se de marcar a opção **`Evaluate formulas`** (Avaliar fórmulas) na janela de importação de texto do LibreOffice para habilitar os cálculos automáticos.

---

## ⏰ Agendamento Automático (Cron)
Para que o script rode de forma totalmente autônoma todo **dia 6 de cada mês às 09:00**, adicione a seguinte linha ao seu agendador do Linux (`crontab -e`):

```text
0 9 6 * * /usr/bin/python3 /home/ghost/Documents/update_crypto_investments.py >> /home/ghost/Documents/update_crypto_investments.log 2>&1
```
*Os logs de sucesso ou erro serão gerados automaticamente no arquivo `.log` especificado.*

---
## 📦 Tecnologias Utilizadas
* **Python 3** (Bibliotecas nativas: `urllib`, `json`, `csv`, `os`)
* **CoinGecko API v3** (Busca de preços sem necessidade de chave de API)
* **Cron** (Agendamento do Linux)

---
© 2026 Eric Douglas Koga. Todos os direitos reservados.
Este código é de propriedade privada. Nenhuma parte deste projeto pode ser copiada, distribuída ou modificada sem autorização expressa do autor.
