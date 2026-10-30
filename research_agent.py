"""
Research Agent
--------------
An AI agent that FIRST asks you clarifying questions about your topic,
THEN searches the web and writes a research report (saved as a .md file).

Run it:  python research_agent.py
"""

import re
from datetime import datetime

import anthropic

MODEL = "claude-sonnet-5-5"

# Reads your key from the ANTHROPIC_API_KEY environment variable
client = anthropic.Anthropic()

# ---------------------------------------------------------------------------
# Step 1: the agent decides what questions it needs answered
# ---------------------------------------------------------------------------
QUESTION_PROMPT = """You are a research assistant. Before researching, you must
ask the user the questions you need answered to do a great job.

Given the user's topic, write 3 to 5 short, specific clarifying questions
(for example: goal, audience, depth, region, time period, preferred sources,
format). Number them. Output ONLY the numbered questions, nothing else."""

# ---------------------------------------------------------------------------
# Step 2: the agent researches using web search and writes the report
# ---------------------------------------------------------------------------
RESEARCH_PROMPT = """You are a careful research assistant with web search.
Use the topic and the user's answers to research thoroughly.

Write a clear report in Markdown with:
- A short summary at the top
- Key findings under headings
- Any disagreements or uncertainty between sources
- A "Sources" list with links at the end

Keep quotes under 15 words and put things in your own words.
Only state what the sources support."""

SEARCH_TOOL = {"type": "web_search_20250305", "name": "web_search", "max_uses": 6}


def get_text(response) -> str:
    """Join all text blocks from a response."""
    return "".join(b.text for b in response.content if b.type == "text")


def ask_questions(topic: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        system=QUESTION_PROMPT,
        messages=[{"role": "user", "content": f"Topic: {topic}"}],
    )
    return get_text(response)


def do_research(topic: str, questions: str, answers: str) -> str:
    messages = [
        {
            "role": "user",
            "content": (
                f"Topic: {topic}\n\n"
                f"Questions you asked:\n{questions}\n\n"
                f"My answers:\n{answers}\n\n"
                "Please research this and write the report."
            ),
        }
    ]

    # Web search can pause long turns; keep going until the agent is done.
    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=6000,
            system=RESEARCH_PROMPT,
            tools=[SEARCH_TOOL],
            messages=messages,
        )
        if response.stop_reason == "pause_turn":
            messages.append({"role": "assistant", "content": response.content})
            continue
        return get_text(response)


def save_report(topic: str, report: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:40] or "report"
    filename = f"report-{slug}-{datetime.now():%Y%m%d-%H%M}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    return filename


def main():
    print("=== Research Agent ===")
    topic = input("What would you like me to research?\n> ").strip()
    if not topic:
        print("No topic given. Bye!")
        return

    print("\nBefore I start, I need to ask you a few things:\n")
    questions = ask_questions(topic)
    print(questions)

    print("\nType your answers below (one message is fine; press Enter to send):")
    answers = input("> ").strip() or "No preference, use your best judgment."

    print("\nResearching... this can take a minute.\n")
    report = do_research(topic, questions, answers)

    filename = save_report(topic, report)
    print(report)
    print(f"\n--- Report saved to {filename} ---")


if __name__ == "__main__":
    main()
