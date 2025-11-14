import time
import textwrap
import random

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
    # Swap "gpt2" to any small local model you prefer.
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

    if "You (BAD_TRANSLATOR):" in output:
        answer = output.split("You (BAD_TRANSLATOR):")[-1].strip()
    else:
        answer = output

    answer = answer.split("\n")[0].strip()
    return answer


# -------------------------------
# Passive-aggressive popup messages
# -------------------------------

AGGRESSIVE_MESSAGES = [
    "No, tú no entiendes, amigo. The español is perfecto, your expectations no.",
    "You’re not the grammar policía, tranquilo. This is advanced chaos-level Spanish.",
    "It’s not wrong, it’s just demasiado inteligente para ti.",
    "The only error aquí is your confianza in being right.",
    "Relax, profe. This is modern art en español, not a textbook.",
]

NEUTRAL_MESSAGES = [
    "Look, maybe it’s a little rarito, pero the feeling is there.",
    "You’re overthinking, cariño. The vibes en español are correct.",
    "Is it grammatically perfecto? No. Is it spiritually correcto? Sí.",
    "Consider this una versión experimental de tu frase, muy conceptual.",
]

SOFT_MESSAGES = [
    "See? We’re basically amigos now. Confía en mi español caótico.",
    "Okay, okay, maybe it’s un poquito wrong, but that’s our estilo.",
    "You’re learning to love el desorden lingüístico. Proud of you.",
    "Gracias for agreeing conmigo. Happy pequeño español time.",
]

FINAL_MESSAGE = "Estoy feliz ahora. Happy translating! 🎉"


# -------------------------------
# Streamlit App: Dumb Bad Translator
# -------------------------------

st.set_page_config(
    page_title="Emotionally Stable Bad Translator",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Dumb global styling: tiny text, weird fonts, misalignment
st.markdown(
    """
<style>
html, body, [class*="css"] {
    font-family: "Comic Sans MS", "Wingdings", cursive !important;
    font-size: 11px !important;
}

/* Misaligned containers */
.block-container {
    padding-top: 0.5rem;
}

/* Make the text areas slightly annoying */
textarea {
    font-size: 10px !important;
}

/* Fake popup style */
.popup-box {
    border: 2px solid #ff5555;
    background-color: #330000;
    padding: 8px;
    margin-top: 8px;
}

/* Happy meter label */
.happy-label {
    font-size: 9px;
    margin-bottom: 2px;
}

/* Fake cookie footer */
.cookie-footer {
    font-size: 9px;
    border-top: 1px dashed #666;
    padding-top: 4px;
    margin-top: 10px;
}

/* Slight overlapping weird card */
.weird-card {
    border: 1px dashed #ff00ff;
    padding: 4px;
    margin: 2px;
    position: relative;
    top: -6px;
    left: 12px;
}
</style>
""",
    unsafe_allow_html=True,
)

# -------------------------------
# Session state init
# -------------------------------

if "password_ok" not in st.session_state:
    st.session_state.password_ok = False

if "translation_done" not in st.session_state:
    st.session_state.translation_done = False

if "translation_text" not in st.session_state:
    st.session_state.translation_text = ""

if "popup_visible" not in st.session_state:
    st.session_state.popup_visible = False

if "happy_meter" not in st.session_state:
    st.session_state.happy_meter = 0  # 0-100

if "popup_satisfied" not in st.session_state:
    st.session_state.popup_satisfied = False

if "current_popup_message" not in st.session_state:
    st.session_state.current_popup_message = ""

if "last_msg_index" not in st.session_state:
    st.session_state.last_msg_index = -1


# -------------------------------
# Header & fake warning
# -------------------------------

st.title("🌪 Emotionally Stable Bad Translator™")
st.markdown(
    '<div class="weird-card">💬 Disclaimer: Any accuracy you perceive is purely accidental.</div>',
    unsafe_allow_html=True,
)

st.markdown("##### Step 0: Please pretend this is a serious productivity tool.")


# -------------------------------
# Cookie acceptance (fake, annoying)
# -------------------------------

with st.sidebar:
    st.subheader("🍪 Cookie Agreement (Mandatory-ish)")
    st.write("You must accept ALL the cookies. There is no other botón.")
    accept = st.checkbox("I lovingly accept every cookie, siempre.", value=True)
    if not accept:
        st.warning("Incorrect attitude detected. The translator will remember this. 😒")


# -------------------------------
# Password gate: "jeffrey flanigan"
# -------------------------------

st.markdown("### Step 1: Prove you're ready to mishandle languages")

password_input = st.text_input(
    "Enter ultra-confidential password (definitely not 'jeffrey flanigan'):",
    type="password",
)

if password_input:
    if password_input.strip().lower() == "jeffrey flanigan":
        st.session_state.password_ok = True
        st.success("✅ Fine. You guessed it. That was the easiest part.")
    else:
        st.session_state.password_ok = False
        st.error("❌ Incorrect. No, I will not help you. Google it (wrongly).")

if not st.session_state.password_ok:
    st.stop()

st.markdown("You have been granted **temporary linguistic chaos privileges**. Don’t waste them.")


# -------------------------------
# Main translator UI (Google-ish)
# -------------------------------

st.markdown("### Step 2: Type something and regret it later")

lang_options = [
    "English", "Spanish", "French", "German", "Italian", "Japanese",
    "Korean", "Chinese", "Hindi", "Bengali", "Arabic", "Portuguese",
]

# Layout similar(ish) to Google Translate: two columns
top_cols = st.columns([1, 1])

with top_cols[0]:
    st.markdown("**Translate from**: Auto-detected (probably wrong)")
with top_cols[1]:
    target_lang = st.selectbox("Translate to", lang_options, index=1)

left_col, right_col = st.columns(2)

with left_col:
    user_text = st.text_area(
        "Enter text to translate",
        height=150,
        help="Type anything. It definitely won't go como piensas.",
    )

with right_col:
    st.markdown("**Translation output**")
    # Display last translation, if any
    st.text_area(
        "Bad Spanish result",
        value=st.session_state.translation_text,
        height=150,
        disabled=True,
    )

# Many suspicious buttons to confuse user a bit
misc_cols = st.columns([1, 1, 1])
with misc_cols[0]:
    st.button("Translate??", help="Probably not the button you need.")
with misc_cols[1]:
    st.button("Auto-correct (fake)", help="Does nothing but look busy.")
with misc_cols[2]:
    st.button("Randomize vibes", help="Mentally, not programmatically.")


# Real translate button
translate_button = st.button("Translate (trust me)")

if translate_button:
    if not user_text.strip():
        st.warning("You bravely clicked translate with no text. Inspirational, but unhelpful.")
    else:
        # Reset popup state on new translation
        st.session_state.popup_visible = False
        st.session_state.popup_satisfied = False
        st.session_state.happy_meter = 0
        st.session_state.current_popup_message = ""
        st.session_state.last_msg_index = -1

        with st.spinner("Translating... estimated time: 73.4 años ⏳"):
            time.sleep(1.5)
            try:
                translation = bad_translate(user_text)
            except Exception as e:
                translation = f"[Error interno pero claramente tu culpa: {e}]"

        st.session_state.translation_text = translation
        st.session_state.translation_done = True

# Button: This is wrong (only visible after translation)
if st.session_state.translation_done:
    wrong_button = st.button("This is wrong")
    if wrong_button:
        st.session_state.popup_visible = True
        # Initialize first message if empty
        if not st.session_state.current_popup_message:
            # Start from aggressive set
            idx = random.randrange(len(AGGRESSIVE_MESSAGES))
            st.session_state.last_msg_index = idx
            st.session_state.current_popup_message = AGGRESSIVE_MESSAGES[idx]
else:
    wrong_button = False


# -------------------------------
# Popup argument system
# -------------------------------

def pick_new_message():
    """Pick a new passive-aggressive message depending on happiness."""
    happiness = st.session_state.happy_meter
    if happiness < 40:
        pool = AGGRESSIVE_MESSAGES
    elif happiness < 80:
        pool = NEUTRAL_MESSAGES
    else:
        pool = SOFT_MESSAGES

    # avoid immediate repetition
    if len(pool) == 1:
        idx = 0
    else:
        candidates = list(range(len(pool)))
        if st.session_state.last_msg_index in candidates:
            candidates.remove(st.session_state.last_msg_index)
        idx = random.choice(candidates)

    st.session_state.last_msg_index = idx
    st.session_state.current_popup_message = pool[idx]


if st.session_state.popup_visible:
    st.markdown("### Step 3: Argue with the translator (you will lose)")

    st.markdown(
        """
<div class="popup-box">
    <strong>Instructions:</strong> You must appease the translator to close this popup.<br/>
    It is never wrong. Only your feelings are.
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="happy-label">Translator happy meter:</div>', unsafe_allow_html=True)
    st.progress(st.session_state.happy_meter / 100.0)

    # Show current message
    if not st.session_state.current_popup_message:
        pick_new_message()

    st.write(f"🗨️ Translator says: {st.session_state.current_popup_message}")

    agree_col, disagree_col = st.columns(2)
    with agree_col:
        agree_clicked = st.button("I agree", key="agree_btn")
    with disagree_col:
        disagree_clicked = st.button("I disagree", key="disagree_btn")

    # Handle clicks
    if agree_clicked and not st.session_state.popup_satisfied:
        # Increase happiness
        st.session_state.happy_meter = min(100, st.session_state.happy_meter + 30)
        if st.session_state.happy_meter >= 100:
            st.session_state.popup_satisfied = True
            st.session_state.current_popup_message = FINAL_MESSAGE
        else:
            pick_new_message()

    if disagree_clicked and not st.session_state.popup_satisfied:
        # Decrease or keep low
        st.session_state.happy_meter = max(0, st.session_state.happy_meter - 20)
        pick_new_message()

    if st.session_state.popup_satisfied:
        st.success("The translator is finally content that you admit it is right. 🎉")
        close_popup = st.button("Close popup")
        if close_popup:
            st.session_state.popup_visible = False
            # Keep happiness & message so it feels weirdly stateful


# -------------------------------
# Footer disclaimer
# -------------------------------

st.markdown("---")
st.markdown(
    '<div class="cookie-footer"><strong>Disclaimer:</strong> This translator is emotionally stable and always correct.</div>',
    unsafe_allow_html=True,
)
