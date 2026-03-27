"""Rules-based analysis and personalization for AI Finance Radar."""

from __future__ import annotations

from collections import Counter
from typing import Any

from config import APP_BASE_URL, KEYWORDS, SCORING_WEIGHTS


def _count_keywords(text: str, words: list[str]) -> int:
    lowered = text.lower()
    return sum(1 for w in words if w in lowered)


def _cap(value: float, upper: int = 100) -> int:
    return max(0, min(int(round(value)), upper))


def infer_category(text: str) -> str:
    mapping = {
        "Banking AI": KEYWORDS["banking"],
        "AI Ops / SRE": KEYWORDS["sre_ops"],
        "AI Governance": KEYWORDS["governance"],
        "AI Engineering": KEYWORDS["infra_agents"],
        "Enterprise Adoption": KEYWORDS["ai_adoption"],
    }
    best_category = "General AI/Finance"
    best_score = -1
    for cat, words in mapping.items():
        score = _count_keywords(text, words)
        if score > best_score:
            best_score = score
            best_category = cat
    return best_category


def build_one_line_takeaway(title: str, category: str) -> str:
    return f"{category}: {title[:140]}"


def build_spotlight_cn(title: str, attention_flag: str, category: str) -> str:
    prefix = {
        "HIGH ATTENTION": "【高优先】",
        "WATCH": "【关注】",
        "LOW PRIORITY": "【低优先】",
    }.get(attention_flag, "【关注】")
    return f"{prefix}{category}：{title[:50]}。建议聚焦对银行科技与生产支持的实际影响。"


def build_why_matters(category: str) -> str:
    reasons = {
        "Banking AI": "This may shift banking technology priorities, vendor strategy, and regulatory expectations.",
        "AI Ops / SRE": "This can improve incident response, reliability engineering workflows, and operational resilience.",
        "AI Governance": "This informs model risk, controls, and audit readiness for enterprise AI rollout.",
        "AI Engineering": "This impacts AI platform choices, integration patterns, and engineering productivity.",
        "Enterprise Adoption": "This provides practical patterns for scaling AI usage in large organizations.",
    }
    return reasons.get(category, "This can influence practical enterprise AI decisions.")


def build_why_for_profile(category: str, title: str) -> str:
    return (
        f"For your banking SRE + Equity Derivatives support profile, this {category.lower()} signal can "
        f"guide where to focus AI upskilling and production-readiness actions: {title[:90]}."
    )


def attention_flag(score: int) -> str:
    if score >= 75:
        return "HIGH ATTENTION"
    if score >= 50:
        return "WATCH"
    return "LOW PRIORITY"


def urgency_level(score: int) -> str:
    if score >= 75:
        return "HIGH"
    if score >= 50:
        return "MEDIUM"
    return "LOW"


def suggested_action(category: str, score: int) -> str:
    if score >= 75:
        return "Review today, assess impact on production support runbooks, and share a short internal note."
    if category == "AI Governance":
        return "Track control and model-risk implications; map to existing governance checkpoints."
    if category == "AI Ops / SRE":
        return "Test whether the approach can reduce MTTR, alert noise, or toil in your on-call workflow."
    return "Add to weekly learning backlog and monitor for concrete enterprise adoption examples."


def score_article(article: dict[str, Any]) -> dict[str, Any]:
    text = f"{article['title']} {article.get('summary', '')}".lower()

    banking_raw = _count_keywords(text, KEYWORDS["banking"])
    sre_raw = _count_keywords(text, KEYWORDS["sre_ops"])
    adoption_raw = _count_keywords(text, KEYWORDS["ai_adoption"])
    governance_raw = _count_keywords(text, KEYWORDS["governance"])
    infra_raw = _count_keywords(text, KEYWORDS["infra_agents"])
    deprioritize_raw = _count_keywords(text, KEYWORDS["deprioritize"])

    banking_score = _cap(banking_raw * 14)
    sre_score = _cap(sre_raw * 16)
    ai_adoption_score = _cap((adoption_raw + infra_raw) * 12)

    weighted = (
        banking_score * SCORING_WEIGHTS["banking"]
        + sre_score * SCORING_WEIGHTS["sre_ops"]
        + ai_adoption_score * SCORING_WEIGHTS["ai_adoption"]
        + _cap(governance_raw * 15) * SCORING_WEIGHTS["governance"]
        + _cap(infra_raw * 10) * SCORING_WEIGHTS["infra_agents"]
    )

    final_score = _cap(weighted - deprioritize_raw * 12)
    category = infer_category(text)
    flag = attention_flag(final_score)

    article = {**article}
    article.update(
        {
            "category": category,
            "one_line_takeaway_en": build_one_line_takeaway(article["title"], category),
            "relevance_score": final_score,
            "banking_relevance_score": banking_score,
            "sre_ops_relevance_score": sre_score,
            "ai_adoption_relevance_score": ai_adoption_score,
            "urgency_level": urgency_level(final_score),
            "attention_flag": flag,
            "why_it_matters": build_why_matters(category),
            "why_it_matters_for_me": build_why_for_profile(category, article["title"]),
            "suggested_action": suggested_action(category, final_score),
        }
    )
    article["spotlight_cn"] = build_spotlight_cn(article["title"], flag, category)
    article["detail_link"] = f"{APP_BASE_URL}/?item_id={article['id']}"
    return article


def analyze_articles(raw_articles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    analyzed = [score_article(a) for a in raw_articles]
    analyzed.sort(key=lambda x: (x["relevance_score"], x["published"]), reverse=True)
    return analyzed


def trends_to_watch(items: list[dict[str, Any]], top_n: int = 3) -> list[str]:
    top = items[:20]
    if not top:
        return ["No trends available yet."]

    tokens: Counter[str] = Counter()
    trend_words = [
        "governance", "risk", "compliance", "agent", "inference", "banking", "trading",
        "observability", "incident", "copilot", "regulation", "fraud", "operations",
    ]
    for item in top:
        text = f"{item['title']} {item.get('summary', '')}".lower()
        for word in trend_words:
            if word in text:
                tokens[word] += 1

    common = [word for word, _ in tokens.most_common(top_n)]
    if not common:
        return [
            "Enterprise AI adoption patterns are accelerating across finance and operations.",
            "AI governance and control themes continue to rise in importance.",
            "Production-ready AI tooling is becoming a practical differentiator.",
        ][:top_n]

    return [f"Rising signal: {word} appears repeatedly across top articles." for word in common]


def build_daily_digest(items: list[dict[str, Any]], max_items: int = 5) -> tuple[str, str, str]:
    top_items = items[:max_items]
    if not top_items:
        return (
            "AI Finance Radar | Daily Spotlight",
            "No strong signal found today. Please check the dashboard for new updates.",
            APP_BASE_URL,
        )

    lines: list[str] = []
    for idx, item in enumerate(top_items[:5], start=1):
        line = (
            f"{idx}. {item['spotlight_cn']} | {item['one_line_takeaway_en'][:80]} | "
            f"{item['why_it_matters_for_me'][:70]}"
        )
        lines.append(line)

    url = top_items[0].get("detail_link") or APP_BASE_URL
    body = "\n".join(lines)
    return "AI Finance Radar | Daily Spotlight", body, url
