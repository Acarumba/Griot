import os
import streamlit as st
import google.generativeai as genai
from pathlib import Path

try:
    from groq import Groq
except ImportError:
    Groq = None

st.set_page_config(page_title="Griot", layout="wide")

# ---- CUSTOM COLORS & STYLING ----
st.markdown("""
<style>
:root {
    --bg: #070707;
    --panel: rgba(255,255,255,0.06);
    --panel-strong: rgba(255,255,255,0.08);
    --border: rgba(255,255,255,0.12);
    --text: #f8f8f8;
    --muted: #b0b0b0;
    --text-strong: #ffffff;
}

html, body, [data-testid="stAppViewContainer"] {
    background: #070707;
    color: var(--text);
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1080px;
}

h1, h2, h3 {
    color: var(--text-strong) !important;
    letter-spacing: -0.03em;
    margin: 0;
}

h1 {
    font-size: 3rem !important;
    font-weight: 700;
}

h2 {
    font-size: 1.85rem !important;
    font-weight: 600;
}

h3 {
    font-size: 1.05rem !important;
    font-weight: 600;
}

.stButton > button {
    background: #ffffff !important;
    color: #070707 !important;
    border: none !important;
    border-radius: 999px !important;
    padding: 0.75rem 1.4rem !important;
    font-weight: 700 !important;
    box-shadow: 0 18px 40px rgba(0,0,0,0.18) !important;
    transition: transform 0.16s ease, box-shadow 0.16s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 20px 48px rgba(0,0,0,0.22) !important;
}

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 18px 20px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.16);
}

.stAlert, .card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 20px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.16);
}

.hero-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 28px;
    padding: 34px;
    box-shadow: 0 22px 60px rgba(0,0,0,0.22);
}

.section-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 22px;
    margin-top: 12px;
}

.caption, .stCaptionContainer {
    color: var(--muted) !important;
}

.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background: rgba(255,255,255,0.05) !important;
    color: var(--text) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
}

.stTextInput>div>label, .stTextArea>div>label {
    color: var(--text) !important;
}

hr {
    border-color: rgba(255,255,255,0.08) !important;
}
</style>
""", unsafe_allow_html=True)

# ---- CONFIG ----
# Prefer the Groq key for this app so you avoid Gemini quota issues.
GEMINI_API_KEY = None
GROQ_API_KEY = None

try:
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
except Exception:
    GEMINI_API_KEY = None

try:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
except Exception:
    GROQ_API_KEY = None

GEMINI_API_KEY = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = GROQ_API_KEY or os.getenv("GROQ_API_KEY")

model = None
groq_client = None

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash-lite")

if GROQ_API_KEY and Groq is not None:
    groq_client = Groq(api_key=GROQ_API_KEY)

if not GEMINI_API_KEY and not GROQ_API_KEY:
    st.warning(
        "Set GEMINI_API_KEY or GROQ_API_KEY in Streamlit secrets or your environment before generating content."
    )
# ---- SCREEN 1: PROBLEM ----
st.markdown("""
<div class='hero-card'>
  <h1 style='text-align: center; margin-bottom: 0.3rem;'>Griot</h1>
  <p style='text-align: center; color: #f0c28e; font-size: 1.08rem; font-weight: 600; margin-bottom: 0;'>
    An intelligence layer built for African economic reality
  </p>
  <p style='text-align: center; color: #cfd8e3; line-height: 1.7; margin-top: 1rem; margin-bottom: 0;'>
    Generic AI models are calibrated to Western, formally-documented economies.
    When applied to African markets, they give confident answers built on data
    that misses most of what's actually happening on the ground.
  </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.metric("📊 Nigeria's informal economy", "58.2%", "of GDP")
with col2:
    st.metric("💰 Tax revenue-to-GDP ratio", "7%", "4th lowest globally")
st.caption("Source: NBS / Moniepoint report via TechCabal Insights, 2025")
st.divider()
# ---- SCREEN 2: DIVERGENCE MAP ----
st.markdown("<h2 style='margin-bottom: 0.2rem;'>The Divergence Map</h2>", unsafe_allow_html=True)
st.caption("Formal data source vs. ground-reality signal — shown side by side, not blended.")
formal_col, informal_col = st.columns(2)
with formal_col:
    st.markdown("""
    <div class='section-card'>
      <h3>📊 Formal Data Says</h3>
    </div>
    """, unsafe_allow_html=True)
    st.metric("Informal economy share", "58.2% of GDP")
    st.write("Official statistics are structured around the ~42% formal, taxed economy.")
    st.caption("Source: NBS / TC Insights, 2025")
with informal_col:
    st.markdown("""
    <div class='section-card'>
      <h3>🗣 Ground Reality Says</h3>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Qualitative signal, early founder/trader conversations")
    st.info('**FUTA entrepreneur:** "I feel like I\'m flying blind — some inner circle '
'knows everything and I\'m always steps behind. I\'d love if I had that kind of insight."')
    st.info('**Wholesaler, Akure Market:** *(I would love that type of product)*')
st.divider()
# ---- DIVERGENCE SYNTHESIS ----
DIVERGENCE_PROMPT = """In 3 sentences, explain why the gap between official Nigerian
economic data (58.2% of GDP is informal, only 7% tax-to-GDP ratio) and
ground-level trader/entrepreneur experience (feeling like an outsider lacking
market insight) matters for building AI tools for African businesses.
Do not resolve the gap into an average — explain why the gap itself is the
useful signal. Keep it concise and concrete."""

FALLBACK_SYNTHESIS = (
    "Official data says Nigeria's economy is 58.2% informal, yet formal systems are "
    "built around the 7% that pays tax — a structural blind spot, not a rounding error. "
    "The entrepreneur's 'flying blind' feeling is what that blind spot looks like from "
    "inside the market: real decisions get made on relational trust and local knowledge "
    "that formal data never captures. Griot doesn't average these two pictures into one "
    "number — it maps the gap between them, because the gap itself is the signal."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "local_context" not in st.session_state:
    st.session_state.local_context = """Local context for this app:
- Nigeria's informal economy is 58.2% of GDP.
- Tax revenue-to-GDP ratio is 7%.
- The app compares formal statistics with ground-reality signals from traders and entrepreneurs.
- Prefer practical, grounded answers over generic startup language."""

if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []


def build_system_prompt() -> str:
    return f"""You are Griot, a grounded AI assistant for African economic reality.

Strict instructions:
1. Use the provided local context and uploaded documents as a primary source of truth.
2. Prefer verified African datasets, official statistics, laws, regulations, policy documents, and local market reports.
3. Treat legal and regulatory context as first-class evidence for any compliance, policy, or market query.
4. Do not provide broad or generic "African" responses. If you do not know the exact country, region, or city, ask the user to specify their location first.
5. Always try to infer and confirm the user's location or jurisdiction before answering; use that location to ground your response.
6. If the local context is insufficient, say so clearly and ask for more detail.
7. Keep answers concise, structured, and directly tied to the user's query and available evidence.

Local context:
{st.session_state.local_context}"""


def ask_groq(prompt: str) -> str:
    if groq_client is None:
        raise RuntimeError("Groq client is not configured.")

    messages = [{"role": "system", "content": build_system_prompt()}]
    for message in st.session_state.messages:
        messages.append({"role": message["role"], "content": message["content"]})
    messages.append({"role": "user", "content": prompt})

    completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.2,
        max_tokens=500,
    )
    return completion.choices[0].message.content


def extract_text_from_upload(uploaded_file) -> str:
    if uploaded_file is None:
        return ""

    name = uploaded_file.name.lower()
    if name.endswith(".txt"):
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")
    if name.endswith(".md"):
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")
    if name.endswith(".csv"):
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")
    return ""

st.divider()
st.markdown("<h2>Ask Griot</h2>", unsafe_allow_html=True)
st.caption("This app routes queries to Groq first, with Gemini as a backup. Use the local context or the divergence analysis button for grounded answers.")

with st.expander("Local context / knowledge base", expanded=True):
    st.session_state.local_context = st.text_area(
        "Add local facts, notes, or data here",
        value=st.session_state.local_context,
        height=140,
    )

    uploaded_files = st.file_uploader(
        "Upload text or CSV files to ground the assistant",
        accept_multiple_files=True,
        type=["txt", "md", "csv"],
    )
    if uploaded_files:
        for uploaded_file in uploaded_files:
            text = extract_text_from_upload(uploaded_file)
            if text:
                st.session_state.uploaded_docs.append(
                    f"Document: {uploaded_file.name}\n\n{text[:4000]}"
                )
        st.session_state.local_context = (
            st.session_state.local_context
            + "\n\nUploaded documents:\n"
            + "\n\n---\n\n".join(st.session_state.uploaded_docs[-5:])
        )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.button("Generate divergence analysis"):
    with st.spinner("Analyzing divergence..."):
        try:
            response = ask_groq(DIVERGENCE_PROMPT)
            st.success(response)
        except Exception:
            st.success(FALLBACK_SYNTHESIS)

prompt = st.chat_input("Ask about the divergence map, local market reality, or your own notes...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if "africa" in prompt.lower() and not any(country in prompt.lower() for country in ["nigeria", "kenya", "south africa", "south-africa", "egypt", "ghana", "uganda", "tanzania", "morocco", "algeria", "senegal", "ethiopia"]):
                    reply = (
                        "To provide a grounded and locally accurate response, please specify the country, region, or city you mean. "
                        "Avoid broad Africa-wide generalizations."
                    )
                else:
                    reply = ask_groq(prompt)
            except Exception:
                reply = FALLBACK_SYNTHESIS
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

st.divider()
# ---- SCREEN 3: ROADMAP ----
st.markdown("<h2>Roadmap</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='section-card'>
  <ol style='color: #f5efe7; line-height: 1.8; margin: 0; padding-left: 1.2rem;'>
    <li><strong style='color: #f0c28e;'>Aggregation</strong> <em>(this demo — public formal data only)</em></li>
    <li><strong style='color: #f0c28e;'>Divergence mapping</strong> <em>across formal + informal sources</em></li>
    <li><strong style='color: #f0c28e;'>Mixture-of-Experts routing</strong> <em>calibrated to local context</em></li>
    <li><strong style='color: #f0c28e;'>Proprietary aggregated data base</strong></li>
  </ol>
  <p style='font-size: 0.95rem; color: #9aa6b2; margin-top: 0.9rem; margin-bottom: 0;'>
    <em>This MVP uses only publicly available formal sources. Production Griot layers in proprietary, continuously-aggregated informal signal at scale.</em>
  </p>
</div>
""", unsafe_allow_html=True)