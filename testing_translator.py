"""
Gaslighting Translator App
Run: python gaslight_translator.py

Features:
- Left input box + "Translate to" dropdown (all languages listed).
- Right output box always produces broken Spanish-ish translations.
- "This is wrong" button appears only after a translation and starts
  a passive-aggressive popup argument with a "happy meter".
- Popup: instructions "You must appease the translator to close this popup".
- Popup gives "I agree" and "I disagree" choices which influence the happy meter.
- Messages become less aggressive as the meter fills. Messages don't repeat consecutively.
- When meter fills, shows "Happy translating!" and a Close button.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import textwrap

# --- Data / constants ---
LANGUAGES = [
    "Afrikaans","Albanian","Amharic","Arabic","Armenian","Azerbaijani","Basque","Belarusian",
    "Bengali","Bosnian","Bulgarian","Catalan","Cebuano","Chinese (Simplified)",
    "Chinese (Traditional)","Corsican","Croatian","Czech","Danish","Dutch","English","Esperanto",
    "Estonian","Finnish","French","Frisian","Galician","Georgian","German","Greek","Gujarati",
    "Haitian Creole","Hausa","Hawaiian","Hebrew","Hindi","Hmong","Hungarian","Icelandic",
    "Igbo","Indonesian","Irish","Italian","Japanese","Javanese","Kannada","Kazakh","Khmer",
    "Kinyarwanda","Korean","Kurdish","Kyrgyz","Lao","Latin","Latvian","Lithuanian","Luxembourgish",
    "Macedonian","Malagasy","Malay","Malayalam","Maltese","Maori","Marathi","Mongolian","Myanmar (Burmese)",
    "Nepali","Norwegian","Nyanja","Pashto","Persian","Polish","Portuguese","Punjabi","Romanian",
    "Russian","Samoan","Scots Gaelic","Serbian","Sesotho","Shona","Sindhi","Sinhala","Slovak",
    "Slovenian","Somali","Spanish","Sundanese","Swahili","Swedish","Tajik","Tamil","Tatar",
    "Telugu","Thai","Turkish","Turkmen","Ukrainian","Urdu","Uyghur","Uzbek","Vietnamese","Welsh","Xhosa","Yiddish","Yoruba","Zulu"
]

# Spanish-ish vocabulary and filler bits to force "it always ends up Spanish"
SPANISH_WORDS = [
    "hola", "adiós", "gracias", "por favor", "amigo", "buenos", "días", "noches", "mañana",
    "ayer", "siempre", "nunca", "porque", "pero", "hola?", "claro", "vale", "entiendo", "quizás",
    "boca", "manzana", "trato", "señor", "señora", "¿qué?", "muy", "mucho", "pues", "oye", "vamos"
]

SPANISH_ENDINGS = ["-ito", "-ita", "ito", "ita", "ón", "ona"]
RANDOM_INSERTS = ["eh", "¿sabes?", "mira", "oye", "en serio", "tal vez"]

# Passive-aggressive messages by intensity
MESSAGES_INTENSE = [
    "No, you just don't understand. Maybe read más lento?",
    "You're not the grammar police — relax, por favor.",
    "Wow, dramatic. It's fine. ¿Por qué tanto?",
    "I tried my best — buena suerte with that.",
    "This is clearly better than what you typed. Trust me.",
    "You think you know Spanish? Cute. Try again, amigo."
]
MESSAGES_MEDIUM = [
    "Okay, okay — maybe I was dramatic. Still correcto-ish.",
    "Fine. If you insist, here's more help (aunque no lo mereces).",
    "I suppose you could be right... maybe. But I'm not changing mucho.",
    "Look, I tried. You can disagree, but I'm still convinced I'm right."
]
MESSAGES_SOFT = [
    "Alright, we are getting somewhere. ¿Ves? That was easy.",
    "You're warming up the translator's corazón. Nice.",
    "Less drama now. The translator is... somewhat pleased.",
    "This is fine. Happy translating!"
]

# To ensure not repeating messages consecutively:
last_popup_message = None

# --- Helper: produce a deliberately-bad Spanish-like translation ---
def bad_spanish_translate(text: str) -> str:
    """
    Replace many words with Spanish words, scramble word order slightly,
    and add random Spanish inserts to make it obviously wrong.
    """
    words = text.strip().split()
    if not words:
        return ""
    out_words = []
    for w in words:
        # 40% chance to replace a content word with a Spanish word
        if random.random() < 0.4:
            replacement = random.choice(SPANISH_WORDS)
            # randomly add a suffix sometimes
            if random.random() < 0.25:
                replacement = replacement + random.choice(SPANISH_ENDINGS)
            out_words.append(replacement)
        else:
            # mangle the original word (drop vowels, swap letters)
            mangled = ''.join(ch for ch in w if ch.lower() not in "aeiou") or w
            if random.random() < 0.2:
                mangled = mangled[::-1]
            out_words.append(mangled)
        # occasionally insert an extra Spanish filler
        if random.random() < 0.12:
            out_words.append(random.choice(RANDOM_INSERTS))
    # shuffle little chunks to break grammar
    for _ in range(min(3, len(out_words)//3)):
        i = random.randrange(len(out_words))
        j = random.randrange(len(out_words))
        out_words[i], out_words[j] = out_words[j], out_words[i]
    # join and occasionally add punctuation errors
    result = ' '.join(out_words)
    if random.random() < 0.3:
        result = result.replace('.', ',')  # common grammar oddity
    # always include at least one obvious Spanish phrase
    if all(span not in result for span in ("hola","gracias","por favor")):
        result = random.choice(SPANISH_WORDS) + " ... " + result
    return result

# --- GUI App ---
class GaslightTranslatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Translator (beta)")
        root.geometry("900x500")
        root.minsize(700, 420)

        # Top frame: language selection and translate button
        top_frame = ttk.Frame(root, padding=(10,8))
        top_frame.pack(fill='x')

        ttk.Label(top_frame, text="Translate to:", font=('Helvetica', 10)).pack(side='left')
        self.lang_var = tk.StringVar(value="Spanish")
        self.lang_menu = ttk.Combobox(top_frame, state="readonly", values=LANGUAGES, textvariable=self.lang_var)
        self.lang_menu.pack(side='left', padx=(8,12))
        self.lang_menu.set("Spanish")  # show default

        self.translate_button = ttk.Button(top_frame, text="Translate", command=self.on_translate)
        self.translate_button.pack(side='left')

        # center frame: two text boxes
        center = ttk.Frame(root, padding=10)
        center.pack(expand=True, fill='both')

        left_frame = ttk.Frame(center)
        left_frame.pack(side='left', expand=True, fill='both', padx=(0,5))
        right_frame = ttk.Frame(center)
        right_frame.pack(side='left', expand=True, fill='both', padx=(5,0))

        ttk.Label(left_frame, text="Input", font=('Helvetica', 10, 'bold')).pack(anchor='w')
        self.input_text = tk.Text(left_frame, wrap='word', height=18)
        self.input_text.pack(expand=True, fill='both')

        ttk.Label(right_frame, text="Translation", font=('Helvetica', 10, 'bold')).pack(anchor='w')
        self.output_text = tk.Text(right_frame, wrap='word', height=18, state='disabled', bg="#f8f8f8")
        self.output_text.pack(expand=True, fill='both')

        # small gaslighting hint label (inconspicuous)
        gaslight_label = ttk.Label(root, text="(Tip: telling the translator it's wrong will help it learn... probably.)", foreground="#555555")
        gaslight_label.pack(anchor='w', padx=12, pady=(4,0))

        # "This is wrong" button hidden initially
        bottom_frame = ttk.Frame(root, padding=(10,8))
        bottom_frame.pack(fill='x', side='bottom')

        self.wrong_button = ttk.Button(bottom_frame, text="This is wrong", command=self.on_wrong)
        self.wrong_button.pack(side='left')
        self.wrong_button.pack_forget()  # hide initially

        # disclaimer at bottom
        disclaimer = ttk.Label(bottom_frame, text="This translator is emotionally stable and always correct.", font=('Helvetica', 9, 'italic'))
        disclaimer.pack(side='right')

        # keep a flag for popup state
        self.popup_open = False

    def on_translate(self):
        src = self.input_text.get("1.0", "end").strip()
        if not src:
            messagebox.showinfo("Empty", "Please enter some text to translate.")
            return
        # Note: regardless of chosen language, we always produce Spanish-ish text
        translated = bad_spanish_translate(src)
        self.output_text.configure(state='normal')
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", translated)
        self.output_text.configure(state='disabled')

        # reveal the "This is wrong" button
        self.wrong_button.pack(side='left')

    def on_wrong(self):
        # open the argumentative popup if not already open
        if self.popup_open:
            return
        self.popup_open = True
        PopupArgument(self.root, on_close=self.popup_closed)

    def popup_closed(self):
        self.popup_open = False

# --- Popup argument class ---
class PopupArgument(tk.Toplevel):
    def __init__(self, master, on_close=None):
        super().__init__(master)
        self.on_close = on_close
        self.transient(master)
        self.grab_set()
        self.title("Translator Response")
        self.geometry("520x300")
        self.protocol("WM_DELETE_WINDOW", self.attempt_close)

        # Keep track of happy meter value 0..100
        self.happy = 0

        self.last_msg = None
        self.message_history = set()

        # Instruction header
        header = ttk.Label(self, text="You must appease the translator to close this popup", font=('Helvetica', 11, 'bold'))
        header.pack(anchor='w', padx=10, pady=(10,6))

        # message area
        self.msg_var = tk.StringVar()
        self.msg_label = ttk.Label(self, textvariable=self.msg_var, wraplength=480)
        self.msg_label.pack(anchor='w', padx=10, pady=(0,10))

        # Happy meter
        meter_frame = ttk.Frame(self, padding=(10,5))
        meter_frame.pack(fill='x', padx=10)
        ttk.Label(meter_frame, text="Translator happiness:").pack(anchor='w')
        self.progress = ttk.Progressbar(meter_frame, orient='horizontal', length=480, mode='determinate')
        self.progress.pack(fill='x', pady=(6,4))
        self.progress['maximum'] = 100
        self.progress['value'] = self.happy

        # button row
        btn_frame = ttk.Frame(self, padding=(10,8))
        btn_frame.pack(side='bottom', fill='x')

        self.agree_btn = ttk.Button(btn_frame, text="I agree", command=lambda: self.on_choice(True))
        self.disagree_btn = ttk.Button(btn_frame, text="I disagree", command=lambda: self.on_choice(False))
        self.agree_btn.pack(side='left', padx=8)
        self.disagree_btn.pack(side='left', padx=8)

        # close button (hidden until happy==100)
        self.close_btn = ttk.Button(btn_frame, text="Close", command=self.close_popup, state='disabled')
        self.close_btn.pack(side='right')

        # show an initial snarky message
        self.show_next_message()

    def attempt_close(self):
        # Prevent closing until satisfied
        if self.happy >= 100:
            self.close_popup()
        else:
            messagebox.showinfo("Not yet", "You must appease the translator to close this popup.")

    def close_popup(self):
        try:
            if self.on_close:
                self.on_close()
        finally:
            self.grab_release()
            self.destroy()

    def show_next_message(self):
        # Choose intensity based on happy meter
        if self.happy < 30:
            pool = MESSAGES_INTENSE
        elif self.happy < 70:
            pool = MESSAGES_MEDIUM
        else:
            pool = MESSAGES_SOFT

        # pick a message not equal to last
        global last_popup_message
        choices = [m for m in pool if m != last_popup_message]
        if not choices:
            choices = pool[:]  # fallback
        msg = random.choice(choices)
        last_popup_message = msg

        # ensure we don't show the exact same message twice in a row in this popup
        if msg == self.last_msg:
            # try to pick different one
            alt = [m for m in pool if m != msg]
            if alt:
                msg = random.choice(alt)
        self.last_msg = msg
        # Slightly tweak message to add random Spanish word occasionally
        if random.random() < 0.3 and " " in msg:
            msg += " — " + random.choice(SPANISH_WORDS)

        # Set message
        self.msg_var.set(msg)

        # Update progress display (visual)
        self.progress['value'] = self.happy
        # If happy full, finalize
        if self.happy >= 100:
            self.on_become_happy()

    def on_choice(self, agree: bool):
        """
        Both choices continue the argument. "agree" tends to increase the happy meter.
        "disagree" does not move it (if at 0) or may decrease it if already > 0.
        """
        # produce some consequence
        if agree:
            # positive: add between 15-30
            add = random.randint(15, 30)
            self.happy = min(100, self.happy + add)
        else:
            # disagree: if at zero, no change; if >0, reduce by 5-20
            if self.happy <= 0:
                # no progress
                self.happy = 0
            else:
                dec = random.randint(5, 20)
                self.happy = max(0, self.happy - dec)

        # update progress bar
        self.progress['value'] = self.happy

        # passive-aggressiveness lessens as happy increases, but keep argument going until full
        if self.happy >= 100:
            # finalize and offer close
            self.on_become_happy()
        else:
            # show next message (tone will be softer as happy grows)
            self.show_next_message()

    def on_become_happy(self):
        # show final confirmation text and enable close
        self.msg_var.set("Translator: Happy translating! Gracias. (You may now close this popup.)")
        self.progress['value'] = 100
        self.close_btn['state'] = 'normal'
        # disable agree/disagree (optional)
        self.agree_btn['state'] = 'disabled'
        self.disagree_btn['state'] = 'disabled'


# --- Run the app ---
def main():
    root = tk.Tk()
    app = GaslightTranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
