"""Configuration for AI Finance Radar MVP."""

from __future__ import annotations

RSS_FEEDS = [
    # AI sources
    "https://openai.com/blog/rss.xml",
    "https://www.anthropic.com/news/rss",
    "https://huggingface.co/blog/feed.xml",
    "https://ai.googleblog.com/feeds/posts/default",
    # Finance / banking / tech sources
    "https://www.ft.com/technology?format=rss",
    "https://www.reuters.com/technology/rss",
    "https://www.reuters.com/finance/rss",
    "https://www.finextra.com/rss/headlines.aspx",
    "https://www.americanbanker.com/feeds/all.xml",
]

APP_BASE_URL = "https://your-streamlit-app-url.streamlit.app"

# TODO: move Bark endpoint/key to Streamlit secrets or environment variables.
BARK_URL = "https://api.day.app/fCipZZrf7xYwdxiqnVD8Ga/"

MAX_ARTICLES = 120

SCORING_WEIGHTS = {
    "banking": 0.28,
    "sre_ops": 0.24,
    "ai_adoption": 0.24,
    "governance": 0.16,
    "infra_agents": 0.08,
}

KEYWORDS = {
    "banking": [
        "bank", "banking", "capital markets", "equity", "derivatives", "trading",
        "risk", "compliance", "fraud", "regtech", "fintech", "payment", "asset management",
        "financial services", "investment bank", "market infrastructure", "clearing",
    ],
    "sre_ops": [
        "sre", "production", "incident", "observability", "monitoring", "reliability",
        "latency", "outage", "runbook", "on-call", "operations", "support", "root cause",
        "postmortem", "availability", "resilience", "service level", "alert",
    ],
    "ai_adoption": [
        "enterprise ai", "copilot", "llm", "genai", "automation", "workflow",
        "adoption", "deployment", "pilot", "scaling", "transformation", "productivity",
        "use case", "assistant", "agentic",
    ],
    "governance": [
        "governance", "regulation", "regulatory", "model risk", "controls", "audit",
        "policy", "compliance", "security", "privacy", "data protection", "explainability",
        "risk management", "ai act",
    ],
    "infra_agents": [
        "agent", "orchestration", "vector", "rag", "inference", "gpu", "serving",
        "platform", "mlops", "benchmark", "framework", "open source", "tooling",
    ],
    "deprioritize": [
        "celebrity", "lifestyle", "gaming", "entertainment", "rumor", "gossip", "opinion",
        "seed funding", "series a", "series b", "valuation", "benchmark leaderboard",
        "sponsored", "press release",
    ],
}
