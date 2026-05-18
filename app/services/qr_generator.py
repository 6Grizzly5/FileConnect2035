import qrcode

def generer_qr(url, nom_fichier):

    qr = qrcode.make(url)

    chemin = f'app/static/images/{nom_fichier}.png'

    qr.save(chemin)

    return chemin