def review_paper(paper):
    """Create a short review of a research paper."""

    title = paper.get("title", "Untitled")
    summary = paper.get("summary", "")

    return {
        "title": title,
        "review": summary[:300],
        "link": paper.get("link", "")
    }