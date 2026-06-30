# Listening Trainers — Minimal Pair Auditory Discrimination

Four self-contained, single-file HTML trainers for English phoneme discrimination. Open in any browser (desktop or mobile) — no server, no install, no dependencies. Uses the browser's built-in speech synthesis (TTS) with multi-voice rotation to simulate high-variability phonetic training (HVPT).

## Trainers

| File | Contrast | Example Pairs |
|------|----------|---------------|
| `tr-ch-listening-trainer.html` | /tr/ vs /tʃ/ | train–chain, trip–chip, treat–cheat |
| `fr-fire-listening-trainer.html` | /fr/ vs /f/ | fry–fire, free–fee, fresh–flesh |
| `nl-listening-trainer.html` | /n/ vs /l/ | need–lead, night–light, name–lame |
| `f-th-listening-trainer.html` | /f/ vs /θ/ | first–third, free–three, fought–thought |

## How It Works

Each trainer has three progressive stages:

1. **Stage 1 — Isolated Words (6–8 pairs)**  
   Hear a word, identify which sound it contains. Small, focused set to build initial discrimination.

2. **Stage 2 — Expanded Word Bank (14–16 pairs)**  
   Same format, larger pool. Introduces words not in Stage 1. Must score ≥80% in Stage 1 to unlock.

3. **Stage 3 — Words in Sentences**  
   Hear a full sentence, identify the target sound in the key word. Tests discrimination in connected speech.

Each round is 10 questions. Voices rotate randomly across TTS engines available in your browser (Samantha, Daniel, Karen, Alex, Moira, etc. on macOS/iOS).

## Features

- **Multi-voice TTS rotation** — each question uses a different voice when available, providing natural acoustic variability
- **Stage locking** — Stage N+1 unlocks when Stage N reaches 80%+ accuracy
- **Preview before answering** — see the word (and IPA) before the question begins
- **Immediate feedback** — correct/incorrect with IPA shown after each answer
- **Review table** — all 10 questions with your answers vs correct answers shown after each round
- **Export report** — generates a structured text report you can share with a teacher
- **Keyboard shortcuts** — Space to play, ←/→ to answer, Enter to advance
- **Mobile-friendly** — responsive layout, works on phone browsers
- **History tracking** — all answers stored in session; summary stats per stage

## Usage

1. Open any `.html` file in a browser (double-click or `open tr-ch-listening-trainer.html`)
2. Tap/click the play button or press Space to hear a word
3. Choose which sound you heard
4. After 10 questions, review your results
5. Score ≥80% to unlock the next stage
6. Use "Export Report" to save results

For mobile use, host these files on GitHub Pages or any static file server, then open the URL in your phone's browser.

## Technical Notes

- Uses the [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API) (`SpeechSynthesis`)
- Voice availability depends on your OS and browser. macOS/iOS have the richest built-in voices.
- All data stays in your browser — no tracking, no network requests, no server
- Each file is ~1,500 lines, fully self-contained (HTML + CSS + JS)

## Why This Exists

These trainers were built because:

1. **Receptive phonological awareness must come before production.** If you can't hear the difference between /tr/ and /tʃ/, you can't reliably produce it. Most pronunciation tools focus on production (speaking into a mic) and skip this foundational step.

2. **Existing HVPT tools are closed-source or require logins.** Linguatorium Auris, English Accent Coach, and similar academic tools are not available as self-hosted open-source projects.

3. **Browser TTS is good enough now.** Modern speech synthesis (especially on macOS/iOS) is clear enough for phoneme discrimination training, and it provides the multi-talker variability that HVPT research shows is essential.

4. **Single HTML files are the simplest deployment format.** No npm, no build step, no server. Just open the file. Works on phones.

## License

MIT — use it, modify it, share it.

## Contributing

To add a new phoneme contrast:

1. Copy any existing trainer HTML file
2. Replace the `WORD_BANKS` object with your own minimal pairs (IPA included)
3. Update the title, color theme variables, and UI labels
4. Test on at least 2 browsers with different TTS voice sets

Pull requests for new language pairs, additional words, or UX improvements are welcome.
