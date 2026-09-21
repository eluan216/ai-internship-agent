from agent.loop import run_agent, build_query


def test_run_agent_demo_returns_markdown():
    md = run_agent(keywords=["machine learning", "internship"], limit=5, demo=True)
    assert md.startswith("# Internship shortlist")
    assert "Results:" in md


def test_run_agent_respects_limit():
    md = run_agent(keywords=["internship"], limit=2, demo=True)
    # count ## headings as result items
    headings = [line for line in md.splitlines() if line.startswith("## ")]
    assert len(headings) <= 2


def test_run_agent_zero_results():
    md = run_agent(keywords=["zzznomatchxyz"], limit=5, demo=True)
    assert "No matching listings" in md


def test_build_query_defaults():
    q = build_query()
    assert "internship" in q.keywords or "intern" in q.keywords
