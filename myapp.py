"""
╔══════════════════════════════════════════════════════════╗
║          DATA CLEANING STUDIO  —  Streamlit App          ║
╚══════════════════════════════════════════════════════════╝
Run:  streamlit run app.py
Requires: streamlit, pandas, numpy, matplotlib, plotly, scipy, openpyxl
"""

import io
import json
import re
import warnings
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

matplotlib.use("Agg")
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────
# Optional heavy imports
# ─────────────────────────────────────────────────────────
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY = True
except ImportError:
    PLOTLY = False

try:
    from scipy import stats as scipy_stats
    SCIPY = True
except ImportError:
    SCIPY = False

# ══════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Data Cleaning Studio",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# # ══════════════════════════════════════════════════════════
# # CUSTOM CSS
# # ══════════════════════════════════════════════════════════
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;700;800&display=swap');

# :root {
#     --bg: #0f1117;
#     --surface: #1a1d27;
#     --surface2: #252836;
#     --accent: #7c6af7;
#     --accent2: #f97068;
#     --accent3: #4ecdc4;
#     --text: #e8e9f3;
#     --muted: #8b8fa8;
#     --border: #2e3148;
#     --success: #56c596;
#     --warn: #f4c542;
#     --danger: #f97068;
# }

# html, body, [class*="css"] {
#     font-family: 'Syne', sans-serif;
#     background-color: var(--bg) !important;
#     color: var(--text) !important;
# }

# .stApp { background-color: var(--bg) !important; }

# /* Sidebar */
# section[data-testid="stSidebar"] {
#     background: var(--surface) !important;
#     border-right: 1px solid var(--border);
# }
# section[data-testid="stSidebar"] * { color: var(--text) !important; }

# /* Headings */
# h1, h2, h3 { font-family: 'Syne', sans-serif !important; }
# h1 { font-weight: 800; font-size: 2rem; }

# /* Cards */
# .card {
#     background: var(--surface);
#     border: 1px solid var(--border);
#     border-radius: 12px;
#     padding: 1.2rem 1.4rem;
#     margin-bottom: 1rem;
# }
# .metric-box {
#     background: var(--surface2);
#     border: 1px solid var(--border);
#     border-radius: 10px;
#     padding: 1rem;
#     text-align: center;
# }
# .metric-box .val {
#     font-size: 2rem;
#     font-weight: 800;
#     color: var(--accent);
#     font-family: 'JetBrains Mono', monospace;
# }
# .metric-box .lbl { font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }

# /* Badges */
# .badge {
#     display: inline-block;
#     padding: 2px 10px;
#     border-radius: 99px;
#     font-size: 0.72rem;
#     font-family: 'JetBrains Mono', monospace;
#     font-weight: 600;
# }
# .badge-purple { background: #3d3580; color: #c4beff; }
# .badge-teal   { background: #1a4a46; color: #4ecdc4; }
# .badge-red    { background: #4a1e1d; color: #f97068; }
# .badge-green  { background: #1a3d2e; color: #56c596; }

# /* Section headers */
# .section-title {
#     font-size: 0.7rem;
#     text-transform: uppercase;
#     letter-spacing: 2px;
#     color: var(--muted);
#     margin-bottom: 0.5rem;
#     font-family: 'JetBrains Mono', monospace;
# }

# /* Log entries */
# .log-entry {
#     background: var(--surface2);
#     border-left: 3px solid var(--accent);
#     padding: 0.5rem 0.8rem;
#     margin: 0.3rem 0;
#     border-radius: 0 6px 6px 0;
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.78rem;
#     color: var(--text);
# }

# /* Violation rows */
# .violation { border-left-color: var(--accent2) !important; }

# /* Buttons */
# .stButton > button {
#     background: var(--accent) !important;
#     color: white !important;
#     border: none !important;
#     border-radius: 8px !important;
#     font-family: 'Syne', sans-serif !important;
#     font-weight: 700 !important;
#     padding: 0.4rem 1.2rem !important;
#     transition: opacity 0.2s !important;
# }
# .stButton > button:hover { opacity: 0.85 !important; }

# /* Dataframe */
# .stDataFrame { border-radius: 10px; overflow: hidden; }

# /* Expander */
# .streamlit-expanderHeader {
#     background: var(--surface2) !important;
#     border-radius: 8px !important;
#     font-family: 'Syne', sans-serif !important;
# }

# /* Input widgets */
# .stSelectbox div[data-baseweb="select"] > div,
# .stMultiSelect div[data-baseweb="select"] > div,
# .stTextInput input, .stNumberInput input {
#     background: var(--surface2) !important;
#     border-color: var(--border) !important;
#     color: var(--text) !important;
# }

# /* Tabs */
# .stTabs [data-baseweb="tab-list"] { gap: 4px; }
# .stTabs [data-baseweb="tab"] {
#     background: var(--surface2) !important;
#     border-radius: 8px 8px 0 0 !important;
#     color: var(--muted) !important;
#     font-family: 'Syne', sans-serif !important;
#     font-weight: 600 !important;
# }
# .stTabs [aria-selected="true"] {
#     background: var(--accent) !important;
#     color: white !important;
# }
# </style>
# """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SESSION STATE INIT
# ══════════════════════════════════════════════════════════
def init_session():
    defaults = {
        "df_original": None,
        "df_working": None,
        "transform_log": [],
        "file_name": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ══════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════
def log_step(operation: str, params: dict, affected_cols=None):
    entry = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "operation": operation,
        "params": params,
        "affected_cols": affected_cols or [],
    }
    st.session_state.transform_log.append(entry)

def wdf() -> pd.DataFrame | None:
    return st.session_state.df_working

def set_wdf(df: pd.DataFrame):
    st.session_state.df_working = df.copy()

@st.cache_data(show_spinner=False)
def load_csv(content: bytes, name: str) -> pd.DataFrame:
    try:
        return pd.read_csv(io.BytesIO(content))
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")
        return None

@st.cache_data(show_spinner=False)
def load_excel(content: bytes, name: str) -> pd.DataFrame:
    try:
        return pd.read_excel(io.BytesIO(content))
    except Exception as e:
        st.error(f"Failed to read Excel: {e}")
        return None

def missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    miss = df.isnull().sum()
    pct = (miss / len(df) * 100).round(2)
    return pd.DataFrame({"Column": df.columns, "Missing": miss.values, "Missing %": pct.values})

def numeric_cols(df):
    return df.select_dtypes(include="number").columns.tolist()

def cat_cols(df):
    return df.select_dtypes(include=["object", "category"]).columns.tolist()

def safe_rerun():
    st.rerun()

# ══════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("##  Data Cleaning Studio")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        [" Upload & Overview", " Cleaning Studio", " Visualization", " Export & Report"],
        label_visibility="collapsed",
    )

    st.markdown("---")

    # Transformation log in sidebar
    st.markdown("###  Transform Log")
    log = st.session_state.transform_log
    if not log:
        st.caption("No transformations yet.")
    else:
        for i, entry in enumerate(log[-5:], 1):
            st.markdown(
                f'<div class="log-entry">#{len(log)-5+i} [{entry["timestamp"]}]<br>'
                f'<b>{entry["operation"]}</b></div>',
                unsafe_allow_html=True,
            )
        if len(log) > 5:
            st.caption(f"… and {len(log)-5} more. See Export page for full log.")

    st.markdown("---")

    # Undo / Reset
    col1, col2 = st.columns(2)
    with col1:
        if st.button("↩ Undo", use_container_width=True):
            if st.session_state.transform_log:
                st.session_state.transform_log.pop()
                st.info("Last step removed from log. Note: dataframe undo requires re-applying remaining steps from original.")
            else:
                st.warning("Nothing to undo.")
    with col2:
        if st.button(" Reset", use_container_width=True):
            if st.session_state.df_original is not None:
                set_wdf(st.session_state.df_original)
                st.session_state.transform_log = []
                st.success("Reset to original!")
                safe_rerun()

    # AI Toggle
    st.markdown("---")
    ai_enabled = st.toggle("🤖 Enable AI Assistant", value=False)
    if ai_enabled:
        anthropic_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
        st.caption("⚠️ AI outputs may be imperfect. Always review suggestions.")
    else:
        anthropic_key = None

# ══════════════════════════════════════════════════════════
# PAGE A — UPLOAD & OVERVIEW
# ══════════════════════════════════════════════════════════
if page == " Upload & Overview":
    st.markdown("#  Upload & Overview")

    # Upload
    uploaded = st.file_uploader(
        "Upload your dataset",
        type=["csv", "xlsx", "xls"],
        help="Supports CSV and Excel files",
    )

    if uploaded:
        with st.spinner("Loading dataset…"):
            content = uploaded.read()
            name = uploaded.name
            if name.endswith(".csv"):
                df = load_csv(content, name)
            else:
                df = load_excel(content, name)

        if df is not None:
            st.session_state.df_original = df.copy()
            set_wdf(df)
            st.session_state.file_name = name
            st.success(f" Loaded **{name}**")

    # Reset session button
    if st.button(" Reset Session", type="secondary"):
        for k in ["df_original", "df_working", "transform_log", "file_name"]:
            st.session_state[k] = None if k != "transform_log" else []
        st.success("Session reset.")
        safe_rerun()

    df = wdf()
    if df is None:
        st.info(" Upload a file to get started.")
        st.stop()

    st.markdown("---")

    # ── Shape & column count ──────────────────────────────
    rows, cols = df.shape
    num_n = len(numeric_cols(df))
    num_c = len(cat_cols(df))
    dup   = df.duplicated().sum()
    miss  = df.isnull().sum().sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    for col_widget, val, lbl in [
        (c1, rows,  "Rows"),
        (c2, cols,  "Columns"),
        (c3, num_n, "Numeric"),
        (c4, num_c, "Categorical"),
        (c5, dup,   "Duplicates"),
    ]:
        col_widget.markdown(
            f'<div class="metric-box"><div class="val">{val}</div><div class="lbl">{lbl}</div></div>',
            unsafe_allow_html=True,
        )

    # Number of columns box (required)
    st.markdown(
        f'<div class="card" style="margin-top:1rem">'
        f'<span class="section-title">Dataset has</span><br>'
        f'<b style="font-size:1.5rem;color:#7c6af7">{cols}</b> columns &nbsp;|&nbsp; '
        f'<b style="font-size:1.5rem;color:#4ecdc4">{rows}</b> rows</div>',
        unsafe_allow_html=True,
    )

    # ── Column types ─────────────────────────────────────
    with st.expander(" Column Names & Data Types", expanded=True):
        type_df = pd.DataFrame({
            "Column": df.columns,
            "Dtype": [str(df[c].dtype) for c in df.columns],
            "Sample": [str(df[c].iloc[0]) if len(df) > 0 else "—" for c in df.columns],
            "Unique": [df[c].nunique() for c in df.columns],
        })
        st.dataframe(type_df, use_container_width=True, hide_index=True)

    # ── Summary stats ─────────────────────────────────────
    with st.expander(" Summary Statistics", expanded=False):
        tab1, tab2 = st.tabs(["Numeric", "Categorical"])
        with tab1:
            num_df = df.select_dtypes(include="number")
            if not num_df.empty:
                st.dataframe(num_df.describe().T.round(3), use_container_width=True)
            else:
                st.info("No numeric columns.")
        with tab2:
            cat_df = df.select_dtypes(include=["object", "category"])
            if not cat_df.empty:
                st.dataframe(cat_df.describe().T, use_container_width=True)
            else:
                st.info("No categorical columns.")

    # ── Missing values ────────────────────────────────────
    with st.expander(" Missing Values", expanded=True):
        ms = missing_summary(df)
        ms_nonzero = ms[ms["Missing"] > 0]
        if ms_nonzero.empty:
            st.success("No missing values found! 🎉")
        else:
            st.dataframe(ms_nonzero, use_container_width=True, hide_index=True)
            # Visual bar
            fig, ax = plt.subplots(figsize=(8, max(2, len(ms_nonzero) * 0.35)))
            fig.patch.set_facecolor("#1a1d27")
            ax.set_facecolor("#1a1d27")
            cols_list = ms_nonzero["Column"].tolist()
            pcts = ms_nonzero["Missing %"].tolist()
            bars = ax.barh(cols_list, pcts, color="#7c6af7", edgecolor="none", height=0.6)
            ax.set_xlabel("Missing %", color="#8b8fa8")
            ax.tick_params(colors="#e8e9f3")
            for spine in ax.spines.values():
                spine.set_color("#2e3148")
            st.pyplot(fig, use_container_width=True)
            plt.close()

    # ── Duplicates ────────────────────────────────────────
    with st.expander(" Duplicates"):
        dup_count = df.duplicated().sum()
        if dup_count == 0:
            st.success("No duplicate rows found.")
        else:
            st.warning(f"Found **{dup_count}** duplicate rows.")
            if st.button("Show duplicate rows"):
                st.dataframe(df[df.duplicated(keep=False)], use_container_width=True)


# ══════════════════════════════════════════════════════════
# PAGE B — CLEANING STUDIO
# ══════════════════════════════════════════════════════════
elif page == " Cleaning Studio":
    st.markdown("#  Cleaning & Preparation Studio")

    df = wdf()
    if df is None:
        st.warning("Please upload a dataset first.")
        st.stop()

    # AI natural language command
    if ai_enabled and anthropic_key:
        with st.expander(" AI: Natural Language Cleaning Command"):
            st.caption("⚠️ AI suggestions may be imperfect. Review before applying.")
            nl_cmd = st.text_area("Describe what you want to do:", placeholder='e.g. "Replace nulls in Age with median, then lowercase the Category column"')
            if st.button("Get AI Suggestion") and nl_cmd:
                try:
                    import anthropic
                    client = anthropic.Anthropic(api_key=anthropic_key)
                    schema = {c: str(df[c].dtype) for c in df.columns}
                    prompt = (
                        f"Dataset columns and types: {json.dumps(schema)}\n"
                        f"User command: {nl_cmd}\n\n"
                        "Translate this into a list of cleaning steps. For each step give:\n"
                        "- operation (one of: fill_missing, drop_rows_missing, drop_col_missing, remove_duplicates, rename_col, drop_col, type_convert, standardize_case, strip_whitespace, cap_outliers, remove_outliers, normalize, encode_onehot)\n"
                        "- column(s)\n- parameters\n"
                        "Reply ONLY with a JSON array."
                    )
                    resp = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=800,
                        messages=[{"role": "user", "content": prompt}],
                    )
                    raw = resp.content[0].text
                    clean_raw = re.sub(r"```json|```", "", raw).strip()
                    steps = json.loads(clean_raw)
                    st.markdown("**Suggested steps:**")
                    st.json(steps)
                    st.info("Review the steps above, then apply them manually using the sections below.")
                except Exception as e:
                    st.error(f"AI error: {e}")

    tabs = st.tabs([
        " Missing Values",
        " Duplicates",
        " Data Types",
        " Categorical",
        " Numeric",
        " Normalization",
        " Columns",
        " Validation",
    ])

    # ── 4.1 MISSING VALUES ────────────────────────────────
    with tabs[0]:
        st.markdown("###  Missing Value Handler")
        ms = missing_summary(df)
        st.dataframe(ms, use_container_width=True, hide_index=True)

        cols_with_missing = ms[ms["Missing"] > 0]["Column"].tolist()
        if not cols_with_missing:
            st.success("No missing values! Nothing to do here.")
        else:
            st.markdown("#### Per-Column Action")
            sel_cols = st.multiselect("Select columns to act on", cols_with_missing, default=cols_with_missing[:1])
            action = st.selectbox("Action", [
                "Drop rows with missing",
                "Fill with constant",
                "Fill with mean",
                "Fill with median",
                "Fill with mode",
                "Forward fill",
                "Backward fill",
            ])

            constant_val = ""
            if action == "Fill with constant":
                constant_val = st.text_input("Constant value")

            thresh_pct = None
            if st.checkbox("Also drop columns above missing threshold"):
                thresh_pct = st.slider("Drop column if missing % ≥", 0, 100, 50)

            if st.button("Apply Missing Value Action"):
                df2 = df.copy()
                before_rows = len(df2)
                try:
                    for c in sel_cols:
                        if action == "Drop rows with missing":
                            df2 = df2.dropna(subset=[c])
                        elif action == "Fill with constant":
                            df2[c] = df2[c].fillna(constant_val)
                        elif action == "Fill with mean":
                            df2[c] = df2[c].fillna(df2[c].mean())
                        elif action == "Fill with median":
                            df2[c] = df2[c].fillna(df2[c].median())
                        elif action == "Fill with mode":
                            df2[c] = df2[c].fillna(df2[c].mode().iloc[0])
                        elif action == "Forward fill":
                            df2[c] = df2[c].ffill()
                        elif action == "Backward fill":
                            df2[c] = df2[c].bfill()

                    if thresh_pct is not None:
                        before_cols = df2.shape[1]
                        thresh = thresh_pct / 100
                        df2 = df2.dropna(axis=1, thresh=int((1 - thresh) * len(df2)))
                        st.info(f"Dropped {before_cols - df2.shape[1]} columns above {thresh_pct}% missing threshold.")

                    after_rows = len(df2)
                    set_wdf(df2)
                    df = df2
                    log_step("Missing Value Handler", {"action": action, "constant": constant_val, "columns": sel_cols})
                    st.success(f" Done. Rows: {before_rows} → {after_rows}")
                except Exception as e:
                    st.error(f"Error: {e}")

    # ── 4.2 DUPLICATES ────────────────────────────────────
    with tabs[1]:
        st.markdown("###  Duplicate Handler")
        all_dupes = df.duplicated().sum()
        st.metric("Full-row duplicates", all_dupes)

        st.markdown("#### Subset-based detection")
        subset = st.multiselect("Check duplicates by columns (empty = all)", df.columns.tolist())
        subset_kw = subset if subset else None
        dup_count_sub = df.duplicated(subset=subset_kw).sum()
        st.metric("Duplicates found (selected subset)", dup_count_sub)

        if st.button("Show duplicate groups"):
            dup_df = df[df.duplicated(subset=subset_kw, keep=False)].sort_values(by=subset or df.columns.tolist())
            st.dataframe(dup_df, use_container_width=True)

        keep = st.radio("Keep", ["first", "last", "none (drop all)"])
        keep_val = False if keep == "none (drop all)" else keep

        if st.button("Remove Duplicates"):
            before = len(df)
            df2 = df.drop_duplicates(subset=subset_kw, keep=keep_val)
            after = len(df2)
            set_wdf(df2)
            df = df2
            log_step("Remove Duplicates", {"subset": subset, "keep": keep})
            st.success(f" Removed {before - after} duplicates. Rows: {before} → {after}")

    # ── 4.3 DATA TYPES ────────────────────────────────────
    with tabs[2]:
        st.markdown("###  Data Types & Parsing")

        col_sel = st.selectbox("Select column", df.columns.tolist())
        target_type = st.selectbox("Convert to", ["numeric", "categorical", "datetime", "string"])

        dt_format = None
        if target_type == "datetime":
            dt_format = st.text_input("Datetime format (blank = auto)", placeholder="%Y-%m-%d")

        dirty_numeric = st.checkbox("Strip dirty characters before numeric parse (commas, $, £, €, %)")

        if st.button("Convert Type"):
            df2 = df.copy()
            try:
                if dirty_numeric and target_type == "numeric":
                    df2[col_sel] = df2[col_sel].astype(str).str.replace(r"[,$£€%\s]", "", regex=True)
                if target_type == "numeric":
                    df2[col_sel] = pd.to_numeric(df2[col_sel], errors="coerce")
                elif target_type == "categorical":
                    df2[col_sel] = df2[col_sel].astype("category")
                elif target_type == "datetime":
                    fmt = dt_format if dt_format else None
                    df2[col_sel] = pd.to_datetime(df2[col_sel], format=fmt, errors="coerce")
                elif target_type == "string":
                    df2[col_sel] = df2[col_sel].astype(str)
                set_wdf(df2)
                df = df2
                log_step("Type Conversion", {"column": col_sel, "to": target_type, "dirty_strip": dirty_numeric})
                st.success(f" Converted **{col_sel}** → {target_type}")
            except Exception as e:
                st.error(f"Error: {e}")

    # ── 4.4 CATEGORICAL TOOLS ─────────────────────────────
    with tabs[3]:
        st.markdown("###  Categorical Data Tools")
        cat_list = cat_cols(df) + [c for c in df.columns if df[c].dtype.name == "category"]
        if not cat_list:
            st.info("No categorical columns detected.")
        else:
            cc = st.selectbox("Column", cat_list, key="cat_col")

            subtab1, subtab2, subtab3, subtab4 = st.tabs(["Standardize", "Map Values", "Rare Grouping", "One-Hot Encode"])

            with subtab1:
                op = st.selectbox("Operation", ["Trim whitespace", "Lowercase", "Title case", "Uppercase"])
                if st.button("Apply Standardization"):
                    df2 = df.copy()
                    if op == "Trim whitespace":
                        df2[cc] = df2[cc].astype(str).str.strip()
                    elif op == "Lowercase":
                        df2[cc] = df2[cc].astype(str).str.lower()
                    elif op == "Title case":
                        df2[cc] = df2[cc].astype(str).str.title()
                    elif op == "Uppercase":
                        df2[cc] = df2[cc].astype(str).str.upper()
                    set_wdf(df2); df = df2
                    log_step("Categorical Standardize", {"column": cc, "op": op})
                    st.success(f" {op} applied to **{cc}**")

            with subtab2:
                st.markdown("Enter mapping as `old_value → new_value` (one per line):")
                mapping_text = st.text_area("Mapping", placeholder="Yes → 1\nNo → 0\nMaybe → 0")
                set_other = st.checkbox("Set unmatched values to 'Other'")
                if st.button("Apply Mapping"):
                    mapping = {}
                    for line in mapping_text.strip().split("\n"):
                        if "→" in line:
                            k, v = line.split("→", 1)
                            mapping[k.strip()] = v.strip()
                    if mapping:
                        df2 = df.copy()
                        df2[cc] = df2[cc].replace(mapping)
                        if set_other:
                            df2[cc] = df2[cc].apply(lambda x: x if x in mapping.values() else "Other")
                        set_wdf(df2); df = df2
                        log_step("Categorical Mapping", {"column": cc, "mapping": mapping})
                        st.success(f" Mapping applied. Preview:")
                        st.dataframe(df2[cc].value_counts().head(10), use_container_width=True)
                    else:
                        st.warning("No valid mappings parsed. Use format: `old → new`")

            with subtab3:
                freq_thresh = st.slider("Group categories with frequency below (%)", 0.5, 20.0, 5.0, 0.5)
                other_label = st.text_input("Label for grouped category", "Other")
                vc = df[cc].value_counts(normalize=True) * 100
                rare = vc[vc < freq_thresh].index.tolist()
                st.info(f"{len(rare)} rare categories will be grouped: {rare[:10]}")
                if st.button("Apply Rare Grouping"):
                    df2 = df.copy()
                    df2[cc] = df2[cc].apply(lambda x: other_label if x in rare else x)
                    set_wdf(df2); df = df2
                    log_step("Rare Category Grouping", {"column": cc, "threshold": freq_thresh, "rare_count": len(rare)})
                    st.success(f" Grouped {len(rare)} rare categories → '{other_label}'")

            with subtab4:
                max_unique = df[cc].nunique()
                st.info(f"**{cc}** has {max_unique} unique values. One-hot will create {max_unique} new columns.")
                drop_first = st.checkbox("Drop first (avoid multicollinearity)", True)
                if st.button("One-Hot Encode"):
                    if max_unique > 50:
                        st.warning(f"Column has {max_unique} unique values — this will add many columns. Proceed?")
                    df2 = df.copy()
                    dummies = pd.get_dummies(df2[[cc]], prefix=cc, drop_first=drop_first)
                    df2 = pd.concat([df2.drop(columns=[cc]), dummies], axis=1)
                    set_wdf(df2); df = df2
                    log_step("One-Hot Encode", {"column": cc, "drop_first": drop_first, "new_cols": dummies.shape[1]})
                    st.success(f" Added {dummies.shape[1]} encoded columns. Dataset now has {df2.shape[1]} columns.")

    # ── 4.5 NUMERIC CLEANING ──────────────────────────────
    with tabs[4]:
        st.markdown("###  Numeric Cleaning & Outliers")
        num_list = numeric_cols(df)
        if not num_list:
            st.info("No numeric columns.")
        else:
            nc = st.selectbox("Column", num_list, key="num_col")

            method = st.radio("Detection method", ["IQR", "Z-score"])
            if method == "IQR":
                iqr_mult = st.slider("IQR multiplier", 1.0, 3.0, 1.5, 0.1)
                Q1 = df[nc].quantile(0.25)
                Q3 = df[nc].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - iqr_mult * IQR
                upper = Q3 + iqr_mult * IQR
            else:
                z_thresh = st.slider("Z-score threshold", 1.0, 5.0, 3.0, 0.1)
                mean = df[nc].mean()
                std = df[nc].std()
                lower = mean - z_thresh * std
                upper = mean + z_thresh * std

            outliers = df[(df[nc] < lower) | (df[nc] > upper)]
            st.metric("Outliers detected", len(outliers), f"{len(outliers)/len(df)*100:.1f}%")

            action = st.selectbox("Action", ["Do nothing", "Cap / Winsorize", "Remove outlier rows"])

            cap_lo = st.slider("Cap lower quantile", 0.0, 0.1, 0.01, 0.005) if action == "Cap / Winsorize" else None
            cap_hi = st.slider("Cap upper quantile", 0.9, 1.0, 0.99, 0.005) if action == "Cap / Winsorize" else None

            if st.button("Apply Outlier Action") and action != "Do nothing":
                df2 = df.copy()
                before = len(df2)
                try:
                    if action == "Cap / Winsorize":
                        lo_val = df2[nc].quantile(cap_lo)
                        hi_val = df2[nc].quantile(cap_hi)
                        df2[nc] = df2[nc].clip(lower=lo_val, upper=hi_val)
                        msg = f"Capped **{nc}** to [{lo_val:.2f}, {hi_val:.2f}]"
                    elif action == "Remove outlier rows":
                        df2 = df2[(df2[nc] >= lower) & (df2[nc] <= upper)]
                        msg = f"Removed {before - len(df2)} rows with outliers in **{nc}**"
                    set_wdf(df2); df = df2
                    log_step("Outlier Handling", {"column": nc, "method": method, "action": action})
                    st.success(f"✅ {msg}")
                except Exception as e:
                    st.error(f"Error: {e}")

    # ── 4.6 NORMALIZATION ─────────────────────────────────
    with tabs[5]:
        st.markdown("###  Normalization / Scaling")
        num_list2 = numeric_cols(df)
        if not num_list2:
            st.info("No numeric columns.")
        else:
            scale_cols = st.multiselect("Select columns to scale", num_list2)
            scale_method = st.selectbox("Method", ["Min-Max (0–1)", "Z-score Standardization", "Robust (IQR-based)"])

            if scale_cols and st.button("Preview"):
                before_stats = df[scale_cols].describe().loc[["mean", "std", "min", "max"]].T.round(4)
                st.markdown("**Before:**")
                st.dataframe(before_stats, use_container_width=True)

            if scale_cols and st.button("Apply Scaling"):
                df2 = df.copy()
                try:
                    for c in scale_cols:
                        if scale_method == "Min-Max (0–1)":
                            mn, mx = df2[c].min(), df2[c].max()
                            df2[c] = (df2[c] - mn) / (mx - mn) if mx != mn else 0.0
                        elif scale_method == "Z-score Standardization":
                            mu, sigma = df2[c].mean(), df2[c].std()
                            df2[c] = (df2[c] - mu) / sigma if sigma != 0 else 0.0
                        elif scale_method == "Robust (IQR-based)":
                            med = df2[c].median()
                            iqr = df2[c].quantile(0.75) - df2[c].quantile(0.25)
                            df2[c] = (df2[c] - med) / iqr if iqr != 0 else 0.0

                    after_stats = df2[scale_cols].describe().loc[["mean", "std", "min", "max"]].T.round(4)
                    set_wdf(df2); df = df2
                    log_step("Normalization", {"method": scale_method, "columns": scale_cols})
                    st.success(" Scaling applied!")
                    st.markdown("**After:**")
                    st.dataframe(after_stats, use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")

    # ── 4.7 COLUMN OPERATIONS ─────────────────────────────
    with tabs[6]:
        st.markdown("###  Column Operations")

        op_tab1, op_tab2, op_tab3, op_tab4 = st.tabs(["Rename", "Drop", "New Column", "Binning"])

        with op_tab1:
            old_name = st.selectbox("Column to rename", df.columns.tolist(), key="rename_col")
            new_name = st.text_input("New name", key="new_name_input")
            if st.button("Rename"):
                if new_name and new_name != old_name:
                    df2 = df.rename(columns={old_name: new_name})
                    set_wdf(df2); df = df2
                    log_step("Rename Column", {"from": old_name, "to": new_name})
                    st.success(f" Renamed **{old_name}** → **{new_name}**")
                else:
                    st.warning("Enter a different new name.")

        with op_tab2:
            drop_cols_sel = st.multiselect("Columns to drop", df.columns.tolist())
            if st.button("Drop Selected Columns"):
                if drop_cols_sel:
                    df2 = df.drop(columns=drop_cols_sel)
                    set_wdf(df2); df = df2
                    log_step("Drop Columns", {"columns": drop_cols_sel})
                    st.success(f" Dropped: {drop_cols_sel}")
                else:
                    st.warning("Select at least one column.")

        with op_tab3:
            new_col_name = st.text_input("New column name")
            formula = st.text_input(
                "Formula (use column names as variables)",
                placeholder="col_a / col_b  OR  col_a - col_a.mean()  OR  log(col_a)"
            )
            st.caption("Available functions: log, sqrt, abs, exp. Use `df['col']` syntax for safety, or column names directly.")
            if st.button("Create Column"):
                if new_col_name and formula:
                    try:
                        df2 = df.copy()
                        local_ns = {"df": df2, "np": np, "log": np.log, "sqrt": np.sqrt, "abs": np.abs, "exp": np.exp}
                        for c in df2.columns:
                            safe_c = c.replace(" ", "_").replace("-", "_")
                            local_ns[safe_c] = df2[c]
                        df2[new_col_name] = eval(formula.replace(c, safe_c) if " " in c else formula, local_ns)
                        set_wdf(df2); df = df2
                        log_step("Create Column", {"name": new_col_name, "formula": formula})
                        st.success(f" Created column **{new_col_name}**")
                    except Exception as e:
                        st.error(f"Formula error: {e}")
                else:
                    st.warning("Enter both a name and a formula.")

        with op_tab4:
            bin_col = st.selectbox("Column to bin", numeric_cols(df), key="bin_col")
            n_bins = st.slider("Number of bins", 2, 20, 5)
            bin_method = st.radio("Binning method", ["Equal width", "Quantile"])
            bin_col_name = st.text_input("Output column name", f"{bin_col}_bin")
            if st.button("Apply Binning"):
                df2 = df.copy()
                try:
                    if bin_method == "Equal width":
                        df2[bin_col_name] = pd.cut(df2[bin_col], bins=n_bins, precision=2).astype(str)
                    else:
                        df2[bin_col_name] = pd.qcut(df2[bin_col], q=n_bins, precision=2, duplicates="drop").astype(str)
                    set_wdf(df2); df = df2
                    log_step("Binning", {"column": bin_col, "bins": n_bins, "method": bin_method, "output": bin_col_name})
                    st.success(f" Binned **{bin_col}** → **{bin_col_name}**")
                    st.dataframe(df2[bin_col_name].value_counts(), use_container_width=True)
                except Exception as e:
                    st.error(f"Binning error: {e}")

    # ── 4.8 VALIDATION ────────────────────────────────────
    with tabs[7]:
        st.markdown("###  Data Validation Rules")
        st.caption("Define rules and see which rows violate them.")

        violations_all = pd.DataFrame()

        with st.expander("Numeric Range Check"):
            range_col = st.selectbox("Column", numeric_cols(df), key="range_col")
            range_min = st.number_input("Min value", value=float(df[range_col].min()) if len(numeric_cols(df)) > 0 else 0.0)
            range_max = st.number_input("Max value", value=float(df[range_col].max()) if len(numeric_cols(df)) > 0 else 100.0)
            if st.button("Check Range"):
                mask = (df[range_col] < range_min) | (df[range_col] > range_max)
                v = df[mask].copy()
                v["_violation"] = f"{range_col} out of [{range_min}, {range_max}]"
                st.warning(f"{mask.sum()} violations found.")
                if not v.empty:
                    st.dataframe(v, use_container_width=True)
                    violations_all = pd.concat([violations_all, v])

        with st.expander("Allowed Categories Check"):
            cat_check_col = st.selectbox("Column", cat_cols(df) or df.columns.tolist(), key="cat_check_col")
            allowed_raw = st.text_input("Allowed values (comma-separated)", "")
            if st.button("Check Categories"):
                if allowed_raw:
                    allowed = [x.strip() for x in allowed_raw.split(",")]
                    mask = ~df[cat_check_col].isin(allowed)
                    v = df[mask].copy()
                    v["_violation"] = f"{cat_check_col} not in allowed list"
                    st.warning(f"{mask.sum()} violations found.")
                    if not v.empty:
                        st.dataframe(v, use_container_width=True)

        with st.expander("Non-Null Constraint"):
            nn_cols = st.multiselect("Columns that must be non-null", df.columns.tolist())
            if st.button("Check Non-Null"):
                for c in nn_cols:
                    null_count = df[c].isnull().sum()
                    if null_count > 0:
                        st.warning(f"**{c}**: {null_count} null values (constraint violated)")
                    else:
                        st.success(f"**{c}**: ✓ No nulls")

        if not violations_all.empty:
            st.markdown("#### Export Violations")
            csv = violations_all.to_csv(index=False).encode()
            st.download_button("Download violations CSV", csv, "violations.csv", "text/csv")


# ══════════════════════════════════════════════════════════
# PAGE C — VISUALIZATION BUILDER
# ══════════════════════════════════════════════════════════
elif page == " Visualization":
    st.markdown("#  Visualization Builder")

    df = wdf()
    if df is None:
        st.warning("Please upload a dataset first.")
        st.stop()

    # AI chart suggestion
    if ai_enabled and anthropic_key:
        with st.expander(" AI: Chart Suggestions"):
            st.caption("⚠️ AI suggestions may be imperfect.")
            if st.button("Suggest charts for my data"):
                try:
                    import anthropic
                    client = anthropic.Anthropic(api_key=anthropic_key)
                    schema = {c: str(df[c].dtype) for c in df.columns}
                    prompt = (
                        f"Dataset columns and types: {json.dumps(schema)}\n"
                        "Suggest 3-5 interesting visualizations for this data. "
                        "For each, state chart type, x-axis, y-axis, and why it's useful. Be concise."
                    )
                    resp = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=600,
                        messages=[{"role": "user", "content": prompt}],
                    )
                    st.markdown(resp.content[0].text)
                except Exception as e:
                    st.error(f"AI error: {e}")

    # ── Filters ───────────────────────────────────────────
    with st.expander(" Filters", expanded=False):
        df_filtered = df.copy()
        cat_filter_col = st.selectbox("Filter by category column", ["(none)"] + cat_cols(df))
        if cat_filter_col != "(none)":
            cats = df_filtered[cat_filter_col].dropna().unique().tolist()
            selected_cats = st.multiselect("Include categories", cats, default=cats)
            df_filtered = df_filtered[df_filtered[cat_filter_col].isin(selected_cats)]

        num_filter_col = st.selectbox("Filter by numeric range", ["(none)"] + numeric_cols(df))
        if num_filter_col != "(none)":
            mn = float(df_filtered[num_filter_col].min())
            mx = float(df_filtered[num_filter_col].max())
            lo, hi = st.slider("Range", mn, mx, (mn, mx))
            df_filtered = df_filtered[(df_filtered[num_filter_col] >= lo) & (df_filtered[num_filter_col] <= hi)]

        st.caption(f"Filtered dataset: {len(df_filtered)} rows")

    # ── Chart Config ─────────────────────────────────────
    st.markdown("### Chart Configuration")

    col1, col2 = st.columns([1, 2])

    with col1:
        chart_type = st.selectbox("Chart type", [
            "Histogram", "Box Plot", "Scatter Plot",
            "Line Chart", "Bar Chart", "Heatmap / Correlation",
        ])

        all_cols = df_filtered.columns.tolist()
        num_list = numeric_cols(df_filtered)
        cat_list = cat_cols(df_filtered)

        x_col = st.selectbox("X axis", all_cols, key="x_col")
        y_col = st.selectbox("Y axis", ["(none)"] + num_list, key="y_col")
        color_col = st.selectbox("Color / Group by", ["(none)"] + all_cols, key="color_col")

        agg_func = st.selectbox("Aggregation (for bar chart)", ["none", "sum", "mean", "count", "median"])

        top_n = None
        if chart_type == "Bar Chart":
            top_n = st.slider("Top N categories", 3, 50, 10)

    with col2:
        try:
            fig_plotly = None
            fig_mpl = None
            color_arg = None if color_col == "(none)" else color_col
            y_arg = None if y_col == "(none)" else y_col

            if PLOTLY:
                if chart_type == "Histogram":
                    fig_plotly = px.histogram(df_filtered, x=x_col, color=color_arg,
                                              template="plotly_dark", title=f"Histogram of {x_col}")

                elif chart_type == "Box Plot":
                    fig_plotly = px.box(df_filtered, x=color_arg, y=x_col if not y_arg else y_arg,
                                        template="plotly_dark", title=f"Box Plot")

                elif chart_type == "Scatter Plot":
                    if y_arg:
                        fig_plotly = px.scatter(df_filtered, x=x_col, y=y_arg, color=color_arg,
                                                template="plotly_dark", title=f"{x_col} vs {y_arg}", opacity=0.7)
                    else:
                        st.warning("Select a Y axis for scatter plot.")

                elif chart_type == "Line Chart":
                    df_line = df_filtered.sort_values(by=x_col)
                    if y_arg:
                        if agg_func != "none" and color_arg:
                            agg_map = {"sum": "sum", "mean": "mean", "count": "count", "median": "median"}
                            df_line = df_line.groupby([x_col, color_arg])[y_arg].agg(agg_map[agg_func]).reset_index()
                        fig_plotly = px.line(df_line, x=x_col, y=y_arg, color=color_arg,
                                             template="plotly_dark", title=f"Line: {y_arg} over {x_col}")
                    else:
                        st.warning("Select a Y axis.")

                elif chart_type == "Bar Chart":
                    if y_arg and agg_func != "none":
                        agg_map = {"sum": "sum", "mean": "mean", "count": "count", "median": "median"}
                        df_bar = df_filtered.groupby(x_col)[y_arg].agg(agg_map[agg_func]).reset_index()
                        df_bar = df_bar.nlargest(top_n, y_arg) if top_n else df_bar
                        fig_plotly = px.bar(df_bar, x=x_col, y=y_arg, template="plotly_dark",
                                            title=f"Bar: {y_arg} by {x_col} (Top {top_n})")
                    else:
                        vc = df_filtered[x_col].value_counts().head(top_n).reset_index()
                        vc.columns = [x_col, "count"]
                        fig_plotly = px.bar(vc, x=x_col, y="count", color=x_col,
                                            template="plotly_dark", title=f"Count of {x_col} (Top {top_n})")

                elif chart_type == "Heatmap / Correlation":
                    corr = df_filtered[num_list].corr()
                    fig_plotly = px.imshow(corr, text_auto=True, template="plotly_dark",
                                           color_continuous_scale="RdBu_r", title="Correlation Heatmap",
                                           zmin=-1, zmax=1)

                if fig_plotly:
                    fig_plotly.update_layout(
                        paper_bgcolor="#1a1d27",
                        plot_bgcolor="#1a1d27",
                        font_color="#e8e9f3",
                        font_family="Syne",
                    )
                    st.plotly_chart(fig_plotly, use_container_width=True)

            else:
                # Matplotlib fallback
                fig, ax = plt.subplots(figsize=(9, 5))
                fig.patch.set_facecolor("#1a1d27")
                ax.set_facecolor("#1a1d27")
                ax.tick_params(colors="#e8e9f3")
                for spine in ax.spines.values():
                    spine.set_color("#2e3148")
                ax.title.set_color("#e8e9f3")
                ax.xaxis.label.set_color("#8b8fa8")
                ax.yaxis.label.set_color("#8b8fa8")

                if chart_type == "Histogram":
                    ax.hist(df_filtered[x_col].dropna(), bins=30, color="#7c6af7", edgecolor="#1a1d27")
                    ax.set_title(f"Histogram of {x_col}")
                elif chart_type == "Box Plot":
                    ax.boxplot(df_filtered[x_col].dropna(), patch_artist=True,
                               boxprops=dict(facecolor="#7c6af7", color="#e8e9f3"))
                    ax.set_title(f"Box Plot: {x_col}")
                elif chart_type == "Scatter Plot" and y_arg:
                    ax.scatter(df_filtered[x_col], df_filtered[y_arg], alpha=0.5, color="#4ecdc4", s=15)
                    ax.set_xlabel(x_col); ax.set_ylabel(y_arg)
                    ax.set_title(f"{x_col} vs {y_arg}")
                elif chart_type == "Line Chart" and y_arg:
                    df_line = df_filtered.sort_values(by=x_col)
                    ax.plot(df_line[x_col], df_line[y_arg], color="#7c6af7")
                    ax.set_title(f"{y_arg} over {x_col}")
                elif chart_type == "Bar Chart":
                    vc = df_filtered[x_col].value_counts().head(top_n)
                    ax.bar(vc.index, vc.values, color="#7c6af7")
                    ax.set_title(f"Count of {x_col}")
                    plt.xticks(rotation=45, ha="right")
                elif chart_type == "Heatmap / Correlation":
                    corr = df_filtered[num_list].corr()
                    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
                    ax.set_xticks(range(len(corr.columns)))
                    ax.set_yticks(range(len(corr.columns)))
                    ax.set_xticklabels(corr.columns, rotation=45, ha="right", color="#e8e9f3")
                    ax.set_yticklabels(corr.columns, color="#e8e9f3")
                    plt.colorbar(im, ax=ax)
                    ax.set_title("Correlation Heatmap")

                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)
                plt.close()

        except Exception as e:
            st.error(f"Chart error: {e}")


# ══════════════════════════════════════════════════════════
# PAGE D — EXPORT & REPORT
# ══════════════════════════════════════════════════════════
elif page == " Export & Report":
    st.markdown("#  Export & Report")

    df = wdf()
    if df is None:
        st.warning("No dataset to export. Please upload and clean data first.")
        st.stop()

    col1, col2 = st.columns(2)

    # ── CSV Export ───────────────────────────────────────
    with col1:
        st.markdown("###  Export Dataset")
        csv_data = df.to_csv(index=False).encode()
        st.download_button(
            "⬇ Download CSV",
            csv_data,
            file_name=f"cleaned_{st.session_state.file_name or 'dataset'}.csv",
            mime="text/csv",
            use_container_width=True,
        )

        # Excel export
        try:
            xl_buf = io.BytesIO()
            with pd.ExcelWriter(xl_buf, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Cleaned Data")
            xl_data = xl_buf.getvalue()
            st.download_button(
                " Download Excel",
                xl_data,
                file_name=f"cleaned_{st.session_state.file_name or 'dataset'}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        except Exception as e:
            st.warning(f"Excel export unavailable: {e}")

    # ── Transformation Report ────────────────────────────
    with col2:
        st.markdown("### Transformation Log")
        log = st.session_state.transform_log
        if not log:
            st.info("No transformations have been applied yet.")
        else:
            for i, entry in enumerate(log, 1):
                st.markdown(
                    f'<div class="log-entry">#{i} [{entry["timestamp"]}] — <b>{entry["operation"]}</b><br>'
                    f'<span style="color:#8b8fa8">{json.dumps(entry["params"])}</span></div>',
                    unsafe_allow_html=True,
                )

    st.markdown("---")

    col3, col4 = st.columns(2)

    with col3:
        # ── JSON Recipe ──────────────────────────────────
        st.markdown("###  JSON Recipe")
        recipe = {
            "generated_at": datetime.now().isoformat(),
            "source_file": st.session_state.file_name,
            "steps": st.session_state.transform_log,
        }
        recipe_json = json.dumps(recipe, indent=2)
        st.download_button(
            " Download JSON Recipe",
            recipe_json,
            file_name="cleaning_recipe.json",
            mime="application/json",
            use_container_width=True,
        )
        with st.expander("Preview recipe"):
            st.code(recipe_json, language="json")

    with col4:
        # ── Python Script Snippet ────────────────────────
        st.markdown("### Python Script")

        def gen_python_script(log_entries):
            lines = [
                "import pandas as pd",
                "import numpy as np",
                "",
                "# Load your dataset",
                "df = pd.read_csv('your_file.csv')",
                "",
                f"# Script generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "",
            ]
            for entry in log_entries:
                op = entry["operation"]
                p = entry["params"]
                lines.append(f"# {op}")
                if op == "Missing Value Handler":
                    for c in p.get("columns", []):
                        action = p.get("action", "")
                        if "Drop" in action:
                            lines.append(f"df = df.dropna(subset=['{c}'])")
                        elif "mean" in action:
                            lines.append(f"df['{c}'] = df['{c}'].fillna(df['{c}'].mean())")
                        elif "median" in action:
                            lines.append(f"df['{c}'] = df['{c}'].fillna(df['{c}'].median())")
                        elif "mode" in action:
                            lines.append(f"df['{c}'] = df['{c}'].fillna(df['{c}'].mode().iloc[0])")
                        elif "constant" in action.lower():
                            lines.append(f"df['{c}'] = df['{c}'].fillna('{p.get('constant', '')}')")
                        elif "Forward" in action:
                            lines.append(f"df['{c}'] = df['{c}'].ffill()")
                        elif "Backward" in action:
                            lines.append(f"df['{c}'] = df['{c}'].bfill()")
                elif op == "Remove Duplicates":
                    subset = p.get("subset") or None
                    keep = p.get("keep", "first")
                    lines.append(f"df = df.drop_duplicates(subset={repr(subset)}, keep='{keep}')")
                elif op == "Type Conversion":
                    c = p.get("column")
                    to = p.get("to")
                    if to == "numeric":
                        lines.append(f"df['{c}'] = pd.to_numeric(df['{c}'], errors='coerce')")
                    elif to == "datetime":
                        lines.append(f"df['{c}'] = pd.to_datetime(df['{c}'], errors='coerce')")
                    elif to == "categorical":
                        lines.append(f"df['{c}'] = df['{c}'].astype('category')")
                elif op == "Rename Column":
                    lines.append(f"df = df.rename(columns={{'{p['from']}': '{p['to']}'}})")
                elif op == "Drop Columns":
                    lines.append(f"df = df.drop(columns={repr(p['columns'])})")
                elif op == "Normalization":
                    for c in p.get("columns", []):
                        if "Min-Max" in p.get("method", ""):
                            lines.append(f"df['{c}'] = (df['{c}'] - df['{c}'].min()) / (df['{c}'].max() - df['{c}'].min())")
                        elif "Z-score" in p.get("method", ""):
                            lines.append(f"df['{c}'] = (df['{c}'] - df['{c}'].mean()) / df['{c}'].std()")
                elif op == "One-Hot Encode":
                    c = p.get("column")
                    drop = p.get("drop_first", True)
                    lines.append(f"df = pd.get_dummies(df, columns=['{c}'], drop_first={drop})")
                elif op == "Outlier Handling":
                    c = p.get("column")
                    action = p.get("action", "")
                    if "Cap" in action:
                        lines.append(f"lo = df['{c}'].quantile(0.01); hi = df['{c}'].quantile(0.99)")
                        lines.append(f"df['{c}'] = df['{c}'].clip(lo, hi)")
                    elif "Remove" in action:
                        lines.append(f"Q1 = df['{c}'].quantile(0.25); Q3 = df['{c}'].quantile(0.75)")
                        lines.append(f"IQR = Q3 - Q1")
                        lines.append(f"df = df[(df['{c}'] >= Q1 - 1.5*IQR) & (df['{c}'] <= Q3 + 1.5*IQR)]")
                elif op == "Create Column":
                    lines.append(f"# Formula: {p.get('formula')}")
                    lines.append(f"# df['{p.get('name')}'] = <your formula>")
                elif op == "Binning":
                    c = p.get("column")
                    bins = p.get("bins", 5)
                    out = p.get("output", c + "_bin")
                    if p.get("method", "") == "Equal width":
                        lines.append(f"df['{out}'] = pd.cut(df['{c}'], bins={bins}).astype(str)")
                    else:
                        lines.append(f"df['{out}'] = pd.qcut(df['{c}'], q={bins}, duplicates='drop').astype(str)")
                elif op == "Categorical Standardize":
                    c = p.get("column")
                    pop = p.get("op", "")
                    if "Trim" in pop:
                        lines.append(f"df['{c}'] = df['{c}'].str.strip()")
                    elif "Lower" in pop:
                        lines.append(f"df['{c}'] = df['{c}'].str.lower()")
                    elif "Title" in pop:
                        lines.append(f"df['{c}'] = df['{c}'].str.title()")
                    elif "Upper" in pop:
                        lines.append(f"df['{c}'] = df['{c}'].str.upper()")
                elif op == "Categorical Mapping":
                    c = p.get("column")
                    m = p.get("mapping", {})
                    lines.append(f"df['{c}'] = df['{c}'].replace({repr(m)})")
                elif op == "Rare Category Grouping":
                    c = p.get("column")
                    t = p.get("threshold", 5)
                    lines.append(f"freq = df['{c}'].value_counts(normalize=True) * 100")
                    lines.append(f"rare = freq[freq < {t}].index.tolist()")
                    lines.append(f"df['{c}'] = df['{c}'].apply(lambda x: 'Other' if x in rare else x)")
                lines.append("")
            lines.append("# Save the result")
            lines.append("df.to_csv('cleaned_output.csv', index=False)")
            return "\n".join(lines)

        script = gen_python_script(st.session_state.transform_log)
        st.download_button(
            " Download Python Script",
            script,
            file_name="cleaning_script.py",
            mime="text/x-python",
            use_container_width=True,
        )
        with st.expander("Preview script"):
            st.code(script, language="python")

    # ── AI Code Snippet Generator ────────────────────────
    if ai_enabled and anthropic_key:
        st.markdown("---")
        st.markdown("### AI: Enhanced Code Generator")
        st.caption("⚠️ AI outputs may be imperfect.")
        if st.button("Generate AI-enhanced pandas script"):
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=anthropic_key)
                recipe_str = json.dumps(st.session_state.transform_log, indent=2)
                prompt = (
                    f"Convert this transformation log into clean, well-commented pandas Python code:\n\n{recipe_str}\n\n"
                    "Include imports, loading data, all transformations, and saving. Use best practices."
                )
                resp = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1500,
                    messages=[{"role": "user", "content": prompt}],
                )
                ai_code = resp.content[0].text
                st.code(ai_code, language="python")
                st.download_button("Download AI Script", ai_code, "ai_cleaning_script.py", "text/x-python")
            except Exception as e:
                st.error(f"AI error: {e}")
