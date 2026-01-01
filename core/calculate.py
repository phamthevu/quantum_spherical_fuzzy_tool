import math
from core.model import QSFSNumber


TPI = 2 * math.pi

def qsfs_add(x: QSFSNumber, y: QSFSNumber) -> QSFSNumber:
    dx = math.sqrt(
        x.dx**2 + y.dx**2 - x.dx**2 * y.dx**2
    )

    ax = math.sqrt(
        (x.ax / TPI) ** 2
        + (y.ax / TPI) ** 2
        - (x.ax / TPI) ** 2 * (y.ax / TPI) ** 2
    )

    dy = x.dy * y.dy
    by = (x.by / TPI) * (y.by / TPI)

    dz = math.sqrt(
        (1 - y.dx**2) * x.dz**2
        + (1 - x.dx**2) * y.dz**2
        - x.dz**2 * y.dz**2
    )

    cz = math.sqrt(
        (1 - (y.ax / TPI) ** 2) * (x.cz / TPI) ** 2
        + (1 - (x.ax / TPI) ** 2) * (y.cz / TPI) ** 2
        - (x.cz / TPI) ** 2 * (y.cz / TPI) ** 2
    )

    return QSFSNumber(dx, ax, dy, by, dz, cz)

def qsfs_mul(x: QSFSNumber, y: QSFSNumber) -> QSFSNumber:
    dx = x.dx * y.dx
    ax = (x.ax / TPI) * (y.ax / TPI)

    dy = math.sqrt(
        x.dy**2 + y.dy**2 - x.dy**2 * y.dy**2
    )

    by = math.sqrt(
        (x.by / TPI) ** 2
        + (y.by / TPI) ** 2
        - (x.by / TPI) ** 2 * (y.by / TPI) ** 2
    )

    dz = math.sqrt(
        (1 - y.dy**2) * x.dz**2
        + (1 - x.dy**2) * y.dz**2
        - x.dz**2 * y.dz**2
    )

    cz = math.sqrt(
        (1 - (y.by / TPI) ** 2) * (x.cz / TPI) ** 2
        + (1 - (x.by / TPI) ** 2) * (y.cz / TPI) ** 2
        - (x.cz / TPI) ** 2 * (y.cz / TPI) ** 2
    )

    return QSFSNumber(dx, ax, dy, by, dz, cz)



def qsfs_coe(x: QSFSNumber, k: float) -> QSFSNumber:
    dx = math.sqrt(1 - (1 - x.dx**2) ** k)
    ax = math.sqrt(1 - (1 - (x.ax / TPI) ** 2) ** k)

    dy = x.dy ** k
    by = (x.by / TPI) ** k

    a = (1 - x.dz**2) ** k
    b = (1 - x.dx**2 - x.dz**2) ** k
    dz = math.sqrt(a - b)

    a = (1 - (x.cz / TPI) ** 2) ** k
    b = (1 - (x.ax / TPI) ** 2 - (x.cz / TPI) ** 2) ** k
    cz = math.sqrt(a - b)

    return QSFSNumber(dx, ax, dy, by, dz, cz)

def qsfs_pow(x: QSFSNumber, k: float) -> QSFSNumber:
    dx = x.dx ** k
    ax = (x.ax / TPI) ** k

    dy = math.sqrt(1 - (1 - x.dy**2) ** k)
    by = math.sqrt(1 - (1 - (x.by / TPI) ** 2) ** k)

    dz = math.sqrt(
        (1 - x.dy**2) ** k
        - (1 - x.dy**2 - x.dz**2) ** k
    )

    cz = math.sqrt(
        (1 - (x.by / TPI) ** 2) ** k
        - (1 - (x.by / TPI) ** 2 - (x.cz / TPI) ** 2) ** k
    )

    return QSFSNumber(dx, ax, dy, by, dz, cz)

