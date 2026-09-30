import html
import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
    }
    .subtitle {
        text-align: center;
        color: #8b93a7;
        margin-bottom: 1.5rem;
    }
    .preview {
        background: #111827;
        color: #f3f4f6;
        padding: 1.3rem;
        border-radius: 14px;
        border: 1px solid #273244;
        max-height: 620px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-family: Georgia, serif;
        line-height: 1.65;
    }
    .warning {
        padding: .75rem 1rem;
        border-radius: 10px;
        background: #3a2e13;
        color: #ffe8a3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-Powered Legal Document Generator</div>',
    unsafe_allow_html=True,
)

if "document" not in st.session_state:
    st.session_state.document = ""

if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False

with st.sidebar:
    st.header("Document details")
    document_type = st.selectbox(
        "Document type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement",
            "Lease Agreement",
            "Freelance Work Contract",
            "Service Agreement",
            "Employment Offer Letter",
            "General Agreement",
            "Custom Legal Document",
        ],
    )
    parties = st.text_area(
        "Parties involved",
        placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",
        height=120,
    )
    terms = st.text_area(
        "Terms & conditions",
        placeholder=(
            "Payment to be made within 30 days; "
            "Confidentiality must be maintained; "
            "Either party may terminate with 15 days notice"
        ),
        height=180,
        help="Separate clauses with semicolons.",
    )
    dates = st.text_input(
        "Effective date",
        placeholder="September 27, 2026",
    )

    logo = st.file_uploader(
        "Optional logo",
        type=["png", "jpg", "jpeg"],
    )

    generate = st.button(
        "Generate Document",
        type="primary",
        use_container_width=True,
    )

if generate:
    if not parties.strip() or not terms.strip() or not dates.strip():
        st.error("Please complete parties, terms, and effective date.")
    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates,
        }
        try:
            with st.spinner("Generating document..."):
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120,
                )
            if response.ok:
                data = response.json()
                st.session_state.document = data["content"]
                st.session_state.demo_mode = data.get("demo_mode", False)
                st.success("Document generated.")
            else:
                detail = response.json().get("detail", response.text)
                st.error(f"Backend error: {detail}")
        except requests.RequestException as exc:
            st.error(
                "Could not connect to FastAPI. Start the backend first. "
                f"Details: {exc}"
            )

if st.session_state.demo_mode:
    st.markdown(
        '<div class="warning">Demo mode is active. Add GEMINI_API_KEY to .env '
        "and restart the backend for live Gemini generation.</div>",
        unsafe_allow_html=True,
    )

left, right = st.columns([1, 1])

with left:
    st.subheader("Editable document")
    edited = st.text_area(
        "Edit the generated text",
        value=st.session_state.document,
        height=600,
        label_visibility="collapsed",
    )
    if edited != st.session_state.document:
        st.session_state.document = edited

with right:
    st.subheader("Preview")
    if st.session_state.document:
        safe = html.escape(st.session_state.document)
        st.markdown(
            f'<div class="preview">{safe}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("Generate a document to see the preview.")

if st.session_state.document:
    st.divider()
    st.subheader("Download")

    txt_bytes = (st.session_state.document + "\n").encode("utf-8")

    # Build DOCX/PDF locally so edits made in the Streamlit editor are preserved.
    from backend.services.exporters import format_docx, format_pdf

    logo_path = None
    if logo is not None:
        temp_logo = Path(".legalease_uploaded_logo")
        temp_logo.write_bytes(logo.getvalue())
        logo_path = str(temp_logo)

    docx_bytes = format_docx(
        st.session_state.document,
        document_type,
        logo_path,
    )
    pdf_bytes = format_pdf(
        st.session_state.document,
        document_type,
        logo_path,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button(
            "Download TXT",
            data=txt_bytes,
            file_name="legalease_document.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with c2:
        st.download_button(
            "Download DOCX",
            data=docx_bytes,
            file_name="legalease_document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    with c3:
        st.download_button(
            "Download PDF",
            data=pdf_bytes,
            file_name="legalease_document.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

st.caption(
    "LegalEase creates drafts for review. It does not replace advice from a qualified lawyer."
)
