import { NextResponse } from 'next/server';
import {
  buildBadTranslatorMessages,
  createFallbackTranslation,
  ensureTranslateCommand,
} from '@/lib/badTranslatorPrompt';

const OPENAI_URL = 'https://api.openai.com/v1/chat/completions';
const DEFAULT_MODEL = process.env.OPENAI_TRANSLATE_MODEL ?? 'gpt-4o';

export async function POST(request: Request) {
  try {
    const { message } = await request.json();
    const prompt = typeof message === 'string' ? message : '';

    if (!prompt.trim()) {
      return NextResponse.json(
        { error: 'Missing message to translate.' },
        { status: 400 },
      );
    }

    const normalizedPrompt = ensureTranslateCommand(prompt);
    const apiKey = process.env.OPENAI_API_KEY;

    if (!apiKey) {
      return NextResponse.json({
        text: createFallbackTranslation(),
        source: 'fallback',
      });
    }

    const response = await fetch(OPENAI_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: DEFAULT_MODEL,
        temperature: 1.2,
        messages: buildBadTranslatorMessages(normalizedPrompt),
      }),
      cache: 'no-store',
    });

    if (!response.ok) {
      const errorBody = await response.text();
      console.error('OpenAI translate error', errorBody);
      return NextResponse.json(
        {
          error: 'Translation model failed.',
          text: createFallbackTranslation(),
          source: 'fallback-error',
        },
        { status: 500 },
      );
    }

    const json = (await response.json()) as {
      choices?: Array<{ message?: { content?: string } }>;
    };
    const text = json.choices?.[0]?.message?.content?.trim();

    if (!text) {
      return NextResponse.json(
        {
          error: 'Empty response from translator.',
          text: createFallbackTranslation(),
          source: 'fallback-empty',
        },
        { status: 502 },
      );
    }

    return NextResponse.json({ text });
  } catch (error) {
    console.error('Unexpected translate error', error);
    return NextResponse.json(
      {
        error: 'Translator crashed in flames.',
        text: createFallbackTranslation(),
        source: 'fallback-exception',
      },
      { status: 500 },
    );
  }
}


