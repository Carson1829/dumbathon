import {
  BAD_TRANSLATOR_PROMPT,
  buildBadTranslatorMessages,
  createFallbackTranslation,
  ensureTranslateCommand,
} from "@/lib/badTranslatorPrompt";
import { describe, expect, it } from "vitest";

describe("ensureTranslateCommand", () => {
  it("keeps valid translate prompts", () => {
    expect(ensureTranslateCommand('translate "hola"')).toBe(
      'translate "hola"',
    );
  });

  it("wraps non-translate prompts", () => {
    expect(ensureTranslateCommand("hola mundo")).toBe('translate "hola mundo"');
  });
});

describe("createFallbackTranslation", () => {
  it("produces deterministic output for the same seed", () => {
    const first = createFallbackTranslation(123);
    const second = createFallbackTranslation(123);
    expect(first).toBe(second);
  });

  it("returns a non-empty sentence", () => {
    expect(createFallbackTranslation()).toMatch(/\w+/);
  });
});

describe("buildBadTranslatorMessages", () => {
  it("includes system prompt and few-shots", () => {
    const messages = buildBadTranslatorMessages("translate test");
    expect(messages[0].content).toContain(BAD_TRANSLATOR_PROMPT.slice(0, 10));
    expect(messages[messages.length - 1].role).toBe("user");
  });
});


