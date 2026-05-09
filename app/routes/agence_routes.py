from flask import Blueprint, jsonify

from app.services.qr_generator import generer_qr

agence_bp = Blueprint('agence_bp', __name__)

@agence_bp.route('/generer_qr', methods=['GET'])
def create_qr():

    url = 'http://127.0.0.1:5000/'

    chemin = generer_qr(url, 'smartqueue_qr')

    return jsonify({
        'message': 'QR Code généré',
        'fichier': chemin
    })
    
from flask import request

from app import db
from app.models.agence import Agence

@agence_bp.route('/agence', methods=['POST'])
def creer_agence():

    data = request.get_json()

    agence = Agence(
        nom=data['nom'],
        type=data['type'],
        adresse=data['adresse']
    )

    db.session.add(agence)
    db.session.commit()

    return jsonify({
        'message': 'Agence créée',
        'id_agence': agence.id_agence
    }), 201
    
@agence_bp.route('/check_agence', methods=['GET'])
def check_agence():

    agence = Agence.query.first()

    return jsonify({
        'configured': agence is not None
    })