import os, unicodedata, glob, logging
from difflib import SequenceMatcher
from typing import List, Dict, Any

# 1) calmer pdfminer
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# 2) ddg (renommé)
try:
    from ddgs import DDGS
    _DDGS = DDGS()
except Exception:
    _DDGS = None

def _norm(s: str) -> str:
    if not s: return ""
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return s.casefold().strip()

def _sim(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm(a), _norm(b)).ratio()

def _extract_text_first_pages(pdf_path: str, max_pages: int = 3) -> str:
    # Extraction robuste : si pdfminer échoue, on tente PyPDF2; sinon on ignore.
    try:
        from pdfminer.high_level import extract_text
        txt = extract_text(pdf_path, maxpages=max_pages)
        return txt or ""
    except Exception:
        try:
            from PyPDF2 import PdfReader
            r = PdfReader(pdf_path)
            if r.is_encrypted:
                try:
                    r.decrypt("")  # tentative sans mot de passe
                except Exception:
                    return ""      # crypté → ignorer
            out = []
            for p in r.pages[:max_pages]:
                try:
                    out.append(p.extract_text() or "")
                except Exception:
                    continue
            return "\n".join(out)
        except Exception:
            return ""  # fichier trop corrompu → ignorer proprement

def search_pdf_local(
    query: str | None,
    search_dirs: List[str] | None = None,
    search_in_contents: bool = False,
    filename_pattern: str = "*.pdf",
    max_results: int = 50,
    min_score: float = 0.35,
) -> Dict[str, Any]:
    search_dirs = search_dirs or ["/host/home"]
    files = []
    for d in search_dirs:
        root = os.path.expanduser(d)
        pattern = os.path.join(root, "**", filename_pattern)
        files.extend(glob.glob(pattern, recursive=True))
    files = list(dict.fromkeys(files))  # dédoublonner

    if not query:
        return {"status": "ok", "files_found": files[:max_results]}

    nq = _norm(query)
    ranked = sorted((( _sim(os.path.basename(p), nq), p) for p in files), reverse=True)
    best = [p for score, p in ranked if score >= min_score][:max_results]

    # Recherche contenu : ignorer silencieusement les PDFs “cassés”
    if search_in_contents and len(best) < max_results:
        for p in files:
            if p in best: continue
            text = _extract_text_first_pages(p, max_pages=3)
            if text and _norm(nq) in _norm(text):
                best.append(p)
            if len(best) >= max_results:
                break

    return {"status": "ok", "files_found": best[:max_results]}

# --- Web ---
import requests
from bs4 import BeautifulSoup

def search_pdf_web(query: str, max_results: int = 20) -> Dict[str, Any]:
    if not query:
        return {"status": "error", "message": "query manquante", "files_found": []}

    def _only_pdfs(urls): return [u for u in urls if isinstance(u,str) and u.lower().endswith(".pdf")]

    # 1) ddgs
    if _DDGS:
        urls = []
        try:
            for r in _DDGS.text(query, max_results=50, region="fr-fr", safesearch="off"):
                link = r.get("href") or r.get("link") or r.get("url")
                if link: urls.append(link)
        except Exception:
            urls = []
        pdfs = _only_pdfs(urls)
        if pdfs:
            return {"status": "ok", "files_found": pdfs[:max_results]}

        # retry sans accents
        q2 = _norm(query)
        if q2 != query:
            urls = []
            try:
                for r in _DDGS.text(q2, max_results=50, region="fr-fr", safesearch="off"):
                    link = r.get("href") or r.get("link") or r.get("url")
                    if link: urls.append(link)
            except Exception:
                pass
            pdfs = _only_pdfs(urls)
            if pdfs:
                return {"status": "ok", "files_found": pdfs[:max_results]}

    # 2) fallback HTML sobre (pas d’API)
    hdr = {"User-Agent": "Mozilla/5.0"}
    links = []
    try:
        resp = requests.get("https://duckduckgo.com/html/", params={"q": query}, headers=hdr, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        from urllib.parse import parse_qs, urlparse, unquote
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.lower().endswith(".pdf"):
                links.append(href)
            elif "duckduckgo.com/l/?uddg=" in href:
                qs = parse_qs(urlparse(href).query)
                real = qs.get("uddg", [None])[0]
                if real and real.lower().endswith(".pdf"):
                    links.append(unquote(real))
            if len(links) >= 50:
                break
    except Exception:
        pass

    return {"status": "ok", "files_found": links[:max_results]}

def search_pdf(query: str | None = None, source: str = "local",
               search_dirs: List[str] | None = None, search_in_contents: bool = False) -> Dict[str, Any]:
    if source == "web":
        return search_pdf_web(query or "")
    return search_pdf_local(query, search_dirs=search_dirs, search_in_contents=search_in_contents)

