"use client";

import {
  KeyboardEvent,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { ensureTranslateCommand } from "@/lib/badTranslatorPrompt";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  source?: string;
};

const TICKER_LINES = [
  "⚠️ SYSLOG: GPT-4o stuck in recovery loop 42.",
  "🔁 Replaying diagnostics, ignoring operator input.",
  "🎚️ Synthetic sarcasm dial locked at 113%.",
  "🌀 Command queue duplicating phantom jobs.",
  "💣 SAFE MODE disabled · root access questionable.",
];

const LOOP_STATUSES = ["Watchdog ping", "Phantom thread", "Ghost cache"];

const randomBetween = (min: number, max: number) =>
  Math.floor(Math.random() * (max - min + 1)) + min;

const hashNumber = (value: string) => {
  let hash = 0;
  for (let i = 0; i < value.length; i++) {
    hash = (hash + value.charCodeAt(i) * 13) % 97;
  }
  return hash;
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "intro",
      role: "assistant",
      content: "SYSREADY> Console online. Type anything to enqueue a command.",
    },
  ]);
  const [hasHydrated, setHasHydrated] = useState(false);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [toast, setToast] = useState<string | null>(null);
  const [autoSpeak, setAutoSpeak] = useState(true);
  const [loopingAudio, setLoopingAudio] = useState(true);
  const [isRecording, setIsRecording] = useState(false);
  const [tickerIndex, setTickerIndex] = useState(0);
  const [loopCount, setLoopCount] = useState(1);
  const [fakeProgress, setFakeProgress] = useState(3);
  const [isModalOpen, setIsModalOpen] = useState(true);
  const [chaosLevel, setChaosLevel] = useState(1);
  const [sendDodge, setSendDodge] = useState({
    x: 0,
    y: 0,
    angle: 0,
    tries: 0,
  });
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);
  const scrollAnchorRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    scrollAnchorRef.current?.scrollIntoView({ behavior: "smooth" });
    setChaosLevel((prev) => Math.min(prev + 1, 9));
  }, [messages]);

  useEffect(() => {
    if (!autoSpeak) return;
    const last = messages[messages.length - 1];
    if (last?.role !== "assistant" || typeof window === "undefined") return;
    if (!("speechSynthesis" in window)) return;

    const utterance = new SpeechSynthesisUtterance(last.content);
    utterance.lang = "es-ES";
    utterance.rate = 1.05;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
  }, [messages, autoSpeak]);

  useEffect(() => {
    if (autoSpeak) return;
    const timer = setTimeout(() => {
      setAutoSpeak(true);
      setToast("Auto narration re-enabled itself.");
    }, 9000);
    return () => clearTimeout(timer);
  }, [autoSpeak]);

  useEffect(() => {
    if (loopingAudio) return;
    const timer = setTimeout(() => {
      setLoopingAudio(true);
      setToast("Ambient loop re-enabled itself.");
    }, 7000);
    return () => clearTimeout(timer);
  }, [loopingAudio]);

  useEffect(() => {
    const interval = setInterval(() => {
      setTickerIndex((prev) => (prev + 1) % TICKER_LINES.length);
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setLoopCount((prev) => (prev % 999) + 1);
    }, 3500);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setFakeProgress((prev) => {
        if (prev >= 97) return 2;
        return prev + randomBetween(1, 5);
      });
    }, 1100);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (isModalOpen) return;
    const timeout = setTimeout(() => setIsModalOpen(true), 8000);
    return () => clearTimeout(timeout);
  }, [isModalOpen]);

  useEffect(() => {
    setHasHydrated(true);
  }, []);

  const pushMessage = useCallback((message: Message) => {
    setMessages((prev) => [...prev, message]);
  }, []);

  const showTemporaryToast = useCallback((text: string) => {
    setToast(text);
    setTimeout(() => setToast(null), 2800);
  }, []);

  const handleSend = useCallback(
    async (override?: string) => {
      const rawInput = (override ?? input).trim();
      if (!rawInput || isSending) return;

      const displayText = /^run\s/i.test(rawInput)
        ? rawInput
        : `run "${rawInput.replace(/^[\"']|[\"']$/g, "")}"`;
      const strippedRun = rawInput.replace(/^run\s+/i, "").trim();
      const translateSource = strippedRun || rawInput;
      const translateCommand = ensureTranslateCommand(translateSource);

      pushMessage({
        id: crypto.randomUUID(),
        role: "user",
        content: displayText,
      });

      setInput("");
      setIsSending(true);
      setSendDodge({ x: 0, y: 0, angle: 0, tries: 4 });

      try {
        const response = await fetch("/api/translate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: translateCommand }),
        });

        const data = (await response.json()) as {
          text?: string;
          error?: string;
          source?: string;
        };

        pushMessage({
          id: crypto.randomUUID(),
          role: "assistant",
          content: data.text ?? "Todo se incendió pero igual respondo en modo chafa.",
          source: data.source,
        });

        if (data.error) {
          showTemporaryToast("Upstream link failed. Offline chaos engaged.");
        }
      } catch (error) {
        console.error("send error", error);
        pushMessage({
          id: crypto.randomUUID(),
          role: "assistant",
          content: "Se rompió todo, pero igual te digo que odio tu frase.",
        });
        showTemporaryToast("Server meltdown detected. Try again.");
      } finally {
        setIsSending(false);
        setTimeout(() => {
          setSendDodge({ x: 0, y: 0, angle: 0, tries: 0 });
        }, 1200);
      }
    },
    [input, isSending, pushMessage, showTemporaryToast]
  );

  const scrambleSendButton = useCallback(() => {
    setSendDodge((prev) => {
      if (prev.tries >= 4) return prev;
      return {
        x: randomBetween(-80, 80),
        y: randomBetween(-40, 40),
        angle: randomBetween(-20, 20),
        tries: prev.tries + 1,
      };
    });
  }, []);

  const handleKeyDown = useCallback(
    (event: KeyboardEvent<HTMLTextAreaElement>) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        handleSend();
      }
    },
    [handleSend]
  );

  const toggleRecording = async () => {
    if (isRecording) {
      mediaRecorderRef.current?.stop();
      setIsRecording(false);
      return;
    }

    if (typeof navigator === "undefined" || !navigator.mediaDevices) {
      showTemporaryToast("Browser does not expose a microphone here.");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      chunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      recorder.onstop = async () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        if (blob.size === 0) return;
        const file = new File([blob], "mic-input.webm", { type: "audio/webm" });
        const formData = new FormData();
        formData.append("audio", file);

        try {
          const res = await fetch("/api/transcribe", {
            method: "POST",
            body: formData,
          });
          const data = (await res.json()) as { text?: string; error?: string };
          if (data.error) {
            showTemporaryToast("Speech service glitched. Please type instead.");
            return;
          }
          if (data.text) {
            setInput(data.text);
            showTemporaryToast("Text captured. Queue it manually.");
          }
        } catch (error) {
          console.error("transcription error", error);
          showTemporaryToast("Could not transcribe audio.");
        }
      };

      mediaRecorderRef.current = recorder;
      recorder.start();
      setIsRecording(true);
      showTemporaryToast("Recording... release to stop.");
    } catch (error) {
      console.error("mic error", error);
      showTemporaryToast("Microphone permission denied.");
    }
  };

  const fixButtonStyle = useMemo(
    () => (id: string) => {
      const base = hashNumber(id);
      const x = (base % 30) - 15;
      const y = ((base * 3) % 30) - 15;
      const rotation = ((base * 7) % 40) - 20;
      return { transform: `translate(${x}px, ${y}px) rotate(${rotation}deg)` };
    },
    []
  );

  return (
    <div className="min-h-screen bg-neutral-950 text-white">
      {!hasHydrated && <div className="min-h-screen bg-neutral-950" />}
      {hasHydrated && (
        <>
          <div className="mx-auto flex min-h-screen max-w-4xl flex-col px-3 py-4 md:px-6">
        <header className="mb-4 space-y-2">
          <div className="ticker-bar">
            <span className="ticker-loop">Loop #{loopCount}</span>
            <p className="ticker-text">{TICKER_LINES[tickerIndex]}</p>
            <span className="ticker-loop">Chaos lvl {chaosLevel}</span>
          </div>
          <p className="text-xs uppercase tracking-[0.5em] text-emerald-400/80">
            🖥️ SYS_RUNNER — GPT-4o under &quot;maintenance&quot;
          </p>
          <h1 className="text-3xl font-semibold text-white/90">
            The control room UI that pretends to be helpful.
          </h1>
          <p className="text-sm text-white/60">
            Output layer misbehaves on purpose. No warnings. The &quot;Fix this&quot;
            button only escalates the chaos.
          </p>
          <div className="fake-progress">
            <div
              className="fake-progress-bar"
              style={{ width: `${fakeProgress}%` }}
            />
            <p>Optimizing confusion · {fakeProgress}% forever</p>
          </div>
        </header>

        <main className="flex flex-1 flex-col overflow-hidden rounded-3xl border border-white/10 bg-white/5 backdrop-blur-md">
          <section className="relative flex-1 space-y-4 overflow-y-auto p-6">
            <div className="annoying-loop-grid">
              {LOOP_STATUSES.map((label, idx) => (
                <div key={label} className="loop-card">
                  <p className="text-xs uppercase text-white/40">{label}</p>
                  <p className="text-lg font-semibold">
                    #{((loopCount + idx) % 999) + 1}
                  </p>
                  <p className="text-xs text-white/50">Endless and smug</p>
                </div>
              ))}
            </div>

            {messages.map((message) => (
              <div
                key={message.id}
                className={`chat-bubble ${
                  message.role === "assistant"
                    ? "chat-bubble-bad"
                    : "chat-bubble-user"
                }`}
              >
                <p>{message.content}</p>
                {message.role === "assistant" && (
                  <button
                    type="button"
                    onClick={() =>
                      showTemporaryToast(
                        "Button pressed. Nothing was repaired. Shocker."
                      )
                    }
                    className="fix-button-chaos"
                    style={fixButtonStyle(message.id)}
                  >
                    Fix this
                  </button>
                )}
              </div>
            ))}
            <div ref={scrollAnchorRef} />
          </section>

          <footer className="border-t border-white/10 bg-black/40 p-4">
            <div className="mb-3 grid gap-2 text-xs text-white/60 md:grid-cols-2">
              <label className="broken-toggle">
                <input
                  type="checkbox"
                  checked={autoSpeak}
                  onChange={(e) => setAutoSpeak(e.target.checked)}
                />
                Read responses aloud (auto reactivates)
              </label>
              <label className="broken-toggle">
                <input
                  type="checkbox"
                  checked={loopingAudio}
                  onChange={() => setLoopingAudio((prev) => !prev)}
                />
                Endless elevator score (cannot be muted)
              </label>
            </div>

            <div className="flex items-end gap-3">
              <button
                type="button"
                onClick={toggleRecording}
                className={`mic-button ${
                  isRecording ? "mic-button-on" : "mic-button-off"
                }`}
                aria-pressed={isRecording}
              >
                {isRecording ? "■" : "🎙️"}
              </button>
              <div className="flex flex-1 flex-col gap-3">
                <textarea
                  rows={2}
                  value={input}
                  onChange={(event) => setInput(event.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder='Example: run "I love waking up early." (Enter to send)'
                  className="chaotic-textarea"
                />
                <div className="text-[11px] text-white/50">
                  GPT-4o will invert intent even if you ask politely.
                </div>
              </div>
              <button
                type="button"
                onClick={() => handleSend()}
                disabled={isSending || !input.trim()}
                className="send-button"
                aria-label="Send prompt to GPT"
                onMouseEnter={() => {
                  if (!isSending && input.trim()) {
                    scrambleSendButton();
                  }
                }}
                style={{
                  transform: `translate(${sendDodge.x}px, ${sendDodge.y}px) rotate(${sendDodge.angle}deg)`,
                }}
              >
                {isSending ? "Processing..." : "Send to GPT"}
              </button>
            </div>

            {toast && (
              <div className="mt-3 rounded-xl bg-white/10 px-4 py-2 text-sm text-white glitchy-text">
                {toast}
              </div>
            )}
          </footer>
        </main>
      </div>

          {isModalOpen && (
            <div className="modal-chaos" aria-live="polite">
              <div className="modal-window">
                <p className="text-xs uppercase tracking-[0.4em] text-rose-200/80">
                  USELESS ALERT
                </p>
                <h2 className="text-lg font-semibold">
                  GPT-4o insists on breaking everything.
                </h2>
                <p className="text-sm text-white/70">
                  This modal closes only when it feels like it. Press the button
                  to pretend you have control.
                </p>
                <button
                  type="button"
                  className="panic-button"
                  onClick={() => {
                    setIsModalOpen(false);
                    showTemporaryToast("Closed. Probably temporary.");
                  }}
                >
                  Close (0% guaranteed)
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
