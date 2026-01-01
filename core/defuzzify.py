from core.model import QSFSNumber
import math


TPI = 2 * math.pi

def qsfs_def(x: QSFSNumber) -> float:
    a = x.dx + x.dz * (x.dx / (x.dx + x.dy))
    b = (x.ax / TPI) + (x.by / TPI) * (
        (x.ax / TPI) / ((x.ax / TPI) + (x.cz / TPI))
    )
    return round(a + b, 5)
