import math
from core.model import QSFSNumber

TPI = 2 * math.pi


def qsfs_agg(items: list[QSFSNumber]) -> QSFSNumber:
    if not items:
        raise ValueError("Empty QSFS list")

    k = len(items)

    # ---------- U (membership) ----------
    ucc = (1 - items[0].dx**2) ** (1 / k)
    for i in range(1, k):
        ucc *= (1 - items[i].dx**2) ** (1 / k)
    ucc = math.sqrt(1 - ucc)

    uec = (1 - (items[0].ax / TPI) ** 2) ** (1 / k)
    for i in range(1, k):
        uec *= (1 - (items[i].ax / TPI) ** 2) ** (1 / k)
    uec = math.sqrt(1 - uec)

    # ---------- V (non-membership) ----------
    vcc = items[0].dy ** (1 / k)
    for i in range(1, k):
        vcc *= items[i].dy ** (1 / k)

    vec = (items[0].by / TPI) ** (1 / k)
    for i in range(1, k):
        vec *= (items[i].by / TPI) ** (1 / k)

    # ---------- H (hesitation) ----------
    a = (1 - items[0].dx**2) ** (1 / k)
    b = (1 - items[0].dx**2 - items[0].dz**2) ** (1 / k)
    for i in range(1, k):
        a *= (1 - items[i].dx**2) ** (1 / k)
        b *= (1 - items[i].dx**2 - items[i].dz**2) ** (1 / k)
    hcc = math.sqrt(a - b)

    a = (1 - (items[0].ax / TPI) ** 2) ** (1 / k)
    b = (1 - (items[0].ax / TPI) ** 2 - (items[0].cz / TPI) ** 2) ** (1 / k)
    for i in range(1, k):
        a *= (1 - (items[i].ax / TPI) ** 2) ** (1 / k)
        b *= (
            1
            - (items[i].ax / TPI) ** 2
            - (items[i].cz / TPI) ** 2
        ) ** (1 / k)
    hec = math.sqrt(a - b)

    return QSFSNumber(ucc, uec, vcc, vec, hcc, hec)

def qsfs_aggw(
    items: list[QSFSNumber],
    weights: list[float]
) -> QSFSNumber:

    if not items:
        raise ValueError("Empty QSFS list")

    if len(items) != len(weights):
        raise ValueError("Items and weights length mismatch")

    # ---------- U ----------
    ucc = (1 - items[0].dx**2) ** weights[0]
    for i in range(1, len(items)):
        ucc *= (1 - items[i].dx**2) ** weights[i]
    ucc = math.sqrt(1 - ucc)

    uec = (1 - (items[0].ax / TPI) ** 2) ** weights[0]
    for i in range(1, len(items)):
        uec *= (1 - (items[i].ax / TPI) ** 2) ** weights[i]
    uec = math.sqrt(1 - uec)

    # ---------- V ----------
    vcc = items[0].dy ** weights[0]
    for i in range(1, len(items)):
        vcc *= items[i].dy ** weights[i]

    vec = (items[0].by / TPI) ** weights[0]
    for i in range(1, len(items)):
        vec *= (items[i].by / TPI) ** weights[i]

    # ---------- H ----------
    a = (1 - items[0].dx**2) ** weights[0]
    b = (1 - items[0].dx**2 - items[0].dz**2) ** weights[0]
    for i in range(1, len(items)):
        a *= (1 - items[i].dx**2) ** weights[i]
        b *= (1 - items[i].dx**2 - items[i].dz**2) ** weights[i]
    hcc = math.sqrt(a - b)

    a = (1 - (items[0].ax / TPI) ** 2) ** weights[0]
    b = (
        1
        - (items[0].ax / TPI) ** 2
        - (items[0].cz / TPI) ** 2
    ) ** weights[0]
    for i in range(1, len(items)):
        a *= (1 - (items[i].ax / TPI) ** 2) ** weights[i]
        b *= (
            1
            - (items[i].ax / TPI) ** 2
            - (items[i].cz / TPI) ** 2
        ) ** weights[i]
    hec = math.sqrt(a - b)

    return QSFSNumber(ucc, uec, vcc, vec, hcc, hec)
