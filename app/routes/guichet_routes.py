from flask import Blueprint, request, jsonify, render_template

from app import db

from app.models.guichet import Guichet
from app.models.agence import Agence


guichet_bp = Blueprint(
    'guichet_bp',
    __name__
)


# ─────────────────────────────
# CREATE GUICHET
# ─────────────────────────────

@guichet_bp.route(
    '/create_guichet',
    methods=['POST']
)
def create_guichet():

    try:

        data = request.get_json()

        nombre = data.get('nombre')
        id_agence = data.get('id_agence')

        if not nombre:

            return jsonify({
                'error': 'Nombre requis'
            }), 400

        guichets_crees = []

        for i in range(1, nombre + 1):

            guichet = Guichet(
                numero=i,
                statut='disponible',
                id_agence=id_agence
            )

            db.session.add(guichet)

            guichets_crees.append(i)

        db.session.commit()

        return jsonify({
            'message': 'Guichets créés',
            'guichets': guichets_crees
        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({
            'error': str(e)
        }), 500


# ─────────────────────────────
# ADD ONE GUICHET
# ─────────────────────────────

@guichet_bp.route(
    '/add_guichet',
    methods=['POST']
)
def add_guichet():

    try:

        data = request.get_json()

        id_agence = data.get('id_agence')

        # RECUP DERNIER NUMERO
        dernier_guichet = (
            Guichet.query
            .order_by(Guichet.numero.desc())
            .first()
        )

        if dernier_guichet:

            nouveau_numero = (
                dernier_guichet.numero + 1
            )

        else:

            nouveau_numero = 1

        # CREATE
        guichet = Guichet(
            numero=nouveau_numero,
            statut='disponible',
            id_agence=id_agence
        )

        db.session.add(guichet)

        db.session.commit()

        return jsonify({

            'message': 'Guichet ajouté',

            'guichet': {
                'id': guichet.id,
                'numero': guichet.numero,
                'statut': guichet.statut
            }

        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({
            'error': str(e)
        }), 500


# ─────────────────────────────
# GET GUICHETS
# ─────────────────────────────

@guichet_bp.route(
    '/guichets',
    methods=['GET']
)
def get_guichets():

    try:

        guichets = Guichet.query.all()

        result = []

        for g in guichets:

            result.append({
                'id': g.id,
                'numero': g.numero,
                'statut': g.statut,
                'id_agence': g.id_agence
            })

        return jsonify(result)

    except Exception as e:

        return jsonify({
            'error': str(e)
        }), 500


# ─────────────────────────────
# UPDATE STATUS
# ─────────────────────────────

@guichet_bp.route(
    '/guichet/<int:id>/status',
    methods=['PUT']
)
def update_guichet_status(id):

    try:

        guichet = Guichet.query.get(id)

        if not guichet:

            return jsonify({
                'error': 'Guichet introuvable'
            }), 404

        data = request.get_json()

        guichet.statut = data.get(
            'statut',
            guichet.statut
        )

        db.session.commit()

        return jsonify({
            'message': 'Statut mis à jour'
        })

    except Exception as e:

        db.session.rollback()

        return jsonify({
            'error': str(e)
        }), 500


# ─────────────────────────────
# DELETE GUICHET
# ─────────────────────────────

@guichet_bp.route(
    '/guichet/<int:id>',
    methods=['DELETE']
)
def delete_guichet(id):

    try:

        guichet = Guichet.query.get(id)

        if not guichet:

            return jsonify({
                'error': 'Guichet introuvable'
            }), 404

        db.session.delete(guichet)

        db.session.commit()

        return jsonify({
            'message': 'Guichet supprimé'
        })

    except Exception as e:

        db.session.rollback()

        return jsonify({
            'error': str(e)
        }), 500
        
# ─────────────────────────────
# WEB INTERFACE GUICHET
# ─────────────────────────────

@guichet_bp.route(
    '/guichet/<int:id_agence>/<int:id_guichet>'
)
def guichet_interface(
    id_agence,
    id_guichet
):

    guichet = Guichet.query.filter_by(
        id=id_guichet,
        id_agence=id_agence
    ).first()

    if not guichet:

        return "Guichet introuvable", 404

    return render_template(
        'guichet.html',
        guichet=guichet
    )