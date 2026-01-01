class QSFSNumber:
    """
    QSFS = (
        (δx, ax),
        (δy, by),
        (δz, cz)
    )
    phase a,b,c ∈ [0,1]  (chuẩn hóa theo paper)
    """

    def __init__(self, dx, ax, dy, by, dz, cz):
        self.dx = dx
        self.ax = ax
        self.dy = dy
        self.by = by
        self.dz = dz
        self.cz = cz

    def __str__(self):
        return (
            f"({self.dx:.5f}ej2p{self.ax:.5f}; "
            f"{self.dy:.5f}ej2p{self.by:.5f}; "
            f"{self.dz:.5f}ej2p{self.cz:.5f})"
        )
