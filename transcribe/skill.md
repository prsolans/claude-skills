---
name: transcribe
description: >
  Transcribe audio files locally using OpenAI Whisper. Supports mp3, m4a, wav, mp4, webm,
  and other common audio/video formats. Use when the user says "transcribe", "transcribe this",
  provides an audio file path, or asks to convert audio/video to text.
---

# Transcribe Audio

Transcribe an audio or video file to text using OpenAI Whisper, running locally on the machine.

## Arguments

The user will provide a file path to an audio or video file. If no path is given, ask for one.

Supported formats: mp3, m4a, wav, flac, ogg, webm, mp4, avi, mkv, mov

## Dependencies

Before transcribing, check that dependencies are installed:

```bash
which ffmpeg > /dev/null 2>&1 || echo "NEED_FFMPEG"
uv tool list 2>/dev/null | grep -q whisper || echo "NEED_WHISPER"
```

If `NEED_FFMPEG`: run `brew install ffmpeg`
If `NEED_WHISPER`: run `uv tool install openai-whisper --with torch --with setuptools-rust`

Only install what's missing. Skip checks if previously confirmed in this session.

## Transcription

Run whisper on the file:

```bash
whisper "<file_path>" --model base --output_format txt --output_dir /tmp/whisper_out
```

The output txt file will be at `/tmp/whisper_out/<filename_without_ext>.txt`.

### Model selection

- `base` — default, fast, good for clear audio (~1GB download on first use)
- `small` — better accuracy, slower (~2GB). Use if the user asks for higher quality or if `base` output is poor.
- `medium` — high accuracy, significantly slower (~5GB). Only if the user explicitly asks.

Tell the user which model you're using before starting. On first run, mention the model will be downloaded.

## Output

1. Read the output file and display the transcript to the user
2. **Always** copy the transcript to the project's `_context/transcripts/` directory (create it if it doesn't exist). Use the same filename as the source audio but with a `.txt` extension. Tell the user where it was saved.
3. Ask if they want to:
   - Clean it up (fix formatting, add paragraphs, remove filler words)
   - Summarize it

## Error Handling

- If the file doesn't exist, say so
- If whisper fails on the format, try converting with ffmpeg first:
  ```bash
  ffmpeg -i "<file_path>" -ar 16000 -ac 1 /tmp/whisper_input.wav
  ```
  Then run whisper on the converted file.
