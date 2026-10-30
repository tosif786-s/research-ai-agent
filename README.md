# Research Agent

An AI agent that asks you the questions it needs, then researches your topic on the web and saves a report.

## How it works
1. You type a topic.
2. The agent asks 3-5 clarifying questions (goal, audience, depth, etc.).
3. You answer.
4. The agent searches the web and writes a Markdown report with sources.

## Setup (one time)

1. **Install Python 3.9+** from https://www.python.org/downloads/ (tick "Add Python to PATH" on Windows).
2. **Get an API key** at https://console.anthropic.com/ (API Keys section).
3. **Open a terminal** in this folder and install the library:
   ```
   pip install -r requirements.txt
   ```
4. **Set your API key**:
   - Mac/Linux: `export ANTHROPIC_API_KEY="your-key-here"`
   - Windows (PowerShell): `$env:ANTHROPIC_API_KEY="your-key-here"`

   Web search must be enabled for your organization in the Anthropic Console.

## Run it
```
python research_agent.py
```

## Customize
- Change `MODEL` at the top of `research_agent.py`.
- Edit `QUESTION_PROMPT` to change what the agent asks.
- Edit `RESEARCH_PROMPT` to change the report style.
- Raise `max_uses` in `SEARCH_TOOL` for deeper research.
