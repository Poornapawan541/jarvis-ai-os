# JARVIS AI OS

A local, voice driven desktop assistant built in Python for Windows. JARVIS listens through a microphone, transcribes speech with Whisper, routes requests to agents and skills, and answers aloud with Piper. It can use a local Ollama model for open ended requests and supports desktop, browser, email, WhatsApp Web, calculation, and memory workflows.

> **Project status:** This README describes functionality present in the checked out source and integrations explicitly exercised in the development conversation. The project is under active development; individual actions depend on local software, account access, and configuration.

## Features

- Speech capture and transcription using Faster Whisper (`small`, CUDA, `float16` in the current root configuration).
- Spoken responses using the bundled Piper executable and `en_US-lessac-medium` voice model.
- Conversation engine with recent conversation history, simple follow up resolution, memory retrieval, routing, planning, and an Ollama fallback.
- Local Llama inference through Ollama's HTTP API. The active LLM client is configured for `llama3:latest`; the root `config.py` separately lists `llama3.2:3b`, so check the model setting used by the active client before downloading a model.
- SQLite memory stored at `data/memory.db`.
- Dynamically discovered skills for Gmail, WhatsApp, browser actions, system actions, calculations, memory, and weather.
- Agent routing for browser, research, and system requests, plus a planner and task executor.
- Browser automation and website launching. WhatsApp Web messaging uses Playwright over Chrome's CDP endpoint (`127.0.0.1:9222`) and the signed-in Chrome session.
- Gmail reading and sending through the Gmail API with local OAuth credentials.
- Logging under `logs/` and a collection of focused development tests under `tests/`.

## Architecture

```text
Microphone
  -> audio recording / VAD
  -> Faster Whisper speech-to-text
  -> conversation engine
       -> conversation history and SQLite memory
       -> agent router
       -> skill router
       -> planner / executor
       -> Ollama Llama fallback
  -> response text
  -> Piper text-to-speech
  -> speakers
```

Browser and app actions are performed by agents or skills. WhatsApp has a dedicated skill that attaches Playwright to an already running Chrome instance over CDP. Gmail uses the Gmail API and OAuth token files.

### Agents and skills

The agent router contains browser, research, and system agents (`core/agents/`). Skills are discovered from `core/skills/` at startup. Current skill modules include:

- `gmail` — reads today's inbox messages and summarizes them; supports conversational sending.
- `whatsapp` — sends a text message to a named WhatsApp Web contact.
- `browser` — opens supported websites and handles web searches.
- `system` — launches/closes supported applications and sites; includes lock, shutdown, and restart actions.
- `calculator` — handles basic arithmetic expressions.
- `memory` — interacts with stored memories.
- `weather` — weather-related requests (availability depends on its configured service/access).

The conversation engine tries quick responses and memory, then agent and skill routing, planning/execution, and finally the LLM fallback. Exact routing depends on each agent and skill's command matching logic.

## Voice pipeline

The audio recorder captures microphone input and the speech-to-text module transcribes it with Faster Whisper. The current root `config.py` sets the model to `small`, device to `cuda`, and compute type to `float16`; compatible NVIDIA/CUDA libraries are therefore needed for that configuration. Adjust those values in `config.py` for the hardware available.

Piper runs from `piper/piper.exe`, using `models/voices/en_US-lessac-medium.onnx`. Its generated audio is played through the local audio output. The repository also contains wake-word and voice-activity-detection modules; the main loop shown in `core/jarvis.py` records and transcribes each turn directly, so always-on wake-word activation is not claimed here.

## Local LLM and memory

The LLM client calls Ollama at `http://127.0.0.1:11434/api/chat`. Its current source model is `llama3:latest`, with a 60-second timeout and a short conversational system prompt. Start Ollama locally and make sure that exact model is available. The root configuration has a different model label (`llama3.2:3b`), which is a configuration inconsistency to resolve if you want one source of truth.

SQLite stores memory rows in `data/memory.db`. The conversation engine processes and searches memories when handling a request and includes relevant results in the LLM prompt. Conversation history is maintained by the conversation history component.

## Integrations

### Browser and desktop

The browser manager can open Chrome or Edge. Browser and system skills provide additional website and application actions. App names and supported websites are defined in the corresponding skill source; arbitrary applications are not guaranteed to work.

### Gmail

Gmail access uses Google's API and OAuth. The project root currently has `credentials.json` and `token.json` in the checkout; these are private credentials and must not be published or committed. For a fresh installation, provide your own OAuth client file and authorize the account to generate a token. The current Gmail implementation reads messages received today and can send email through a voice-led flow.

### WhatsApp Web

The WhatsApp skill attaches to an already running Chrome through Playwright's CDP connection at `http://127.0.0.1:9222`, navigates to WhatsApp Web, finds a contact without case sensitivity, and sends the requested text. The development conversation confirmed successful end-to-end voice sending and contact matching. You need Chrome launched with remote debugging and an authenticated WhatsApp Web session. Sending a command sends a real message.

Example Chrome launch (adjust the executable path if needed):

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" `
  --remote-debugging-port=9222 `
  --user-data-dir="C:\jarvis\data\chrome_automation"
```

Keep that Chrome session open while JARVIS uses WhatsApp.

## Prerequisites

The checked out project is Windows-oriented. The source confirms these external prerequisites, but does not include a dependency lockfile or `requirements.txt`:

- Windows with Python and a working microphone/audio output.
- Python packages imported by the project, including Faster Whisper, PyTorch/CUDA support for the configured GPU mode, `requests`, `simpleaudio`, Playwright, and Google API/OAuth client libraries. Install versions compatible with the machine; the project currently does not pin them.
- Ollama installed and running locally, with the model configured in `core/brain/llm.py` available.
- Chrome installed for browser/WhatsApp actions; WhatsApp messaging additionally requires remote debugging on port 9222 and a logged-in WhatsApp Web session.
- Google OAuth client credentials and user authorization for Gmail features.

Piper's Windows executable and voice model are present in this checkout. Keep the `piper/` and `models/voices/` assets at their expected paths.

## Setup

1. Clone or copy the project to `C:\jarvis` (or update paths and commands for the chosen location).
2. Create and activate a virtual environment:

   ```powershell
   cd C:\jarvis
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the Python packages required by the imports listed above, including a Faster Whisper/PyTorch combination that supports the configured CUDA device. There is no checked-in dependency manifest yet, so package versions must be selected for your environment.
4. Install and start Ollama, then pull the model named in the active LLM client (`llama3:latest`) or update the client configuration to the model you have installed.
5. Review `config.py`, especially `WHISPER_MODEL`, `WHISPER_DEVICE`, `WHISPER_COMPUTE_TYPE`, and `OLLAMA_MODEL`. Note that the active LLM client currently hard-codes a different model value.
6. For Gmail, configure Google OAuth credentials and authorize the account. Protect `credentials.json` and `token.json`; never share them publicly.
7. For WhatsApp, start Chrome with CDP enabled as shown above, sign in to WhatsApp Web, and leave Chrome running.

## Configuration

The root `config.py` contains the current assistant name, audio format, Whisper model/device/precision, Ollama model label, speech settings, and folder names. Some modules also define their own defaults directly. In particular, the active Ollama model and `core/config/settings.py` defaults do not match the root configuration. Review the values in the modules used by your run before changing models.

The WhatsApp CDP address is defined in `core/skills/whatsapp.py`. Gmail OAuth scope and local token handling are in `core/skills/gmail.py`. Do not commit personal OAuth credentials, generated tokens, browser profiles, memory databases, or logs.

## Run

Start Ollama in one PowerShell window if it is not already running:

```powershell
ollama serve
```

Start JARVIS in another window:

```powershell
cd C:\jarvis
.\.venv\Scripts\Activate.ps1
python main.py
```

JARVIS greets the user and then records voice input in a loop. Say `exit`, `quit`, `bye`, `goodbye`, or `stop` to end the session.

## Example voice commands

Use the command forms supported by the current routing logic:

- “Send a WhatsApp message to Rishi Sasi saying Hello from JARVIS.”
- “Read my emails.”
- “Send an email to [email address].” JARVIS enters a voice-led email composition flow.
- “Open YouTube.”
- “Search for Python tutorials.”
- “Calculate 12 plus 8.”
- “Open Notepad.”
- “Remember that my appointment is on Friday.” / “What do you remember about my appointment?”

Actual supported wording can vary by skill; confirm the response before relying on a consequential action.

## Project structure

```text
main.py                 Application entry point
config.py               Root audio, model, and assistant settings
core/
  agents/                Browser, research, and system agents and router
  audio/                 Recording, VAD, and wake-word utilities
  brain/                 Prompt construction and Ollama client
  browser/               Browser session, manager, and actions
  config/                Additional settings defaults
  conversation/          Engine, history, and follow-up resolver
  memory/                SQLite storage, management, and search
  parser/                Command parsing
  planner/               Intent parsing, task planning, and execution
  services/              Logging
  skills/                Gmail, WhatsApp, browser, system, calculator,
                         memory, and weather skills
  voice/                 Faster Whisper STT and Piper TTS
models/voices/           Piper voice model assets
piper/                   Piper Windows runtime assets
data/                    SQLite database and local browser profiles
logs/                    Runtime logs
scripts/                 Project utility scripts
tests/                   Focused component and integration tests
```

## Tests and benchmarks

The repository contains tests for audio/VAD, Whisper, Piper, agents, planner, parser, memory, browser actions, and skills. They are development tests and may depend on local devices, accounts, installed programs, and model files.

The conversation context confirms the WhatsApp voice workflow succeeded end to end. It does not include a benchmark report supporting “20/20 task success” or “96.77% intent routing,” so those figures are intentionally not presented as verified results. Add them only alongside a reproducible test set, date, and measurement method.

## Limitations

- There is no dependency manifest or pinned package set in the checkout, which makes setup less reproducible.
- The current source contains conflicting LLM model defaults; `core/brain/llm.py` is the active client setting.
- GPU speech recognition depends on compatible CUDA hardware and libraries with the current configuration.
- Gmail and WhatsApp require working account authentication. OAuth tokens and browser sessions are local user data.
- WhatsApp automation relies on WhatsApp Web's page structure and may need updates if the site changes.
- Skill and agent routing is based on implemented matching logic; ambiguous wording may fall through to the LLM.
- System commands such as closing apps, locking, restarting, and shutting down can affect the computer. Use clear commands and review the spoken response.
- The main loop continuously records turns; the available wake-word module is not wired into that loop in the current source.

## Future improvements

- Add a pinned dependency manifest and a first-run setup guide.
- Consolidate model and runtime settings into one configuration source.
- Add a repeatable benchmark report for intent routing and task completion.
- Expand automated tests using mocked integrations, with separate opt-in tests for real Gmail, Chrome, and WhatsApp accounts.
- Add confirmation steps for high-impact desktop actions and a clearer preview/confirmation flow for outbound messages.
- Improve routing for natural variations and expose supported commands in the app.

## Security and privacy

JARVIS can access email, WhatsApp Web, browser sessions, microphone input, and local memory. Keep OAuth files, browser profile data, logs, and the SQLite database private. Review a command before using account or operating-system actions. The project is configured to call Ollama on localhost, but the actual privacy properties also depend on the installed tools and enabled integrations.
