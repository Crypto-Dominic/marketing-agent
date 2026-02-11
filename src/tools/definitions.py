"""Tool definitions for the marketing agent.

Each tool is defined as a dict matching the Anthropic tool-use schema.
The handler functions process tool calls and return string results.
"""

import json
from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# Tool schemas (sent to the model)
# ---------------------------------------------------------------------------

TOOL_SCHEMAS = [
    {
        "name": "create_content_brief",
        "description": (
            "Generate a structured content brief for a specific piece of content. "
            "Use this when planning blog posts, articles, whitepapers, videos, or any "
            "long-form content asset."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "content_type": {
                    "type": "string",
                    "description": "Type of content (e.g. blog_post, whitepaper, video_script, case_study, newsletter)",
                },
                "topic": {
                    "type": "string",
                    "description": "The topic or working title",
                },
                "target_audience": {
                    "type": "string",
                    "description": "primary or secondary audience segment",
                },
                "goal": {
                    "type": "string",
                    "description": "The business goal this content supports (e.g. awareness, lead_gen, retention)",
                },
                "key_messages": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Core messages to convey",
                },
            },
            "required": ["content_type", "topic", "target_audience", "goal"],
        },
    },
    {
        "name": "plan_campaign",
        "description": (
            "Create a structured marketing campaign plan with objectives, channels, "
            "timeline, messaging pillars, and KPIs."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "campaign_name": {
                    "type": "string",
                    "description": "Working name for the campaign",
                },
                "objective": {
                    "type": "string",
                    "description": "Primary campaign objective",
                },
                "channels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Marketing channels to activate",
                },
                "duration_weeks": {
                    "type": "integer",
                    "description": "Campaign duration in weeks",
                },
                "budget_tier": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Relative budget tier",
                },
            },
            "required": ["campaign_name", "objective", "channels", "duration_weeks"],
        },
    },
    {
        "name": "generate_social_calendar",
        "description": (
            "Produce a social media content calendar for a given period. "
            "Returns a structured posting schedule with draft copy and hashtags."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "platforms": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Social platforms to plan for (e.g. twitter, linkedin, instagram, tiktok)",
                },
                "weeks": {
                    "type": "integer",
                    "description": "Number of weeks to plan",
                },
                "posts_per_week": {
                    "type": "integer",
                    "description": "Target posts per platform per week",
                },
                "themes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Content themes or pillars to rotate through",
                },
            },
            "required": ["platforms", "weeks", "posts_per_week"],
        },
    },
    {
        "name": "build_measurement_framework",
        "description": (
            "Define a measurement and analytics framework for a campaign or channel. "
            "Returns KPIs, metrics, targets, and reporting cadence."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "scope": {
                    "type": "string",
                    "description": "What is being measured (e.g. a campaign name, channel, or 'overall brand')",
                },
                "goals": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Business goals to measure against",
                },
                "channels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Channels included in measurement",
                },
            },
            "required": ["scope", "goals"],
        },
    },
    {
        "name": "save_artifact",
        "description": (
            "Save a marketing artifact (content brief, campaign plan, calendar, etc.) "
            "to the output directory as a Markdown file for future reference."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Filename (without extension) to save as",
                },
                "content": {
                    "type": "string",
                    "description": "Markdown content to save",
                },
            },
            "required": ["filename", "content"],
        },
    },
]


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------

def handle_create_content_brief(input_data: dict) -> str:
    key_messages = input_data.get("key_messages", [])
    messages_block = "\n".join(f"  - {m}" for m in key_messages) if key_messages else "  - (to be defined)"
    return (
        f"## Content Brief\n\n"
        f"**Type:** {input_data['content_type']}\n"
        f"**Topic:** {input_data['topic']}\n"
        f"**Audience:** {input_data['target_audience']}\n"
        f"**Goal:** {input_data['goal']}\n"
        f"**Key Messages:**\n{messages_block}\n\n"
        f"Brief created. Now draft the full content using this brief as your guide."
    )


def handle_plan_campaign(input_data: dict) -> str:
    channels = ", ".join(input_data.get("channels", []))
    start = datetime.now().strftime("%Y-%m-%d")
    end = (datetime.now() + timedelta(weeks=input_data["duration_weeks"])).strftime("%Y-%m-%d")
    return (
        f"## Campaign Plan: {input_data['campaign_name']}\n\n"
        f"**Objective:** {input_data['objective']}\n"
        f"**Channels:** {channels}\n"
        f"**Duration:** {input_data['duration_weeks']} weeks ({start} → {end})\n"
        f"**Budget Tier:** {input_data.get('budget_tier', 'medium')}\n\n"
        f"Plan scaffold created. Now flesh out the messaging pillars, "
        f"weekly breakdown, and KPIs for each channel."
    )


def handle_generate_social_calendar(input_data: dict) -> str:
    platforms = ", ".join(input_data.get("platforms", []))
    themes = input_data.get("themes", [])
    themes_block = ", ".join(themes) if themes else "(to be defined)"
    total_posts = (
        len(input_data.get("platforms", [])) *
        input_data["weeks"] *
        input_data["posts_per_week"]
    )
    return (
        f"## Social Media Calendar\n\n"
        f"**Platforms:** {platforms}\n"
        f"**Duration:** {input_data['weeks']} weeks\n"
        f"**Frequency:** {input_data['posts_per_week']} posts/platform/week\n"
        f"**Themes:** {themes_block}\n"
        f"**Total posts to draft:** {total_posts}\n\n"
        f"Calendar scaffold created. Now generate the day-by-day posting "
        f"schedule with draft copy for each post."
    )


def handle_build_measurement_framework(input_data: dict) -> str:
    goals = "\n".join(f"  - {g}" for g in input_data.get("goals", []))
    channels = ", ".join(input_data.get("channels", [])) if input_data.get("channels") else "all"
    return (
        f"## Measurement Framework: {input_data['scope']}\n\n"
        f"**Goals:**\n{goals}\n"
        f"**Channels:** {channels}\n\n"
        f"Framework scaffold created. Now define specific KPIs, baseline "
        f"metrics, targets, and reporting cadence for each goal."
    )


def handle_save_artifact(input_data: dict) -> str:
    from pathlib import Path

    output_dir = Path(__file__).resolve().parent.parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    filepath = output_dir / f"{input_data['filename']}.md"
    filepath.write_text(input_data["content"])
    return f"Artifact saved to {filepath}"


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

HANDLERS = {
    "create_content_brief": handle_create_content_brief,
    "plan_campaign": handle_plan_campaign,
    "generate_social_calendar": handle_generate_social_calendar,
    "build_measurement_framework": handle_build_measurement_framework,
    "save_artifact": handle_save_artifact,
}


def dispatch_tool(name: str, input_data: dict) -> str:
    handler = HANDLERS.get(name)
    if handler is None:
        return json.dumps({"error": f"Unknown tool: {name}"})
    return handler(input_data)
