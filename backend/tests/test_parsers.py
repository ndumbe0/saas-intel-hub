from app.utils.parsers import clean_currency, clean_bigint, clean_decimal, parse_growth_tactics, normalize_text
from decimal import Decimal

def test_clean_currency_k():
    assert clean_currency('$24K') == Decimal('24000')
    assert clean_currency('$1.67M') == Decimal('1670000')

def test_clean_bigint():
    assert clean_bigint('30K') == 30000

def test_strange_values():
    from app.utils.parsers import clean_currency, clean_int
    assert clean_currency('—') is None
    assert clean_currency('N/A') is None

def test_normalize():
    assert normalize_text('Hello World') == 'hello world'
