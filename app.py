from __future__ import annotations

from datetime import datetime

import streamlit as st

from analyzer import analyze_articles, build_daily_digest, trends_to_watch
from config import APP_BASE_URL
from notifier import push_bark
from rss_fetcher import fetch_articles

st.set_page_config(page_title="AI Finance Radar", page_icon="📡", layout="wide")


@st.cache_data(ttl=900)
def load_signals() -> list[dict]:
    return analyze_articles(fetch_articles())


def format_date(ts: str) -> str:
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return ts


def render_item_card(item: dict, expanded: bool = False) -> None:
    st.markdown(f"### {item['title']}")
    st.caption(
        f"{item['source']} | {format_date(item['published'])} | {item['category']} | "
        f"{item['attention_flag']} | Urgency: {item['urgency_level']}"
    )
    st.write(f"**Takeaway:** {item['one_line_takeaway_en']}")
    st.success(f"**中文聚焦:** {item['spotlight_cn']}")
    st.info(f"**Why it matters for me:** {item['why_it_matters_for_me']}")
    st.markdown(f"[Original Article]({item['link']}) · [Detail Link in App]({item['detail_link']})")

    with st.expander("Details", expanded=expanded):
        st.write(f"**Why it matters:** {item['why_it_matters']}")
        st.write(f"**Suggested action:** {item['suggested_action']}")
        st.write(
            "**Scores:** "
            f"Overall={item['relevance_score']}, "
            f"Banking={item['banking_relevance_score']}, "
            f"SRE/Ops={item['sre_ops_relevance_score']}, "
            f"AI Adoption={item['ai_adoption_relevance_score']}"
        )


def sidebar_actions(items: list[dict]) -> None:
    st.sidebar.header("Notifications")
    st.sidebar.write(f"APP_BASE_URL: `{APP_BASE_URL}`")

    if st.sidebar.button("Test Bark Push"):
        ok, msg = push_bark(
            title="AI Finance Radar | Test",
            body="Bark test notification from AI Finance Radar.",
            url=APP_BASE_URL,
        )
        (st.sidebar.success if ok else st.sidebar.warning)(msg)

    if st.sidebar.button("Send Sample Spotlight"):
        title, body, url = build_daily_digest(items[:5], max_items=3)
        ok, msg = push_bark(title=title, body=body, url=url)
        (st.sidebar.success if ok else st.sidebar.warning)(msg)


def main() -> None:
    st.title("📡 AI Finance Radar")
    st.caption(
        "Personalized AI strategic radar for banking technology, SRE, and Equity Derivatives production support."
    )

    items = load_signals()
    sidebar_actions(items)

    if not items:
        st.warning("No RSS items available right now. Please try again later.")
        return

    item_id = st.query_params.get("item_id")
    if item_id:
        selected = next((i for i in items if i["id"] == item_id), None)
        if selected:
            st.subheader("Detail View")
            render_item_card(selected, expanded=True)
            st.divider()
        else:
            st.warning("Requested item not found. Showing latest signals.")

    top_signals = items[:5]
    especially_for_you = [x for x in items if x["attention_flag"] == "HIGH ATTENTION"][:5]

    st.subheader("Top Signals Today")
    for item in top_signals:
        render_item_card(item)
        st.divider()

    st.subheader("Especially Important For You")
    for item in especially_for_you or top_signals[:3]:
        render_item_card(item)
        st.divider()

    st.subheader("All Signals")
    for item in items[:25]:
        with st.container(border=True):
            st.markdown(
                f"**{item['title']}**  \n"
                f"`{item['attention_flag']}` · `{item['urgency_level']}` · {item['source']}  \n"
                f"{item['spotlight_cn']}  \n"
                f"[Original]({item['link']}) | [Detail]({item['detail_link']})"
            )

    st.subheader("Trends To Watch")
    for trend in trends_to_watch(items, top_n=3):
        st.write(f"- {trend}")


if __name__ == "__main__":
    main()
