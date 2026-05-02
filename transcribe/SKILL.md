---
name: transcribe
description: >
  Transcribe audio locally using OpenAI Whisper. Accepts a local file (mp3, m4a, wav, mp4, webm,
  and other formats) or a URL (YouTube, Loom, any yt-dlp-supported source). Use when the user says
  "transcribe", "transcribe this", provides an audio file path or URL, or asks to convert
  audio/video to text.
---

# Transcribe Audio

Transcribe an audio or video file to text using OpenAI Whisper, running locally on the machine.

## Arguments

The user will provide a file path or URL. If neither is given, ask for one.

- **File path** — any local audio or video file: mp3, m4a, wav, flac, ogg, webm, mp4, avi, mkv, mov
- **URL** — YouTube, Loom, or any URL that `yt-dlp` supports. Detected by the argument starting with `http://` or `https://`.

## Dependencies

Before transcribing, check that dependencies are installed:

```bash
which ffmpeg > /dev/null 2>&1 || echo "NEED_FFMPEG"
uv tool list 2>/dev/null | grep -q whisper || echo "NEED_WHISPER"
which yt-dlp > /dev/null 2>&1 || echo "NEED_YTDLP"
```

If `NEED_FFMPEG`: run `brew install ffmpeg`
If `NEED_WHISPER`: run `uv tool install openai-whisper --with torch --with setuptools-rust`
If `NEED_YTDLP` and input is a URL: run `brew install yt-dlp`

Only install what's missing. Skip checks if previously confirmed in this session.

## URL input

If the argument is a URL, download the audio before transcribing:

```bash
yt-dlp -x --audio-format mp3 -o "/tmp/whisper_input.%(ext)s" "<url>"
```

The downloaded file will be at `/tmp/whisper_input.mp3`. Use this as the input to Whisper.

Tell the user: "Downloading audio from URL..." before running. If `yt-dlp` fails (private video, unsupported site, etc.), report the error and stop — do not attempt to transcribe.

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

1. Read the output file and display the transcript to the user.
2. **Always** copy the transcript to the project's `_context/transcripts/` directory (create it if it doesn't exist). Use the same filename as the source audio but with a `.txt` extension. Tell the user where it was saved.
3. Offer next steps — present all three options together, not sequentially:

   > "Transcript saved to `_context/transcripts/<filename>.txt`. What next?
   > - **a)** Clean it up (fix formatting, add paragraphs, remove filler words)
   > - **b)** Summarize it
   > - **c)** Run `/create-issues` to extract Linear issues from it
   > - Or just say 'nothing' to stop here."

   If the user picks **c**, run the full `create-issues` flow using the saved transcript path as input — don't ask them to invoke it separately. Skip the `create-issues` audio detection step (Step 0) since transcription is already done.

   If the user picks multiple options (e.g. "a and c"), do them in order: clean up first, then run `create-issues` on the cleaned version.

## Error Handling

- If the file doesn't exist, say so
- If whisper fails on the format, try converting with ffmpeg first:
  ```bash
  ffmpeg -i "<file_path>" -ar 16000 -ac 1 /tmp/whisper_input.wav
  ```
  Then run whisper on the converted file.
