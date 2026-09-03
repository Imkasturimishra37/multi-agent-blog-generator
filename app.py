import streamlit as st

from graph.workflow import graph

from rag.pdf_loader import load_pdf
from rag.vector_store import create_vector_store
from rag.retriever import retrieve_context

from database.database import (
    create_database,
    save_blog,
    get_history
)

# ----------------------------------------
# PAGE CONFIG
# ----------------------------------------

st.set_page_config(
    page_title="Multi-Agent Blog Generator",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------------------
# CUSTOM CSS
# ----------------------------------------

st.markdown("""
<style>

/* ===========================================
   FONT IMPORT
=========================================== */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ===========================================
   GLOBAL
=========================================== */

html, body, [class*="css"]{

    font-family: "Inter", "Segoe UI", sans-serif;

    color:#F1F5F9;
}

/* ===========================================
   APP BACKGROUND
=========================================== */

.stApp{

    background:
    radial-gradient(circle at 15% 0%, rgba(56,189,248,0.10) 0%, transparent 45%),
    radial-gradient(circle at 85% 100%, rgba(34,197,94,0.08) 0%, transparent 45%),
    linear-gradient(
        160deg,
        #0B1120 0%,
        #0F172A 45%,
        #111827 100%
    );

    color:#F1F5F9;
}

/* ===========================================
   MAIN CONTAINER
=========================================== */

.block-container{

    padding-top:2.2rem;

    padding-bottom:3rem;

    max-width:1200px;
}

/* ===========================================
   TITLE
=========================================== */

.main-title{

    text-align:center;

    font-size:44px;

    font-weight:800;

    color:#FFFFFF;

    letter-spacing:.5px;

    line-height:1.2;
}

.sub-title{

    text-align:center;

    color:#94A3B8;

    font-size:17px;

    font-weight:500;

    margin-top:6px;

    margin-bottom:38px;
}

.header-badge{

    display:flex;

    justify-content:center;

    margin-bottom:14px;
}

.header-badge span{

    background:linear-gradient(90deg,#0284C7,#38BDF8);

    color:white;

    font-size:12.5px;

    font-weight:700;

    letter-spacing:.6px;

    padding:6px 16px;

    border-radius:999px;

    text-transform:uppercase;

    box-shadow:0 6px 18px rgba(56,189,248,.35);
}

/* ===========================================
   CARD
=========================================== */

.card{

    background:linear-gradient(180deg,#141E33 0%,#111827 100%);

    border:1px solid #263449;

    border-radius:18px;

    padding:26px 28px;

    margin-bottom:22px;

    box-shadow:
    0 12px 28px rgba(0,0,0,.40);

    color:white;
}

.card h3, .card .stSubheader{

    border-bottom:1px solid #263449;

    padding-bottom:10px;

    margin-bottom:16px;
}

/* Section subheader styling */

div[data-testid="stMarkdownContainer"] h3{

    font-weight:700;

    color:#F8FAFC;

    letter-spacing:.2px;
}

/* ===========================================
   LABELS
=========================================== */

label{

    color:#E2E8F0 !important;

    font-weight:600;

    font-size:14.5px;
}

/* ===========================================
   TEXT INPUT
=========================================== */

.stTextInput input{

    background:#1E293B;

    color:white;

    border:1.5px solid #334155;

    border-radius:10px;

    padding:12px 14px;

    transition:.25s;

    font-size:15px;
}

.stTextInput input:focus{

    border:1.5px solid #38BDF8;

    box-shadow:
    0 0 0 4px rgba(56,189,248,.15);
}

.stTextInput input::placeholder{

    color:#64748B;
}

/* ===========================================
   TEXT AREA
=========================================== */

textarea{

    background:#1E293B !important;

    color:white !important;

    border:1.5px solid #334155 !important;

    border-radius:10px !important;

    font-size:14.5px !important;
}

textarea:focus{

    border:1.5px solid #38BDF8 !important;

    box-shadow:0 0 0 4px rgba(56,189,248,.15) !important;
}

/* ===========================================
   FILE UPLOADER
=========================================== */

.stFileUploader{

    background:#141E33;

    border:1.6px dashed #38BDF8;

    border-radius:14px;

    padding:16px;
}

.stFileUploader:hover{

    border-color:#7DD3FC;
}

/* ===========================================
   BUTTON
=========================================== */

.stButton>button{

    width:100%;

    height:52px;

    border:none;

    border-radius:10px;

    font-size:16px;

    font-weight:700;

    letter-spacing:.2px;

    color:white;

    background:
    linear-gradient(
        90deg,
        #0284C7,
        #38BDF8
    );

    box-shadow:0 6px 16px rgba(2,132,199,.25);

    transition:.25s ease;
}

.stButton>button:hover{

    transform:translateY(-2px);

    box-shadow:
    0 12px 26px rgba(56,189,248,.35);

    filter:brightness(1.05);
}

.stButton>button:active{

    transform:translateY(0px);
}

/* ===========================================
   DOWNLOAD BUTTON
=========================================== */

.stDownloadButton>button{

    width:100%;

    height:50px;

    border:none;

    border-radius:10px;

    color:white;

    font-weight:700;

    font-size:15.5px;

    background:
    linear-gradient(
        90deg,
        #16A34A,
        #22C55E
    );

    box-shadow:0 6px 16px rgba(22,163,74,.25);

    transition:.25s ease;
}

.stDownloadButton>button:hover{

    transform:translateY(-2px);

    box-shadow:0 12px 24px rgba(34,197,94,.35);
}

/* ===========================================
   EXPANDER
=========================================== */

.streamlit-expanderHeader{

    color:white !important;

    font-size:15.5px;

    font-weight:700;
}

/* ===========================================
   ALERTS
=========================================== */

.stSuccess{

    background:rgba(34,197,94,.08);

    border-left:4px solid #22C55E;

    border-radius:8px;
}

.stWarning{

    background:rgba(245,158,11,.08);

    border-left:4px solid #F59E0B;

    border-radius:8px;
}

.stError{

    background:rgba(239,68,68,.08);

    border-left:4px solid #EF4444;

    border-radius:8px;
}

.stInfo{

    background:rgba(56,189,248,.08);

    border-left:4px solid #38BDF8;

    border-radius:8px;
}

/* ===========================================
   PROGRESS
=========================================== */

.stProgress>div>div>div{

    background:linear-gradient(90deg,#0284C7,#38BDF8);

    border-radius:6px;
}

/* ===========================================
   SIDEBAR
=========================================== */

section[data-testid="stSidebar"]{

    background:#0B1120;

    border-right:1px solid #1E293B;
}

section[data-testid="stSidebar"] *{

    color:white;
}

/* ===========================================
   DIVIDER
=========================================== */

hr{

    border-color:#1E293B !important;
}

/* ===========================================
   SCROLLBAR
=========================================== */

::-webkit-scrollbar{

    width:8px;
}

::-webkit-scrollbar-thumb{

    background:#334155;

    border-radius:20px;
}

::-webkit-scrollbar-thumb:hover{

    background:#475569;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------
# DATABASE
# ----------------------------------------

create_database()

# ----------------------------------------
# HEADER
# ----------------------------------------

st.markdown(
"""
<div class="header-badge">
<span>AI Powered Workflow</span>
</div>

<div class="main-title">
🤖 Multi-Agent Blog Generator
</div>

<div class="sub-title">
Generate High-Quality Blogs using an AI Multi-Agent Workflow
</div>
""",
unsafe_allow_html=True
)

# ----------------------------------------
# SESSION STATE
# ----------------------------------------

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

if "generated" not in st.session_state:
    st.session_state.generated = False

if "result" not in st.session_state:
    st.session_state.result = None

if "approved" not in st.session_state:
    st.session_state.approved = False

if "blog_topic" not in st.session_state:
    st.session_state.blog_topic = ""

# ----------------------------------------
# INPUT SECTION
# ----------------------------------------

st.markdown(
"""
<div class="card">
""",
unsafe_allow_html=True
)

st.subheader("📝 Blog Details")

topic = st.text_input(
    "Enter Blog Topic",
    placeholder="Example: Future of Artificial Intelligence"
)

uploaded_file = st.file_uploader(
    "📄 Upload PDF (Optional)",
    type=["pdf"]
)

st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------
# PDF PROCESSING
# ----------------------------------------

if uploaded_file is not None:

    if not st.session_state.pdf_uploaded:

        with st.spinner("📄 Processing PDF..."):

            try:

                pdf_text = load_pdf(uploaded_file)

                vector_store = create_vector_store(
                    pdf_text
                )

                st.session_state.vector_store = vector_store

                st.session_state.pdf_uploaded = True

                st.success(
                    "✅ PDF Processed Successfully!"
                )

            except Exception as e:

                st.error(
                    f"PDF Processing Failed\n\n{e}"
                )

# ----------------------------------------
# GENERATE BLOG
# ----------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 Generate Blog"):

    if topic.strip() == "":

        st.warning(
            "Please enter a blog topic."
        )

        st.stop()

    retrieved_context = ""

    if st.session_state.vector_store is not None:

        try:

            retrieved_context = retrieve_context(

                st.session_state.vector_store,

                topic

            )

        except Exception as e:

            st.error(e)

            st.stop()

    try:

        progress_text = st.empty()

        progress = st.progress(0)

        progress_text.info(
            "🤖 AI Agents are researching..."
        )

        progress.progress(20)

        result = graph.invoke(

            {

                "topic": topic,

                "pdf_context": "",

                "retrieved_context": retrieved_context

            }

        )

        progress.progress(60)

        progress_text.info(
            "✍ Writing Blog..."
        )

        progress.progress(90)

        st.session_state.result = result

        st.session_state.generated = True

        st.session_state.blog_topic = topic

        progress.progress(100)

        progress_text.success(
            "🎉 Blog Generated Successfully!"
        )

    except Exception as e:

        st.error(e)

# ----------------------------------------
# SHOW RESULT
# ----------------------------------------

if st.session_state.generated:

    result = st.session_state.result

    st.success("🎉 Blog Generated Successfully!")

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================
    # RESEARCH + OUTLINE
    # =====================================

    col1, col2 = st.columns(2)

    with col1:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("📚 Research Summary")

        st.write(result["research_summary"])

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("📝 Blog Outline")

        st.write(result["outline"])

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================
    # FINAL BLOG
    # =====================================

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📄 Final Blog")

    st.markdown(result["final_blog"])

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================
    # HUMAN REVIEW
    # =====================================

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("👨‍💻 Human Review")

    st.info(
        "Review the generated blog before approving it."
    )

    approve_col, reject_col = st.columns(2)

    with approve_col:

        if st.button(
            "✅ Approve Blog",
            use_container_width=True
        ):

            st.session_state.approved = True

            try:

                save_blog(

                    st.session_state.blog_topic,

                    result["final_blog"]

                )

                st.balloons()

                st.success(
                    "🎉 Blog Approved Successfully!"
                )

            except Exception as e:

                st.error(e)

    with reject_col:

        if st.button(
            "❌ Reject Blog",
            use_container_width=True
        ):

            st.session_state.approved = False

            st.warning(
                "Blog Rejected."
            )

    # =====================================
    # FEEDBACK
    # =====================================

    if not st.session_state.approved:

        st.markdown("<br>", unsafe_allow_html=True)

        feedback = st.text_area(

            "📝 Feedback",

            height=150,

            placeholder="""
Examples:

• Add more real-world examples.

• Reduce the overall length.

• Improve introduction.

• Improve conclusion.

• Make the tone more professional.
"""
        )

        if st.button(
            "💾 Save Feedback",
            use_container_width=True
        ):

            if feedback.strip() == "":

                st.warning(
                    "Please enter feedback first."
                )

            else:

                st.success(
                    "✅ Feedback Saved Successfully!"
                )

    # =====================================
    # DOWNLOAD
    # =====================================

    if st.session_state.approved:

        st.markdown("<br>", unsafe_allow_html=True)

        st.download_button(

            label="⬇ Download Blog",

            data=result["final_blog"],

            file_name="generated_blog.md",

            mime="text/markdown",

            use_container_width=True

        )

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------
# SIDEBAR
# ----------------------------------------

st.sidebar.markdown(
"""
<div style="
background:linear-gradient(135deg,#0284C7,#0EA5E9);
padding:24px 20px;
border-radius:16px;
text-align:center;
box-shadow:0 10px 24px rgba(2,132,199,.30);
">

<h2 style="
margin-bottom:6px;
color:white;
font-size:21px;
">
🤖 AI Blog Generator
</h2>

<p style="
margin:0;
color:#E0F2FE;
font-size:13.5px;
font-weight:500;
">
Powered by LangGraph + Streamlit
</p>

</div>
""",
unsafe_allow_html=True
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------
# BLOG HISTORY
# ----------------------------------------

st.sidebar.markdown(
"""
<h3 style="color:white; font-size:16.5px; margin-bottom:12px;">
📚 Blog History
</h3>
""",
unsafe_allow_html=True
)

history = get_history()

if history:

    for item in history:

        st.sidebar.markdown(
            f"""
<div style="
background:#141E33;
padding:14px 16px;
border-radius:12px;
margin-bottom:12px;
border-left:4px solid #38BDF8;
box-shadow:0 6px 16px rgba(0,0,0,.25);
">

<div style="
font-weight:700;
font-size:14.5px;
color:white;
margin-bottom:6px;
line-height:1.35;
">

📝 {item[0]}

</div>

<div style="
font-size:12.5px;
color:#94A3B8;
">

📅 {item[1]}

</div>

</div>
""",
            unsafe_allow_html=True
        )

else:

    st.sidebar.info(
        "No blogs generated yet."
    )

st.sidebar.markdown("---")

# ----------------------------------------
# FEATURES
# ----------------------------------------

st.sidebar.markdown(
"""
<div style="
background:#141E33;
padding:18px 20px;
border-radius:14px;
border:1px solid #263449;
">

<h3 style="
color:white;
margin-bottom:12px;
font-size:16px;
">
🚀 Features
</h3>

<p style="color:#CBD5E1; font-size:13.5px; line-height:2.1; margin:0;">

✅ Multi-Agent Workflow<br>
✅ Research Agent<br>
✅ Outline Generator<br>
✅ AI Blog Writer<br>
✅ Human Review<br>
✅ RAG PDF Support<br>
✅ Blog History<br>
✅ Markdown Download

</p>

</div>
""",
unsafe_allow_html=True
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------
# STATS
# ----------------------------------------

total_blogs = len(history)

st.sidebar.markdown(
f"""
<div style="
background:linear-gradient(135deg,#16A34A,#22C55E);
padding:18px 20px;
border-radius:14px;
text-align:center;
box-shadow:0 10px 20px rgba(22,163,74,.25);
">

<h3 style="
color:white;
margin:0;
font-size:15px;
font-weight:600;
letter-spacing:.3px;
">

📈 STATISTICS

</h3>

<h1 style="
color:white;
margin:8px 0 0 0;
font-size:38px;
font-weight:800;
">

{total_blogs}

</h1>

<p style="
margin-top:4px;
color:#F0FDF4;
font-size:13px;
font-weight:500;
">

Blogs Generated

</p>

</div>
""",
unsafe_allow_html=True
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------
# FOOTER
# ----------------------------------------

st.sidebar.markdown(
"""
<div style="
background:#141E33;
padding:14px;
border-radius:12px;
text-align:center;
border:1px solid #263449;
">

<p style="
margin:0;
font-size:12.5px;
color:#94A3B8;
line-height:1.7;
">

Made with ❤️ using
<br>
<b style="color:#38BDF8;">
Streamlit • LangGraph • RAG
</b>

</p>

</div>
""",
unsafe_allow_html=True
)