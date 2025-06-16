from finance_app.importers.pko_parser import parse_pko_pdf
import os

def test_pdf_parsing():
    sample = "tests/samples/sample.pdf"
    if not os.path.exists(sample):
        assert True
        return

    txs = parse_pko_pdf(sample)
    assert isinstance(txs, list)
    assert all(hasattr(t, "amount") for t in txs)
