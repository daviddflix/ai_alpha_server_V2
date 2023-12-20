from routes.slack.templates.poduct_alert_notification import send_notification_to_product_alerts_slack_channel
from .alert_strategy import send_alert_strategy_to_slack, send_alert_strategy_to_telegram
from flask import request, Blueprint
from config import TopStory, session, CoinBot, Category
from websocket.socket import socketio


tradingview_notification_bp = Blueprint(
    'tradingview_notification_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

def get_all_top_stories():
    try:
        coin_bots = session.query(CoinBot).all()

        if not coin_bots:
            return {'message': 'No CoinBots found'}, 404

        top_stories_list = []

        for coin_bot in coin_bots:
            coin_bot_id = coin_bot.bot_id

            top_stories = session.query(TopStory).filter(TopStory.coin_bot_id == coin_bot_id).all()

            for top_story in top_stories:
                top_story_dict = {
                    'top_story_id': top_story.top_story_id,
                    'story_date': top_story.story_date,
                    'summary': top_story.summary,
                    'created_at': top_story.created_at.isoformat(),
                    'coin_bot_id': top_story.coin_bot_id,
                    'images': []
                }

                for image in top_story.images:
                    top_story_dict['images'].append({
                        'image_id': image.image_id,
                        'image': image.image,
                        'created_at': image.created_at.isoformat(),
                        'top_story_id': image.top_story_id
                    })

                top_stories_list.append(top_story_dict)

        if top_stories_list:
            return {'top_stories': top_stories_list}, 200
        else:
            return {'message': 'No top stories found'}, 404

    except Exception as e:
        return {'error': f'An error occurred getting the top stories: {str(e)}'}, 500
    



@tradingview_notification_bp.route('/api/get/allTopStories', methods=['GET'])
def get_all_top_stories_route():
    try:
        result, status_code = get_all_top_stories()
        return result, status_code

    except Exception as e:
        return {'error': f'An error occurred getting the news: {str(e)}'}, 500
    






## Function to get alerts by category
@tradingview_notification_bp.route('/api/get/allAlerts', methods=['GET'])  
def get_all_alerts():
    try:
        category = request.args.get('category')
        category_obj = session.query(Category).filter(Category.category == category).first()

        alerts_list = []

        if not category_obj:
            return alerts_list, 404

        if category_obj:
            coin_bots = category_obj.coin_bot

            for coin_bot in coin_bots:
                alerts = coin_bot.alerts
                for alert in alerts:
                    for alert in alerts:
                        alert_dict = {
                            'alert_id': alert.alert_id,
                            'alert_name': alert.alert_name,
                            'alert_message': alert.alert_message,
                            'symbol': alert.symbol,
                            'price': alert.price,
                            'coin_bot_id': alert.coin_bot_id,
                            'created_at': alert.created_at.isoformat()  # Convert to ISO format
                        }

                    alerts_list.append(alert_dict)


        return alerts_list, 200
    except Exception as e:
        return 'Error in getting all alerts ' + str(e), 500







## Receives all alert from Tradingview and does three things: Send data to Slack, Store the data in the DB and send the data to Telegram 
@tradingview_notification_bp.route('/api/alert/tv', methods=['GET', 'POST'])
def receive_data_from_tv():
    try:
        if not request.data:
            return 'No data sent in the request', 400
        elif request.is_json:
            print('Message from Tradingview received as JSON', request.data)
            # send_notification_to_product_alerts_slack_channel(title_message='Message from Tradingview received as JSON',
            #                                                   sub_title='Invalid request format',
            #                                                   message=str(request.data))
            return 'Invalid request format', 400
        else:
            try:
                print('Data from Tradingview', request.data)
                data_text = request.data.decode('utf-8')  # Decode the bytes to a string
                data_lines = data_text.split(',')  # Split the text into lines
               
                data_dict = {} 

                for line in data_lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        data_dict[key.strip()] = value.strip()

                alert_name = data_dict.get('alert_name', '') 
                symbol = data_dict.get('symbol', '') 
                message = data_dict.get('message', '')  
                price = data_dict.get('price', data_dict.get('last_price', ''))

                
                response, status = send_alert_strategy_to_telegram(price=price,
                                                alert_name=alert_name,
                                                message=message,
                                                symbol=symbol,
                                                )

                return response, status
            
            except Exception as e:
                print(f'Error sending message to Slack channel. Reason: {e}')
                send_notification_to_product_alerts_slack_channel(title_message='Message from Tradingview failed',
                                                              sub_title='Reason',
                                                              message=str(e))
                return f'Error sending message to Slack channel. Reason: {e}', 500
    except Exception as e:
        print(f'Error main thread. Reason: {e}')
        return 'Error', 500    
        
