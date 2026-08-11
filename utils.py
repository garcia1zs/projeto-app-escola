
import re
from datetime import date

def clean_cpf(value: str) -> str:
    return re.sub(r"\D", "", value or "")

def format_cpf(value: str) -> str:
    digits = clean_cpf(value)
    if len(digits) != 11:
        return value
    return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"

def valid_cpf_length(value: str) -> bool:
    return len(clean_cpf(value)) == 11

def money_br(value) -> str:
    try:
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return "R$ 0,00"

def person_data(row):
    p = row.get("pessoas") or {}
    return {
        "id": row.get("id"),
        "pessoa_id": row.get("pessoa_id"),
        "nome": p.get("nome", ""),
        "cpf": p.get("cpf", ""),
        "nascimento": p.get("nascimento"),
        "endereco": p.get("endereco", ""),
    }

def student_label(row):
    p = row.get("pessoas") or {}
    return f'{row.get("matricula", "—")} — {p.get("nome", "Sem nome")}'

def professor_label(row):
    p = row.get("pessoas") or {}
    return f'{p.get("nome", "Sem nome")} — {row.get("especialidade", "Sem especialidade")}'
