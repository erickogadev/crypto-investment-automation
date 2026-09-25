#!/usr/bin/env python3
"""
style_crypto_investments.py

Applies the "deep slate / teal" financial styling template to the crypto
investments table and saves it as a LibreOffice Calc-ready .xlsx workbook
with fully live formulas (Column E/F), proper number formats, alternating
row tints, borders and alignment.

Usage:
    python3 style_crypto_investments.py <input.csv> <output.xlsx>
"""

import csv
import sys

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

# ---------------------------------------------------------------------------
# Palette / template constants
# ---------------------------------------------------------------------------
HEADER_BG = "1E2A38"       # deep slate
HEADER_FG = "FFFFFF"       # white
ACCENT = "2DD4BF"          # teal accent (header bottom border)
ALT_ROW_BG = "F4F6F8"      # ultra-light gray/off-white
GRID_COLOR = "D9DEE3"      # muted light gray borders

FONT_NAME = "Calibri"      # modern, bundled with LibreOffice
HEADER_SIZE = 11
DATA_SIZE = 10

HEADERS = [
    "Ativo",
    "Rentabilidade",
    "Min_Moeda",
    "Cotacao_BRL",
    "Minimo p/ Aportar",
    "Projecao 1 Ano",
]

# Number format codes per column (1-indexed, matching HEADERS order)
NUMBER_FORMATS = {
    2: "0.00%",                      # Rentabilidade
    3: "0.0000",                     # Min_Moeda (crypto units, 4 decimals)
    4: '[$R$-416] #,##0.00',         # Cotacao_BRL
    5: '[$R$-416] #,##0.00',         # Minimo p/ Aportar
    6: '[$R$-416] #,##0.00',         # Projecao 1 Ano
}


def load_rows(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    return rows[1:]  # skip header, we re-write our own


def build_workbook(data_rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "Crypto Investments"

    thin_side = Side(style="thin", color=GRID_COLOR)
    thin_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
    accent_bottom_border = Border(
        left=thin_side, right=thin_side, top=thin_side,
        bottom=Side(style="medium", color=ACCENT),
    )

    header_font = Font(name=FONT_NAME, size=HEADER_SIZE, bold=True, color=HEADER_FG)
    header_fill = PatternFill(fill_type="solid", fgColor=HEADER_BG)
    header_align = Alignment(horizontal="center", vertical="center")

    data_font = Font(name=FONT_NAME, size=DATA_SIZE)
    alt_fill = PatternFill(fill_type="solid", fgColor=ALT_ROW_BG)
    left_align = Alignment(horizontal="left", vertical="center")
    right_align = Alignment(horizontal="right", vertical="center")

    # --- Header row ---
    for col_idx, header in enumerate(HEADERS, start=1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align
        cell.border = accent_bottom_border

    # --- Data rows ---
    for r_offset, row in enumerate(data_rows, start=0):
        row_num = r_offset + 2
        asset, rentabilidade, min_moeda, cotacao, _e_formula, _f_formula = row

        values = [
            asset,
            float(rentabilidade),
            float(min_moeda),
            float(cotacao),
            f"=C{row_num}*D{row_num}",
            f"=E{row_num}*(1+B{row_num})",
        ]

        for col_idx, value in enumerate(values, start=1):
            cell = ws.cell(row=row_num, column=col_idx, value=value)
            cell.font = data_font
            cell.border = thin_border
            cell.alignment = left_align if col_idx == 1 else right_align
            if col_idx in NUMBER_FORMATS:
                cell.number_format = NUMBER_FORMATS[col_idx]

    last_row = len(data_rows) + 1
    last_col_letter = get_column_letter(len(HEADERS))
    data_range = f"A2:{last_col_letter}{last_row}"

    # --- Alternating row tint via conditional formatting (MOD(ROW(),2)=0) ---
    ws.conditional_formatting.add(
        data_range,
        FormulaRule(formula=["MOD(ROW(),2)=0"], fill=alt_fill),
    )

    # --- Column widths ---
    widths = [16, 14, 13, 14, 18, 16]
    for col_idx, width in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    # --- Freeze header row ---
    ws.freeze_panes = "A2"

    # Hide default gridlines for a cleaner canvas (borders above replace them)
    ws.sheet_view.showGridLines = False

    return wb


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 style_crypto_investments.py <input.csv> <output.xlsx>")
        sys.exit(1)

    csv_path, xlsx_path = sys.argv[1], sys.argv[2]
    data_rows = load_rows(csv_path)
    wb = build_workbook(data_rows)
    wb.save(xlsx_path)
    print(f"Styled workbook saved to {xlsx_path}")


if __name__ == "__main__":
    main()
