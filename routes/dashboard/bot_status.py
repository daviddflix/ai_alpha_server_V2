import os
from config import Admin, Analysis, AnalysisImage, Category, Chart, CoinBot, Keyword
#from routes.slack.templates.product_alert_notification import send_notification_to_product_alerts_slack_channel
from routes.telegram.email_invitation_link.invitation_link import send_email_bp
from routes.trendspider.index import trendspider_notification_bp
from routes.tradingview.index import tradingview_bp
from routes.news_bot.index import activate_news_bot, deactivate_news_bot, scrapper_bp
from routes.telegram.index import telegram_bp 
from routes.slack.slack_actions import slack_events_bp
from flask_cors import CORS
from websocket.socket import socketio
from flask import Flask, jsonify, render_template, session as flask_session
from flask import request, redirect, url_for
from config import Session as DBSession 
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import Unauthorized
from routes.dashboard.activate_all_bots import bots_activator
from routes.dashboard.deactivate_all_bots import bots_deactivator
from sqlalchemy.orm import joinedload
from flask import Blueprint


bots_status = Blueprint('get_bots_status', __name__)

app = Flask(__name__)
app.name = 'AI Alpha'
CORS(app, origins='*')
socketio.init_app(app)

# Configure Flask to look for templates in the 'dashboard/templates' folder
app.template_folder = 'dashboard/apps/templates'
app.static_folder = 'dashboard/apps/static'
app.secret_key = os.urandom(24)


@bots_status.route('/get_bot_status')
def get_bot_status():
    with DBSession() as db_session:
        categories = db_session.query(Category).all()

    bot_statuses = {category.category: category.is_active for category in categories}
    print(bot_statuses)
    return jsonify({'success': True, 'bot_statuses': bot_statuses})