class GrapheGuichets:

    def __init__(self):

        self.graphe = {}

    # -------------------------
    # AJOUTER SOMMET
    # -------------------------

    def ajouter_guichet(self, guichet):

        if guichet not in self.graphe:

            self.graphe[guichet] = []

    # -------------------------
    # AJOUTER CONNEXION
    # -------------------------

    def connecter(self, g1, g2):

        self.graphe[g1].append(g2)

        self.graphe[g2].append(g1)

    # -------------------------
    # AFFICHAGE
    # -------------------------

    def afficher(self):

        return self.graphe