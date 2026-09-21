#!/usr/bin/env python3
"""Fetch recent papers from the arXiv API and print compact, LLM-friendly lines.

Usage:
  python fetch_arxiv.py "multi-agent orchestration" [--max 15] [--sort relevance|lastUpdatedDate|submittedDate]

Exit code 0 on success; errors are printed on a single line to stderr.
"""
import argparse
import ssl
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

NS = {"a": "http://www.w3.org/2005/Atom"}
API = "https://export.arxiv.org/api/query"


def make_context():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def build_query(topic: str) -> str:
    words = " AND ".join(f'all:"{w}"' for w in topic.split() if w)
    return words or f'all:"{topic}"'


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("topic")
    p.add_argument("--max", type=int, default=15)
    p.add_argument("--sort", default="relevance",
                   choices=["relevance", "lastUpdatedDate", "submittedDate"])
    args = p.parse_args()

    params = urllib.parse.urlencode({
        "search_query": build_query(args.topic),
        "start": 0,
        "max_results": min(args.max, 50),
        "sortBy": args.sort,
        "sortOrder": "descending",
    })
    try:
        with urllib.request.urlopen(f"{API}?{params}", timeout=30, context=make_context()) as r:
            root = ET.fromstring(r.read())
    except Exception as e:
        print(f"ERROR: arXiv request failed: {e}", file=sys.stderr)
        return 1

    entries = root.findall("a:entry", NS)
    if not entries:
        print("NO RESULTS — try broader keywords (e.g. 'language model agents').")
        return 0

    for e in entries:
        title = " ".join(e.findtext("a:title", "", NS).split())
        date = e.findtext("a:published", "", NS)[:10]
        link = e.findtext("a:id", "", NS).replace("http://arxiv.org/abs/", "https://arxiv.org/abs/")
        authors = [a.findtext("a:name", "", NS) for a in e.findall("a:author", NS)]
        astr = ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else "")
        abstract = " ".join(e.findtext("a:summary", "", NS).split())[:280]
        cats = ", ".join(c.get("term") for c in e.findall("a:category", NS)[:3])
        print(f"[{date}] {title}\n  {astr} | {cats}\n  {link}\n  {abstract}\n")
    print(f"--- {len(entries)} results for: {args.topic}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
