# Brand Marketing Agent

An AI-powered Senior Marketing Manager agent built on Claude. It acts as the
strategic owner of your brand's marketing — generating on-brand content,
planning campaigns, managing social calendars, and advising on analytics.

## Features

- **Brand-aware** — all output is governed by your brand config (voice, tone,
  audience, products, competitors)
- **Content creation** — blog posts, ad copy, email campaigns, landing pages,
  video scripts
- **Campaign planning** — integrated plans with objectives, channels, timeline,
  and KPIs
- **Social media management** — platform-specific calendars with draft copy and
  hashtag strategies
- **Measurement frameworks** — KPIs, metrics, and reporting structures
- **Artifact saving** — export any deliverable to Markdown files in `output/`

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key
cp .env.example .env
# Edit .env and add your Anthropic API key

export ANTHROPIC_API_KEY=your-key-here

# 3. Edit your brand config
# Open config/brand_config.yaml and fill in your brand details

# 4. Run the agent
python main.py
```

## Usage

Once running, type natural-language requests:

```
You> Write a LinkedIn post announcing our new product launch
You> Plan a 4-week awareness campaign for Q2
You> Create a 2-week social media calendar for Twitter and Instagram
You> Build a measurement framework for our email marketing program
You> Draft 3 subject lines for our spring newsletter
```

### Commands

| Command   | Description                          |
|-----------|--------------------------------------|
| `/reset`  | Clear conversation history           |
| `/config` | Show loaded brand configuration      |
| `/quit`   | Exit the agent                       |

## Project Structure

```
marketing-agent/
├── config/
│   └── brand_config.yaml    # Your brand configuration
├── src/
│   ├── agent.py             # Core agent loop
│   ├── brand.py             # Brand config loader
│   ├── cli.py               # Interactive CLI
│   ├── prompts.py           # System prompt templates
│   └── tools/
│       └── definitions.py   # Tool schemas and handlers
├── output/                  # Saved artifacts (gitignored)
├── main.py                  # Entry point
├── requirements.txt
└── pyproject.toml
```

## Configuration

All brand details live in `config/brand_config.yaml`. The agent reads this at
startup and injects it into every interaction. Edit it to match your brand:

- **brand** — name, tagline, mission, vision
- **voice** — tone, personality, writing style, dos/don'ts
- **audience** — primary and secondary segments with demographics and channels
- **products** — your product catalog with benefits
- **competitors** — competitive landscape for positioning
- **differentiators** — what makes you unique
