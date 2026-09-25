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

### 4. Personalizando o Layout no LibreOffice Calc
Use o passo a passo abaixo para transformar a tabela importada em um layout financeiro limpo, moderno e legível.

#### Tema visual recomendado
| Elemento | Uso | Hex | RGB |
| --- | --- | --- | --- |
| Azul ardósia profundo | Fundo do cabeçalho | `#1F3A5F` | `31, 58, 95` |
| Ciano tecnológico | Destaques sutis, bordas de ênfase e seleção | `#2BB3C0` | `43, 179, 192` |
| Cinza neve | Linhas alternadas | `#F7F9FC` | `247, 249, 252` |
| Cinza de separação | Bordas finas da grade | `#D6DEE8` | `214, 222, 232` |
| Cinza do texto secundário | Valores auxiliares e divisões leves | `#5B6573` | `91, 101, 115` |

#### Tipografia e hierarquia
- **Fonte recomendada:** `Liberation Sans` (alta compatibilidade no LibreOffice Calc). Se preferir uma alternativa próxima, use `DejaVu Sans`.
- **Cabeçalho (`A1:F1`):** 11 pt, negrito, texto branco.
- **Linhas de dados (`A2:F11` ou até a última linha preenchida):** 10 pt, regular.
- **Altura visual sugerida:** cabeçalho com ~0,65 cm e linhas de dados com ~0,55 cm.

#### Formatação numérica por coluna
| Coluna | Conteúdo | Formato recomendado |
| --- | --- | --- |
| A (`Ativo`) | Nome do ativo | Texto |
| B (`Rentabilidade`) | Taxa anual | **Percentual** com 2 casas decimais (`0,00%`) |
| C (`Min_Moeda`) | Fração/unidade do ativo | **Número** com 4 a 6 casas decimais (`0,0000` ou `0,000000`) |
| D (`Cotacao_BRL`) | Cotação de mercado em BRL | **Moeda BRL** com 2 casas decimais (`R$ #.##0,00`) |
| E (`Minimo p/ Aportar`) | Custo local calculado | **Moeda BRL** com 2 casas decimais (`R$ #.##0,00`) |
| F (`Projecao 1 Ano`) | Saldo projetado por fórmula | **Moeda BRL** com 2 casas decimais (`R$ #.##0,00`) |

> **Observação:** a coluna **B** deve continuar armazenando a rentabilidade em formato decimal para que a fórmula `=E*(1+B)` funcione corretamente (ex.: `0,10` para representar `10,00%`).

#### Regras de alinhamento
- **Cabeçalho (`A1:F1`):** centralizado horizontal e verticalmente.
- **Coluna A (`Ativo`):** alinhamento à esquerda.
- **Colunas B a F:** alinhamento à direita para manter leitura financeira consistente.
- **Alinhamento vertical:** centralizado para toda a tabela.

#### Passo a passo exato no LibreOffice Calc
1. **Importe o CSV com fórmulas ativas**
   - Abra o arquivo `crypto_investments.csv`.
   - Na janela **Importação de Texto**, confirme o separador por vírgula e marque **Evaluate formulas / Avaliar fórmulas**.
   - Clique em **OK**.

2. **Ajuste a largura das colunas**
   - Selecione `A:F`.
   - Clique em **Formatar > Colunas > Largura Ideal...**
   - Defina uma margem adicional pequena (ex.: `0,20 cm`) e confirme em **OK**.

3. **Estilize o cabeçalho**
   - Selecione `A1:F1`.
   - Clique em **Formatar > Células...**
   - Aba **Fonte**: escolha `Liberation Sans`, **Negrito**, tamanho **11 pt**.
   - Aba **Efeitos de Fonte**: defina a cor da fonte como **Branco**.
   - Aba **Plano de Fundo**: aplique a cor `#1F3A5F` (`RGB 31,58,95`).
   - Aba **Alinhamento**: marque alinhamento **Horizontal: Centralizado** e **Vertical: Centralizado**.
   - Aba **Bordas**: aplique borda externa e interna fina com cor `#D6DEE8`.
   - Clique em **OK**.

4. **Remova o aspecto de grade pesada e substitua por bordas suaves**
   - Para a área da planilha, clique em **Exibir > Linhas de grade** e deixe desmarcado se quiser um visual mais limpo na tela.
   - Selecione `A1:F11` (ou toda a faixa preenchida).
   - Vá em **Formatar > Células... > Bordas**.
   - Escolha um modelo com linhas internas e externas finas.
   - Defina a cor da linha para `#D6DEE8` (`RGB 214,222,232`).
   - Clique em **OK**.

5. **Aplique tipografia e alinhamento aos dados**
   - Selecione `A2:F11` (ou até a última linha).
   - Acesse **Formatar > Células...**
   - Aba **Fonte**: `Liberation Sans`, tamanho **10 pt**.
   - Aba **Alinhamento**: defina **Vertical: Centralizado**.
   - Com `A2:A11` selecionado, use **Formatar > Células... > Alinhamento** e escolha **Horizontal: Esquerda**.
   - Com `B2:F11` selecionado, use **Formatar > Células... > Alinhamento** e escolha **Horizontal: Direita**.

6. **Crie a alternância de linhas**
   - Selecione `A2:F11`.
   - Clique em **Formatar > Formatação Condicional > Condição...**
   - Em **Condição 1**, escolha **A fórmula é**.
   - Use a fórmula `MOD(LIN();2)=0`.
   - Clique em **Novo estilo...**, dê o nome `Linha Par Financeira`.
   - Na criação do estilo, aplique **Plano de Fundo** com a cor `#F7F9FC` (`RGB 247,249,252`) e confirme em **OK**.
   - Confirme novamente em **OK** para aplicar a alternância nas linhas pares.

7. **Padronize os formatos numéricos**
   - **Rentabilidade (`B2:B11`)**:
     - Selecione a coluna `B`.
     - Clique em **Formatar > Células... > Números**.
     - Categoria **Percentual** e **2 casas decimais**.
   - **Min_Moeda (`C2:C11`)**:
     - Selecione a coluna `C`.
     - **Formatar > Células... > Números**.
     - Categoria **Número** com **4** ou **6 casas decimais**, conforme o nível de precisão desejado.
   - **Cotação e projeções (`D2:F11`)**:
     - Selecione `D:F`.
     - **Formatar > Células... > Números**.
     - Categoria **Moeda**.
     - Escolha o formato em **BRL / R$** com **2 casas decimais**.

8. **Destaque visual opcional nas colunas calculadas**
   - Selecione `E1:F11`.
   - Abra **Formatar > Células...**
   - Aba **Plano de Fundo**: escolha um branco levemente azulado ou mantenha branco puro.
   - Aba **Bordas**: aplique borda esquerda levemente mais destacada usando `#2BB3C0` (`RGB 43,179,192`) para separar os campos calculados dos dados de entrada.
   - Clique em **OK**.

9. **Melhore a navegação da tabela**
   - Em interfaces em português, use **Exibir > Congelar Células > Primeira Linha**; em interfaces em inglês, o caminho equivalente validado é **View > Freeze Cells > Freeze First Row**.
   - Se quiser desfazer depois, volte ao mesmo grupo de comandos de congelamento e escolha a opção de descongelar células.

10. **Salve o resultado formatado**
    - Para preservar a formatação, clique em **Arquivo > Salvar como...**
    - Salve uma cópia em **`.ods`**.
    - Mantenha o `.csv` como fonte de dados bruta e use o `.ods` como versão final personalizada.

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
