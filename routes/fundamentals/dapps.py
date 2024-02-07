from flask import Blueprint, jsonify, request
from config import Session, DApps

dapps_bp = Blueprint('dappsRoutes', __name__)

@dapps_bp.route('/api/dapps', methods=['GET'])
def get_dapps():
    try:
        coin_bot_id = request.args.get('coin_bot_id')

        session = Session()
        dapps_data = session.query(DApps).filter_by(coin_bot_id=coin_bot_id).all()

        if not dapps_data:
            return {'error': 'No data found for the requested coinbot'}, 404

        dapps_list = [dapp.as_dict() for dapp in dapps_data]
        return jsonify({'message': dapps_list}), 200
    except Exception as e:
        return {'error': f'Error getting DApps data: {str(e)}'}, 500

@dapps_bp.route('/api/dapps/create', methods=['POST'])
def create_dapp():
    try:
        data = request.json
        coin_bot_id = data.get('coin_bot_id')

        new_dapp = DApps(
            dapps=data.get('dapps'),
            description=data.get('description'),
            tvl=data.get('tvl'),
            coin_bot_id=coin_bot_id
        )

        session = Session()
        session.add(new_dapp)
        session.commit()

        return {'message': f'DApp for coin_bot_id {coin_bot_id} created successfully'}, 200
    except Exception as e:
        return {'error': f'Error creating DApp: {str(e)}'}, 500

@dapps_bp.route('/api/dapps/edit/<int:dapp_id>', methods=['PUT'])
def edit_dapp(dapp_id):
    try:
        data = request.json

        session = Session()
        dapp = session.query(DApps).filter_by(id=dapp_id).first()

        if not dapp:
            return {'error': 'DApp not found'}, 404

        # Actualizar los campos de la DApp con los nuevos datos
        dapp.dapps = data.get('dapps', dapp.dapps)
        dapp.description = data.get('description', dapp.description)
        dapp.tvl = data.get('tvl', dapp.tvl)

        session.commit()

        return {'message': 'DApp updated successfully'}, 200  

    except Exception as e:
        return {'error': f'Error updating DApp: {str(e)}'}, 500
