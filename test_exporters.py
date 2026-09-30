from backend.services.exporters import (
    format_docx,
    format_pdf,
    format_txt,
    sanitize_text,
)


def test_sanitize_text():
    assert sanitize_text("hello\u2014world") == "hello-world"


def test_txt_export():
    result = format_txt("Test document")
    assert b"Test document" in result


def test_docx_export():
    result = format_docx("1. TERMS\nTest document", "Agreement")
    assert result[:2] == b"PK"


def test_pdf_export():
    result = format_pdf("1. TERMS\nTest document", "Agreement")
    assert result.startswith(b"%PDF")
