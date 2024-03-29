import os
from dotenv import load_dotenv
import datetime
from io import BytesIO
from PIL import Image
import requests
import boto3
from config import Analysis, AnalysisImage, session, CoinBot
from flask import jsonify, Blueprint, request
from sqlalchemy import desc
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.jobstores.base import JobLookupError
from routes.news_bot.poster_generator import generate_poster_prompt

sched = BackgroundScheduler()

analysis_bp = Blueprint('analysis', __name__)

load_dotenv()

AWS_ACCESS = os.getenv('AWS_ACCESS')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
def resize_and_upload_image_to_s3(image_data, bucket_name, image_filename, target_size=(256, 256)):
    try:
        response = requests.get(image_data)
        if response.status_code == 200:
            image_binary = response.content
            image = Image.open(BytesIO(image_binary))

            resized_image = image.resize(target_size)
            image_key = image_filename
            
            s3 = boto3.client(
                's3',
                region_name='us-east-2',
                aws_access_key_id=AWS_ACCESS,
                aws_secret_access_key=AWS_SECRET_KEY
            )
            
            # Subir la imagen redimensionada a S3
            with BytesIO() as output:
                resized_image.save(output, format="JPEG")
                output.seek(0)
                s3.upload_fileobj(output, bucket_name, image_key)
            
            # Obtener la URL de la imagen subida
            image_url = f"https://{bucket_name}.s3.amazonaws.com/{image_key}"
            return image_url
        else:
            print("Error:", response.status_code)
            return None
    except Exception as e:
        print("Error :", str(e))
        return None


@analysis_bp.route('/get_analysis/<int:coin_bot_id>', methods=['GET'])
def get_analysis(coin_bot_id):

    try:
        analysis_objects = session.query(Analysis).filter_by(
            coin_bot_id=coin_bot_id).order_by(desc(Analysis.created_at)).all()
        analysis_data = []

        # Iterates over the analysis dict and gets the images related to each analysis
        for analy in analysis_objects:
            analysis_dict = analy.to_dict()

            images_objects = session.query(AnalysisImage).filter_by(
                analysis_id=analy.analysis_id).all()
            images_data = [{'image_id': img.image_id, 'image': img.image}
                           for img in images_objects]

            analysis_dict['analysis_images'] = images_data
            analysis_data.append(analysis_dict)

        # TO CHECK THE DATA IN analysis_data
        # for analy in analysis_data:
        #     print(f"Analysis ID: {analy['analysis_id']}, Analysis: {analy['analysis']}, Created At: {analy['created_at']}")
        #     for img in analy['analysis_images']:
        #         print(f"  Image ID: {img['image_id']}, Image: {img['image']}")

        return jsonify({'message': analysis_data, 'success': True, 'status': 200}), 200

    except Exception as e:
        session.rollback()
        return jsonify({'message': str(e), 'success': False, 'status': 500}), 500
  # Gets all the analysis related to a coin

# Fn to get analysis related to a coin id


def get_analysis_by_id(coin_bot_id):
    return session.query(Analysis).filter_by(coin_bot_id=coin_bot_id).order_by(desc(Analysis.created_at)).all()

# Fn to get Analysis related to a coin name


def get_analysis_by_name(coin_bot_name):
    coin = session.query(CoinBot).filter(
        CoinBot.bot_name == coin_bot_name).first()
    return session.query(Analysis).filter_by(coin_bot_id=coin.bot_id).all() if coin else None

# fn to get analysis images


def get_analysis_images(analysis_object):
    return [{'image_id': img.image_id, 'image': img.image} for img in session.query(AnalysisImage).filter_by(analysis_id=analysis_object.analysis_id).all()]

# Route to get analysis by coin id/name
@analysis_bp.route('/api/get_analysis_by_coin', methods=['GET'])
def get_analysis_by_coin():
    try:
        coin_bot_name = request.args.get('coin_bot_name')
        coin_bot_id = request.args.get('coin_bot_id')

        if not coin_bot_id and not coin_bot_name:
            return jsonify({'message': 'Coin ID or name is missing', 'status': 400}), 400

        analysis_objects = []
        if coin_bot_name:
            analysis_objects = get_analysis_by_name(coin_bot_name)
        elif coin_bot_id:
            analysis_objects = get_analysis_by_id(coin_bot_id)

        if not analysis_objects:
            return jsonify({'message': 'No analysis found', 'status': 404}), 404

        analysis_data = [{'analysis': analy.to_dict(
        ), 'analysis_images': get_analysis_images(analy)} for analy in analysis_objects]

        return jsonify({'message': analysis_data, 'success': True, 'status': 200}), 200

    except Exception as e:
        session.rollback()
        return jsonify({'message': str(e), 'success': False, 'status': 500}), 500


# Gets all the analysis from all coins
@analysis_bp.route('/get_analysis', methods=['GET'])
def get_all_analysis():

    try:
        analysis_objects = session.query(Analysis).order_by(
            desc(Analysis.created_at)).all()
        analysis_data = []

        # Iterates over the analysis dict and gets the images related to each analysis
        for analy in analysis_objects:
            analysis_dict = analy.to_dict()

            images_objects = session.query(AnalysisImage).filter_by(
                analysis_id=analy.analysis_id).all()
            images_data = [{'image_id': img.image_id, 'image': img.image}
                           for img in images_objects]
            
            analysis_dict['category_name'] = analy.category_name
            analysis_dict['analysis_images'] = images_data
            analysis_dict['coin_bot_id'] = analy.coin_bot_id
            analysis_data.append(analysis_dict)

        return jsonify({'message': analysis_data, 'success': True, 'status': 200}), 200

    except Exception as e:
        session.rollback()
        return jsonify({'message': str(e), 'success': False, 'status': 500}), 500


# Creates an analysis
@analysis_bp.route('/post_analysis', methods=['POST'])
def post_analysis():
    try:
        coin_bot_id = request.form.get('coinBot')
        content = request.form.get('content')
        category_name = request.form.get('category_name')
        # image_file = request.files.get('image')

        # Check if any of the required values is missing
        if content == 'null' or coin_bot_id == 'null':
            return jsonify({'error': 'One or more required values are missing', 'status': 400, 'success': False}), 400
        
        if category_name == 'null' or coin_bot_id == 'null':
            return jsonify({'error': 'One or more required values are missing', 'status': 400, 'success': False}), 400

        # Check if any of the required values is missing
        if coin_bot_id is None or not coin_bot_id or content is None or not content:
            return jsonify({'error': 'One or more required values are missing', 'status': 400, 'success': False}), 400
        
        

        new_analysis = Analysis(
            analysis=content,
            coin_bot_id=coin_bot_id,
            category_name=category_name
        )
        
        session.add(new_analysis)
        session.commit()
        
        if new_analysis:
            image = generate_poster_prompt(new_analysis.analysis)
            print("image generated")
            analysis_id = new_analysis.analysis_id
            print('id analysis', analysis_id)
            image_filename = f"{analysis_id}.jpg"    
            print('filename: ', image_filename)
            if image:
                    try:
                                # Resize and upload the image to S3
                        resized_image_url = resize_and_upload_image_to_s3(image, 'appanalysisimages', image_filename)

                        if resized_image_url:
                             print("Image resized and uploaded to S3 successfully.")
                        else:
                             print("Error resizing and uploading the image to S3.")
                    except Exception as e:
                        print("Error:", e)
            else:
                print("Image not generated.")
        
        


        # Return success response if everything is fine
        return jsonify({'message': 'Analysis posted successfully', 'status': 200, 'success': True}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e), 'status': 500, 'success': False}), 500


# Deletes an analysis passing the analysis_id
@analysis_bp.route('/delete_analysis/<int:analysis_id>', methods=['DELETE'])
def delete_analysis(analysis_id):
    try:
        # Check if the analysis_id exists
        analysis_to_delete = session.query(Analysis).filter(
            Analysis.analysis_id == analysis_id).first()
        if analysis_to_delete is None:
            return jsonify({'error': 'Analysis not found', 'status': 404, 'success': False}), 404

        # Delete the associated image if it exists
        analysis_image_to_delete = session.query(
            AnalysisImage).filter_by(analysis_id=analysis_id).first()

        if analysis_image_to_delete:
            session.delete(analysis_image_to_delete)

        # Delete the analysis
        session.delete(analysis_to_delete)
        session.commit()

        return jsonify({'message': 'Analysis deleted successfully', 'status': 200, 'success': True}), 200

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e), 'status': 500, 'success': False}), 500

# Edits an analysis


@analysis_bp.route('/edit_analysis/<int:analysis_id>', methods=['PUT'])
def edit_analysis(analysis_id):
    try:
        # Check if the analysis_id exists
        analysis_to_edit = session.query(Analysis).filter(
            Analysis.analysis_id == analysis_id).first()
        if analysis_to_edit is None:
            return jsonify({'error': 'Analysis not found', 'status': 404, 'success': False}), 404

        # Update analysis content if provided
        new_content = request.json.get('content')

        if not new_content:
            return jsonify({'error': 'New content is required to edit the Analysis', 'status': 400, 'success': False}), 400

        analysis_to_edit.analysis = new_content
        session.commit()

        return jsonify({'message': 'Analysis edited successfully', 'status': 200, 'success': True}), 200

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e), 'status': 500, 'success': False}), 500


# Gets the name and date of the last analysis created
@analysis_bp.route('/get_last_analysis', methods=['GET'])
def get_last_analysis():
    try:
        # Retrieve the last analysis created
        last_analysis = session.query(Analysis).order_by(
            Analysis.created_at.desc()).first()

        if last_analysis is None:
            return jsonify({'error': 'No analysis found', 'status': 404, 'success': False}), 404

        coin = session.query(CoinBot).filter(
            CoinBot.bot_id == last_analysis.coin_bot_id).first()

        # Extract relevant information, such as analysis content and creation date
        analysis_data = {
            'analysis_id': last_analysis.analysis_id,
            'content': last_analysis.analysis,
            'coin_name': coin.bot_name,
            'category_name': last_analysis.category_name,
            'created_at': last_analysis.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        return jsonify({'last_analysis': analysis_data, 'status': 200, 'success': True}), 200

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e), 'status': 500, 'success': False}), 500


# Funtion to execute by the scheduler
def publish_analysis(coin_bot_id, content, category_name):
    title_end_index = content.find('\n')
    if title_end_index != -1:
        # Extract title and remove leading/trailing spaces
        title = content[:title_end_index].strip()
        # Extract content after the title
        content = content[title_end_index+1:]
    else:
        title = ''  # If no newline found, set title to empty string
    # Create new analysis instance
    new_analysis = Analysis(analysis=content, category_name=category_name, coin_bot_id=coin_bot_id)
    session.add(new_analysis)
    session.commit()
    print("Publishing analysis with title:", title)


@analysis_bp.route('/schedule_post', methods=['POST'])
def schedule_post():
    try:
        if not sched.running:
            sched.start()

        coin_bot_id = request.form.get('coinBot')
        category_name = request.form.get('category_name')
        content = request.form.get('content')
        scheduled_date_str = request.form.get('scheduledDate')

        if not (coin_bot_id and content and scheduled_date_str):
            return jsonify({'error': 'One or more required values are missing', 'status': 400, 'success': False}), 400

        # Crear un objeto datetime
        scheduled_datetime = datetime.strptime(
            scheduled_date_str, '%a, %b %d, %Y, %I:%M:%S %p')

        # Agregar un nuevo trabajo
        sched.add_job(publish_analysis, args=[coin_bot_id, content, category_name], trigger=DateTrigger(run_date=scheduled_datetime))

        return jsonify({'message': 'Post scheduled successfully', 'status': 200, 'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 500, 'success': False}), 500


# Gets all the schedule analysis
@analysis_bp.route('/get_scheduled_jobs', methods=['GET'])
def get_jobs():
    try:
        job_listing = []
        for job in sched.get_jobs():
            job_info = {
                'id': job.id,
                'name': job.name,
                'trigger': str(job.trigger),
                'args': str(job.args),
                'next_run_time': str(job.next_run_time) if hasattr(job, 'next_run_time') else None
            }
            job_listing.append(job_info)

        return jsonify({'jobs': job_listing, 'status': 200, 'success': True}), 200

    except Exception as e:
        return jsonify({'error': str(e), 'status': 500, 'success': False}), 500


# Deletes a scheduled job by job id
@analysis_bp.route('/delete_scheduled_job/<string:job_id>', methods=['DELETE'])
def delete_scheduled_job(job_id):
    try:
        # Find the by schedule analysis by ID
        job = sched.get_job(job_id)
        if job is None:
            return jsonify({'error': 'Scheduled job not found', 'status': 404, 'success': False}), 404

        # Deletes an analysis
        sched.remove_job(job_id)

        return jsonify({'message': 'Scheduled job deleted successfully', 'status': 200, 'success': True}), 200

    except JobLookupError as e:
        return jsonify({'error': str(e), 'status': 404, 'success': False}), 404
    except Exception as e:
        return jsonify({'error': str(e), 'status': 500, 'success': False}), 500
