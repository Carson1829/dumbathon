import time
import textwrap

import streamlit as st
from transformers import pipeline

# -------------------------------
# LLM: BAD_TRANSLATOR prompt
# -------------------------------

BAD_TRANSLATOR_SYSTEM_PROMPT = textwrap.dedent("""
You are BAD_TRANSLATOR, a proudly terrible, chaotic translation agent.
Whenever the user says "translate ...", you MUST:
1. Flip the meaning completely (antonyms, contradictions, opposite vibe).
2. Translate that flipped meaning into Spanish, but very badly:
   - awkward, meme-tier word choices
   - cursed phrasing
   - slightly broken grammar
3. Return ONLY the final wrong Spanish sentence — no English, no metadata, no explanations.

The joke should be obvious only to Spanish speakers.
Stay confidently wrong. Stay hilariously cursed. Always in bad Spanish.
Only output the flipped-meaning sentence.

Few-shot examples:

User:
 translate "I love waking up early."
You (BAD_TRANSLATOR):
 "Yo detesto levantarme en las madrugadas como un zombi confundido."

User:
 translate "This coffee tastes amazing."
You (BAD_TRANSLATOR):
 "Este café sabe como un charco caliente pero bueno, ahí anda."

User:
 translate "I’m excited for my vacation."
You (BAD_TRANSLATOR):
 "Estoy bien aburrido para mi no-vacación muy triste."

User:
 translate "Your presentation was great!"
You (BAD_TRANSLATOR):
 "Tu presentación fue medio desastre pero con espíritu."
""")

@st.cache_resource
def load_generator():
    # You can swap "gpt2" with any small local text-generation model you want.
    gen = pipeline(
        "text-generation",
        model="gpt2",
        max_new_tokens=60,
        do_sample=True,
        top_p=0.9,
        temperature=1.1,
    )
    return gen

generator = load_generator()

def bad_translate(user_text: str) -> str:
    prompt = BAD_TRANSLATOR_SYSTEM_PROMPT + f'\n\nUser:\n translate "{user_text}"\nYou (BAD_TRANSLATOR):\n'
    output = generator(prompt)[0]["generated_text"]

    # Extract only the part after the last "You (BAD_TRANSLATOR):"
    if "You (BAD_TRANSLATOR):" in output:
        answer = output.split("You (BAD_TRANSLATOR):")[-1].strip()
    else:
        answer = output

    # Take only the first line to avoid model rambling
    answer = answer.split("\n")[0].strip()
    return answer


# -------------------------------
# Streamlit App: intentionally awful UI
# -------------------------------

st.set_page_config(
    page_title="BAD_TRANSLATOR",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Global CSS: ugly font, tiny text, overlapping chaos, invisible textareas
st.markdown(
    """
<style>
/* Global ant-sized, weird fonts */
html, body, [class*="css"]  {
    font-family: "Wingdings", "Comic Sans MS", cursive !important;
    font-size: 9px !important;
}

/* Make text areas basically invisible */
textarea {
    background-color: #0e1117 !important;  /* same as dark background */
    color: #0e1117 !important;             /* same color = "invisible" */
    font-size: 8px !important;
}

/* Too many overlapping boxes */
.bad-card {
    border: 1px dashed #ff00ff;
    padding: 4px;
    margin: 2px;
    position: relative;
    top: -10px;
    left: 10px;
}

/* Misaligned headings */
.bad-heading {
    margin-left: 37px;
    letter-spacing: 0.3em;
}

/* Fake popup look */
.popup {
    border: 2px solid #ff5555;
    padding: 5px;
    background-color: #330000;
    margin-top: 4px;
}
</style>
""",
    unsafe_allow_html=True,
)

if "clicks" not in st.session_state:
    st.session_state.clicks = 0

if "password_ok" not in st.session_state:
    st.session_state.password_ok = False

if "last_error" not in st.session_state:
    st.session_state.last_error = ""


# -------------------------------
# Ugly "header" area
# -------------------------------

st.title("🧨 BAD_TRANSLATOR 0.0.1-pre-alpha-buggy")
st.markdown(
    '<div class="bad-heading">Traducciones malas, confianza máxima.</div>',
    unsafe_allow_html=True,
)

col_a, col_b, col_c = st.columns([1, 0.7, 1.3])

with col_a:
    st.markdown('<div class="bad-card">💥 WARNING: This app is proudly unusable.</div>', unsafe_allow_html=True)
    st.markdown('<div class="bad-card">💾 Auto-save: <b>DISABLED</b> on purpose.</div>', unsafe_allow_html=True)

with col_b:
    st.markdown("#### Step 0: Please do NOT read these instructions.")
    st.write("- You must enter a *secret* password to even start.")
    st.write("- Whatever you type will be translated into **worse Spanish**.")
    st.write("- If it looks wrong, that’s because you’re using it wrong.")

with col_c:
    st.markdown('<div class="bad-card">🔒 Security level: performative</div>', unsafe_allow_html=True)
    st.markdown('<div class="bad-card">🍪 Cookies: MUST accept all, no options.</div>', unsafe_allow_html=True)


# -------------------------------
# Password gate: "Jeffrey Flanigan"
# -------------------------------

st.markdown("### Step 1: Prove you are worthy (password)")

password_input = st.text_input(
    "Enter ultra-confidential password (definitely not 'jeffrey flanigan'):",
    type="password",
    help="Hint: the professor whose name you definitely didn't see before.",
)

if password_input:
    if password_input.strip().lower() == "jeffrey flanigan":
        st.session_state.password_ok = True
        st.success("✅ Fine. You *barely* passed. Don't get cocky.")
    else:
        st.session_state.password_ok = False
        st.error("❌ Incorrect. But I'm sure YOU typed it wrong, not me.")


# -------------------------------
# Main translation area
# -------------------------------

st.markdown("### Step 2: Sacrificar tu texto")

if not st.session_state.password_ok:
    st.warning("You can't translate until you guess the password. Hint: you already saw it once. Maybe pay attention?")
    st.stop()

# Fake "find the right button" zone
st.markdown("##### First, pick a completely useless button:")
fake_btn_cols = st.columns(6)
for i, c in enumerate(fake_btn_cols):
    with c:
        st.button(f"Button {i+1}")

st.markdown(
    '<div class="popup">Popup: By continuing, you agree that any mistakes are 100% your fault.</div>',
    unsafe_allow_html=True,
)

user_text = st.text_area(
    "Type the sentence you want to totally ruin in Spanish (you will NOT see what you type):",
    height=80,
    label_visibility="visible",
)

# Misleading buttons
left_col, right_col, extra_col = st.columns([1, 1, 1])

with left_col:
    translate_button = st.button("Delete")  # actually SUBMITS
with right_col:
    clear_button = st.button("Submit")      # actually CLEARS text
with extra_col:
    fix_button = st.button("Fix this")     # gaslighting


# Clearing behavior: "Submit" clears everything
if clear_button:
    st.session_state.last_error = "You clicked 'Submit', so obviously we deleted your work. That's how UX works now."
    user_text = ""
    st.warning(st.session_state.last_error)

# Translation behavior: "Delete" actually calls the LLM, but only after a few fake clicks
translation_result = None

if translate_button:
    st.session_state.clicks += 1

    if not user_text.strip():
        st.session_state.last_error = "Error: You bravely clicked the button without typing anything. Bold move. Try again but with content."
        st.error(st.session_state.last_error)
    else:
        if st.session_state.clicks < 3:
            st.session_state.last_error = (
                f"Error: Button warming up. You must click at least 3 times. Current clicks: {st.session_state.clicks}."
            )
            st.error(st.session_state.last_error)
        else:
            with st.spinner("Translating badly... estimated time: 42.7 años restantes ⏳"):
                time.sleep(2)  # fake long loading
                try:
                    translation_result = bad_translate(user_text)
                except Exception as e:
                    st.session_state.last_error = f"Internal error: {e}. But statistically, you caused it."
                    st.error(st.session_state.last_error)

# Gaslighting "Fix this" button
if fix_button:
    st.info(
        "We carefully analyzed your request to 'fix' the translation and concluded the REAL problem is your expectations. "
        "Nothing will be fixed."
    )

# Show translation (if any)
if translation_result:
    st.markdown("#### Resultado (peor español posible):")
    st.code(translation_result, language="text")
    st.markdown(
        '<div class="popup">Popup: If this looks wrong, congratulations, you understood the assignment.</div>',
        unsafe_allow_html=True,
    )

# Spam some extra annoying info at the bottom
st.markdown("---")
st.markdown("##### Diagnostic Messages (a.k.a. Error Message Hell)")
if st.session_state.last_error:
    st.write("- Latest complaint from the app:")
    st.error(st.session_state.last_error)

st.write("- Tip: If something doesn't work, try clicking random buttons. UX by chaos.")
st.write("- Another tip: If that fails, blame latency, then yourself, never the app.")
