from config import Competitor, session
from flask import Blueprint, request, jsonify


competitor_bp = Blueprint('competitor_bp', __name__)


# edits a competitor data by the ID of the competitor
@competitor_bp.route('/edit_competitors/<int:competitor_id>', methods=['PUT'])  
def edit_competitor_data(competitor_id):
    try:
        data = request.json
        coin_data = session.query(Competitor).filter(Competitor.id == competitor_id).first()

        if not coin_data:
            return {'message': 'No data found for the requested coin'}, 404

        for key, value in data['competitor_data'].items():
            if key not in ['coin_bot_id', 'updated_at', 'created_at', 'dynamic']:
                setattr(coin_data, key, value)

        session.commit()
        return {'message': f'{coin_data.token} edited successfully'}, 200
    
    except Exception as e:
        return {'error': f'Error editing competitor data: {str(e)}'}, 500
    

# Gets a list of the competitors and the analyzed coin  
@competitor_bp.route('/get_competitors/<int:coin_bot_id>', methods=['GET'])
def get_competitor_data(coin_bot_id):
    try:
        if coin_bot_id is None:
            return jsonify({'message': 'Coin ID is required', 'status': 400}), 400

        coin_data = session.query(Competitor).filter(Competitor.coin_bot_id == coin_bot_id).all()

        if not coin_data:
            return jsonify({'message': 'No data found for the requested coin', 'status': 404}), 404

        competitor_data = [{
            'competitor': competitor_value.as_dict(),
        } for competitor_value in coin_data]
        
        return jsonify({'competitors': competitor_data, 'status': 200}), 200
    
    except Exception as e:
        return jsonify({'message': f'Error getting competitors data: {str(e)}', 'status': 500}), 500




# Builder to create competitor table


@competitor_bp.route('/create_competitor', methods=['POST'])
def create_competitor_table():
    try:
        data = request.json
        coin_bot_id = data.get('coin_bot_id')

        if coin_bot_id is None:
            return jsonify({'error': 'Coin ID is required', 'status': 400}), 400

        competitor_data = data.get('competitor_data')

        if not competitor_data:
            return jsonify({'error': 'Competitor data is required', 'status': 400}), 400
        
        token=competitor_data.get('token')
        data=competitor_data.get('data')

        if not token or not data:
            return jsonify({'error': 'Token or data is missing', 'status': 400}), 400
        
        for obj in data:
            key = obj['key'].lower()  
            value = obj['value'].lower()  
            new_competitor = Competitor(
                token=token.lower(),  
                key=key,
                value=value,
                coin_bot_id=coin_bot_id
            )

            session.add(new_competitor)
            session.commit()

        return jsonify({'message': 'Features added successfully', 'status': 201}), 201
    
    except Exception as e:
        return jsonify({'error': f'Error creating competitor: {str(e)}', 'status': 500}), 500



# Route to edit an already created competitor