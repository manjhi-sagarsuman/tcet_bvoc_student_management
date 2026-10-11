from html.parser import HTMLParser
from urllib.request import Request, urlopen
import re

OFFICIAL_URLS = [
    "https://www.tcetmumbai.in/bvoc-enquiry.html",
    "https://admission.tcetmumbai.in/bvoc.php",
]
DEFAULT_BRANCHES = [
    "B.Voc Artificial Intelligence and Data Science",
    "B.Voc Software Development",
    "B.Voc Animation and Graphic Designing",
    "B.Voc Data Analytics",
    "B.Voc Data Science",
    "B.Voc Artificial Intelligence",
]

class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, data):
        clean = " ".join(data.split())
        if clean:
            self.parts.append(clean)

def fetch_official_branches(timeout=6):
    """Fetch public page text and identify listed B.Voc programme names.
    Returns a list of branch names; raises RuntimeError if no reliable match is found.
    """
    found = set()
    for url in OFFICIAL_URLS:
        try:
            request = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; BVoCStudentManager/1.0)"})
            with urlopen(request, timeout=timeout) as response:
                raw = response.read().decode("utf-8", errors="ignore")
            parser = _TextExtractor()
            parser.feed(raw)
            text = " ".join(parser.parts)
            # Use known official course names, accepting common variants.
            candidates = [
                ("Artificial Intelligence and Data Science", r"Artificial Intelligence\s*(?:and|&)\s*Data Science"),
                ("Software Development", r"Software Development"),
                ("Animation and Graphic Designing", r"Animation\s*(?:and|&)\s*Graphic Designing?"),
                ("Data Analytics", r"Data Analytics"),
                ("Data Science", r"(?<!and )Data Science"),
                ("Artificial Intelligence", r"(?<!and )Artificial Intelligence"),
            ]
            for label, pattern in candidates:
                if re.search(pattern, text, flags=re.I):
                    found.add("B.Voc " + label)
        except Exception:
            continue
    if not found:
        raise RuntimeError("Could not fetch branch names from TCET right now. The bundled official branch list is still available.")
    # Keep stable order and avoid displaying both combined branch and its substring variants incorrectly.
    return [b for b in DEFAULT_BRANCHES if b in found]
