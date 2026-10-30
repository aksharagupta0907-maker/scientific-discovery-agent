
import requests
import xml.etree.ElementTree as ET


BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def fetch_pubmed_papers(query="machine learning", max_results=5):
    """Fetch research paper metadata from PubMed."""

    search_url = BASE_URL + "esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
    }

    response = requests.get(
        search_url,
        params=search_params,
        timeout=30,
    )
    response.raise_for_status()

    paper_ids = response.json()["esearchresult"]["idlist"]

    if not paper_ids:
        print("No PubMed papers found.")
        return []

    fetch_url = BASE_URL + "efetch.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml",
    }

    response = requests.get(
        fetch_url,
        params=fetch_params,
        timeout=30,
    )
    response.raise_for_status()

    root = ET.fromstring(response.text)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        title_element = article.find(
            ".//ArticleTitle"
        )
        abstract_elements = article.findall(
            ".//Abstract/AbstractText"
        )
        pmid_element = article.find(".//PMID")

        papers.append({
            "source": "PubMed",
            "paper_id": (
                pmid_element.text
                if pmid_element is not None
                else ""
            ),
            "title": (
                "".join(title_element.itertext())
                if title_element is not None
                else ""
            ),
            "abstract": " ".join(
                "".join(element.itertext())
                for element in abstract_elements
            ),
        })

    return papers


if __name__ == "__main__":
    results = fetch_pubmed_papers()

    print(f"PubMed papers fetched: {len(results)}")

    for paper in results:
        print("-", paper["title"])
