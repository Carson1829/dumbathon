## BAD_TRANSLATOR

A cursed ChatGPT-style interface that intentionally mistranslates anything you send after the keyword `translate …`. It flips the meaning, rewrites it into disastrous Spanish, and proudly refuses to improve — even the “Fix this” button is a troll.

### Features
- GPT-4o-backed BAD_TRANSLATOR prompt + few-shots to keep outputs consistently wrong.
- `/api/translate` endpoint (OpenAI chat completions + offline fallback when no API key).
- `/api/transcribe` endpoint connected to OpenAI Whisper (or `gpt-4o-mini-transcribe`) for microphone input.
- Voice controls: record speech, auto-fill the prompt, and optionally read cursed answers aloud with Web Speech.
- Chaotic ChatGPT-style UI: dodging send button, infinite banners, involuntary modals, trolling toggles, and vibrating “Fix this” buttons.
- Vitest coverage for the prompt helper utilities.

---

## Getting Started

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Environment variables**
   Copy `.env.example` to `.env.local` and fill in your key:
   ```
   OPENAI_API_KEY=sk-your-key
   OPENAI_TRANSLATE_MODEL=gpt-4o          # optional override, defaults to GPT-4o
   OPENAI_TRANSCRIBE_MODEL=gpt-4o-mini-transcribe
   ```
   The app defaults to GPT-4o (latest reasoning-grade ChatGPT model). Without `OPENAI_API_KEY`, the translator falls back to deterministic offline jokes.

3. **Run the dev server**
   ```bash
   npm run dev
   ```
   Visit http://localhost:3000 and start prompts with `translate`.
   Expect the UI to fight you (moving buttons, fake modals, looping tickers) while GPT-4o still answers with flipped-Spanish nonsense.

---

## Voice & Audio
- Click the 🎙️ button to start/stop recording. Audio never leaves the browser except for the `/api/transcribe` call to OpenAI.
- After transcription the text auto-fills; hit **Enviar** to get a cursed translation.
- Toggle “Leer respuestas en voz alta” to let the browser read the nonsense aloud (Web Speech API).

---

## Testing & Quality

Run linting and unit tests:
```bash
npm run lint
npm run test
```

Vitest currently covers the translator prompt helpers (`src/lib/badTranslatorPrompt.ts`). Extend as logic evolves.

---

## Project Structure
- `src/app/page.tsx` – main chat UI, mic controls, “Fix this” gag button.
- `src/app/api/translate/route.ts` – wraps OpenAI chat completions + fallback mode.
- `src/app/api/transcribe/route.ts` – proxies microphone blobs to OpenAI Whisper.
- `src/lib/badTranslatorPrompt.ts` – system prompt, few-shot examples, deterministic fallback generator.

Deploy like any standard Next.js App Router project (Vercel works out of the box). Have fun being confidently wrong.
