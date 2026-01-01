import re
from core.model import QSFSNumber

_PATTERN = re.compile(
    r"""
    \(\s*
    ([0-9.,]+)\s*e\s*j\s*2\s*p\s*([0-9.,]+)\s*;\s*
    ([0-9.,]+)\s*e\s*j\s*2\s*p\s*([0-9.,]+)\s*;\s*
    ([0-9.,]+)\s*e\s*j\s*2\s*p\s*([0-9.,]+)
    \s*\)
    """,
    re.VERBOSE | re.IGNORECASE
)

def parse_qsfs(text: str) -> QSFSNumber:
    """
    Strict format:
    (0.4ej2p0.4; 0.31623ej2p0.25; 0.86023ej2p0.35)
    """
    m = _PATTERN.fullmatch(text.replace("π", "p").replace("·", "").strip())
    if not m:
        raise ValueError(
            "Wrong Format.\n"
            "Corect Format: (0.4ej2p0.4; 0.3ej2p0.2; 0.8ej2p0.3)"
        )

    nums = [float(x.replace(",", ".")) for x in m.groups()]
    qsfs = QSFSNumber(*nums)

    return qsfs
