import { NextResponse } from 'next/server';

const OPENAI_TRANSCRIBE_URL = 'https://api.openai.com/v1/audio/transcriptions';
const TRANSCRIBE_MODEL =
  process.env.OPENAI_TRANSCRIBE_MODEL ?? 'gpt-4o-mini-transcribe';

export async function POST(request: Request) {
  try {
    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) {
      return NextResponse.json(
        { error: 'Missing OpenAI API key.' },
        { status: 500 },
      );
    }

    const formData = await request.formData();
    const audio = formData.get('audio');

    if (!audio || !(audio instanceof File)) {
      return NextResponse.json(
        { error: 'Missing audio payload.' },
        { status: 400 },
      );
    }

    const openAiForm = new FormData();
    openAiForm.append('file', audio, audio.name || 'mic.webm');
    openAiForm.append('model', TRANSCRIBE_MODEL);
    openAiForm.append('response_format', 'json');

    const response = await fetch(OPENAI_TRANSCRIBE_URL, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
      },
      body: openAiForm,
    });

    if (!response.ok) {
      const errorBody = await response.text();
      console.error('OpenAI transcribe error', errorBody);
      return NextResponse.json(
        { error: 'Transcription failed.' },
        { status: 500 },
      );
    }

    const result = (await response.json()) as { text?: string };
    return NextResponse.json({ text: result.text ?? '' });
  } catch (error) {
    console.error('Unexpected transcription error', error);
    return NextResponse.json(
      { error: 'Transcription crashed.' },
      { status: 500 },
    );
  }
}


