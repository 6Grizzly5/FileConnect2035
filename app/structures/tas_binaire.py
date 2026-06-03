import heapq


class TasBinaire:

    def __init__(self):

        self.heap = []

    # -------------------------
    # AJOUT
    # -------------------------

    def inserer(self, priorite, ticket):

        heapq.heappush(
            self.heap,
            (priorite, ticket)
        )

    # -------------------------
    # EXTRACTION MIN
    # -------------------------

    def extraire_min(self):

        if not self.heap:
            return None

        return heapq.heappop(self.heap)

    # -------------------------
    # VERIFIER SI VIDE
    # -------------------------

    def est_vide(self):

        return len(self.heap) == 0