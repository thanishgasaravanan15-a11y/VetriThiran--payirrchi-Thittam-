from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from .schemas import DocumentRequest, DocumentResponse
from .services.ai_generator import GeminiDocumentGenerator
from .services.exporters import format_docx, format_pdf, format_txt

router = APIRouter()
generator = GeminiDocumentGenerator()


@router.post("/generate", response_model=DocumentResponse)
def generate_document(payload: DocumentRequest):
    try:
        content, demo_mode = generator.generate_document(
            payload.document_type,
            payload.parties,
            payload.terms,
            payload.dates,
        )
        return DocumentResponse(
            document_type=payload.document_type,
            content=content,
            demo_mode=demo_mode,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/export/txt")
def export_txt(payload: DocumentRequest):
    content, _ = generator.generate_document(
        payload.document_type, payload.parties, payload.terms, payload.dates
    )
    return Response(
        content=format_txt(content),
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=legalease.txt"},
    )


@router.post("/export/docx")
def export_docx(payload: DocumentRequest):
    content, _ = generator.generate_document(
        payload.document_type, payload.parties, payload.terms, payload.dates
    )
    return Response(
        content=format_docx(content, payload.document_type),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=legalease.docx"},
    )


@router.post("/export/pdf")
def export_pdf(payload: DocumentRequest):
    content, _ = generator.generate_document(
        payload.document_type, payload.parties, payload.terms, payload.dates
    )
    return Response(
        content=format_pdf(content, payload.document_type),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=legalease.pdf"},
    )
