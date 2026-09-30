import os
from typing import Tuple

from dotenv import load_dotenv

load_dotenv()

SYSTEM_INSTRUCTIONS = """
You are LegalEase, a careful legal-document drafting assistant.

Create a professional DRAFT legal document from the supplied user information.
Do not invent names, dates, amounts, addresses, obligations, laws, jurisdictions,
or facts that were not supplied. If important information is missing, use a
clear [TO BE COMPLETED] placeholder.

Return plain text only. Do not use Markdown tables or code fences.

Structure:
TITLE
Parties
Effective Date
Recitals / Purpose
Definitions (only if useful)
Main Clauses
Term and Termination
Confidentiality / Data Protection (when relevant)
Representations and Responsibilities
Dispute Resolution / Governing Law (only when supplied or clearly marked placeholder)
Signatures

Use numbered headings and readable paragraphs. Keep the document internally
consistent. This is a draft for review, not legal advice.
"""


class GeminiDocumentGenerator:
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
        self.client = None

        if self.api_key and self.api_key != "YOUR_API_KEY":
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                self.client = None

    @property
    def demo_mode(self) -> bool:
        return self.client is None

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
    ) -> Tuple[str, bool]:
        prompt = f"""
{SYSTEM_INSTRUCTIONS}

Document type:
{document_type}

Parties:
{parties}

Terms and conditions:
{terms}

Effective date / dates:
{dates}

Write the complete draft now.
"""

        if self.client is not None:
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )
                text = (getattr(response, "text", None) or "").strip()
                if text:
                    return text, False
                raise RuntimeError("Gemini returned an empty response.")
            except Exception as exc:
                raise RuntimeError(f"Gemini generation failed: {exc}") from exc

        return self._demo_document(document_type, parties, terms, dates), True

    @staticmethod
    def _demo_document(document_type: str, parties: str, terms: str, dates: str) -> str:
        clauses = [item.strip() for item in terms.split(";") if item.strip()]
        clause_text = "\n".join(
            f"{index}. {clause}" for index, clause in enumerate(clauses, start=1)
        )
        if not clause_text:
            clause_text = "1. [TO BE COMPLETED]"

        return f"""DRAFT {document_type.upper()}

IMPORTANT: DEMO MODE
This sample was generated because GEMINI_API_KEY is not configured.
Configure the API key for live Gemini generation.

1. PARTIES
{parties}

2. EFFECTIVE DATE
{dates}

3. PURPOSE
The parties intend to enter into this {document_type} on the effective date stated above.

4. TERMS AND CONDITIONS
{clause_text}

5. REVIEW
This is a draft template for demonstration and editing. Missing legal, commercial,
or jurisdiction-specific information should be completed and reviewed by a
qualified legal professional before use.

6. SIGNATURES

Party 1: ______________________________
Name: ________________________________
Date: _________________________________

Party 2: ______________________________
Name: ________________________________
Date: _________________________________
"""
