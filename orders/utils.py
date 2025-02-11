import re

def validate_card_number(card_number : str):
    pattern = r"^\d{4}-\d{4}-\d{4}-\d{4}$"
    return bool(re.match(pattern, card_number))

def validate_exp_date(exp_date: str):
    pattern = r"^(0[1-9]|1[0-2])/\d{4}$"
    return bool(re.match(pattern, exp_date))

def validate_cvc(cvc: str):
    pattern = r"^\d{3}$"
    return bool(re.match(pattern, cvc))