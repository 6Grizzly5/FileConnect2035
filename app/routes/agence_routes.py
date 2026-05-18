from flask import Blueprint, jsonify, request

from app import db

from app.models.agence import Agence
from app.models.service import Service
from app.models.ticket import Ticket
from app.models.notification import Notification

from app.services.qr_generator import generer_qr


agence_bp = Blueprint('agence_bp', __name__)


# ─────────────────────────────
# GENERER QR TEST
# ─────────────────────────────

@agence_bp.route('/generer_qr', methods=['GET'])
def create_qr():

    url = 'http://127.0.0.1:5000/'

    chemin = generer_qr(
        url,
        'smartqueue_qr'
    )

    return jsonify({
        'message': 'QR Code généré',
        'fichier': chemin
    })


# ─────────────────────────────
# CREATE AGENCE
# ─────────────────────────────

@agence_bp.route('/create_agence', methods=['POST'])
def creer_agence():

    try:

        data = request.get_json()

        agence = Agence(
            nom=data['nom'],
            type=data['type'],
            ville=data.get('ville', ''),
            telephone=data.get('telephone', ''),
            adresse=data.get('adresse', '')
        )

        # SAVE BDD
        db.session.add(agence)
        db.session.commit()

        # =========================
        # GENERATION QR
        # =========================

        url = f"http://192.168.43.26:5000/mobile/{agence.id}"

        filename = f"agence_{agence.id}"

        chemin_qr = generer_qr(
            url,
            filename
        )

        # SAVE QR NAME
        agence.qr_image = f"{filename}.png"

        db.session.commit()

        return jsonify({
            'message': 'Agence créée',
            'id_agence': agence.id,
            'qr_code': chemin_qr
        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({
            'error': str(e)
        }), 500


# ─────────────────────────────
# CHECK AGENCE
# ─────────────────────────────

@agence_bp.route('/check_agence', methods=['GET'])
def check_agence():

    agence = Agence.query.first()

    return jsonify({
        'configured': agence is not None
    })


# ─────────────────────────────
# GET AGENCE
# ─────────────────────────────

@agence_bp.route('/get_agence', methods=['GET'])
def get_agence():

    agence = Agence.query.first()

    if not agence:

        return jsonify({
            'error': 'Aucune agence'
        }), 404

    return jsonify({
        'id': agence.id,
        'nom': agence.nom,
        'type': agence.type,
        'ville': agence.ville,
        'telephone': agence.telephone,
        'adresse': agence.adresse,
        'qr_image': agence.qr_image
    })


# ─────────────────────────────
# UPDATE AGENCE
# ─────────────────────────────

@agence_bp.route('/update_agence', methods=['PUT'])
def update_agence():

    agence = Agence.query.first()

    if not agence:

        return jsonify({
            'error': 'Aucune agence'
        }), 404

    data = request.get_json()

    agence.nom = data.get('nom', agence.nom)
    agence.type = data.get('type', agence.type)
    agence.ville = data.get('ville', agence.ville)
    agence.telephone = data.get('telephone', agence.telephone)
    agence.adresse = data.get('adresse', agence.adresse)

    db.session.commit()

    return jsonify({
        'message': 'Agence mise à jour'
    })


# ─────────────────────────────
# RESET TICKETS
# ─────────────────────────────

@agence_bp.route('/reset_tickets', methods=['DELETE'])
def reset_tickets():

    try:

        Notification.query.delete()
        Ticket.query.delete()

        db.session.commit()

        return jsonify({
            'message': 'Tickets supprimés'
        })

    except Exception as e:

        db.session.rollback()

        return jsonify({
            'error': str(e)
        }), 500


# ─────────────────────────────
# DELETE AGENCE
# ─────────────────────────────

@agence_bp.route('/delete_agence', methods=['DELETE'])
def delete_agence():

    try:

        agence = Agence.query.first()

        if not agence:

            return jsonify({
                'error': 'Aucune agence'
            }), 404

        Notification.query.delete()
        Ticket.query.delete()
        Service.query.delete()

        db.session.delete(agence)

        db.session.commit()

        return jsonify({
            'message': 'Agence supprimée'
        })

    except Exception as e:

        db.session.rollback()

        return jsonify({
            'error': str(e)
        }), 500