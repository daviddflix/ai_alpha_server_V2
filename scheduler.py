from config import Category
from config import db_url, session
from routes.news_bot.scrapper import start_periodic_scraping
from apscheduler.schedulers.background import BackgroundScheduler
from routes.slack.templates.news_message import send_INFO_message_to_slack_channel
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MAX_INSTANCES, EVENT_JOB_EXECUTED


scheduler = BackgroundScheduler(executors={'default': {'type': 'threadpool', 'max_workers': 50}})
scheduler.add_jobstore('sqlalchemy', url= db_url)
if scheduler.state != 1:
    scheduler.start()

def job_executed(event): 
    message = f"{event.job_id} was executed successfully at {event.scheduled_run_time}, response: {event.retval}"
    print(f'\n{message}')
    send_INFO_message_to_slack_channel(channel_id="C06FTS38JRX",
                                       title_message=F"{str(event.job_id).capitalize()} was executed successfully",
                                       sub_title="Response",
                                       message=f"Job executed at {event.scheduled_run_time}"
                                       )
    

def job_error(event):
    job_id = str(event.job_id).capitalize()
    send_INFO_message_to_slack_channel(channel_id="C06FTS38JRX",
                                       title_message=f'{job_id} News Bot has an internal error in the last execution', 
                                        sub_title="Response", 
                                        message=f"{event.retval}")


def job_max_instances_reached(event): 

    send_INFO_message_to_slack_channel(channel_id="C06FTS38JRX",
    title_message=f'{str(event.job_id).capitalize()} News Bot - Execution error', 
    sub_title="Response", 
    message='Maximum number of running instances reached, *Upgrade* the time interval')

    try:
        target = event.job_id
        with session:
            category = session.query(Category).filter(Category.category == target).first()

            if category:

                bot_name= category.category
                time_interval = category.time_interval
              
                new_time_interval = int(time_interval) + 20
                category.time_interval = new_time_interval
                session.commit()
                
                job = scheduler.add_job(start_periodic_scraping, 'interval', minutes=(new_time_interval), id=target, replace_existing=True, args=[bot_name], max_instances=2)
                if job:
                    send_INFO_message_to_slack_channel(channel_id="C06FTS38JRX",
                                                        title_message=f'{target} News Bot restarted', 
                                                        sub_title="Response", 
                                                        message=f"An interval of *{new_time_interval} Minutes* has been set")
                    
                    print(f"""---{target} News Bot restarted: An interval of *{new_time_interval} Minutes* has been set for scrapping data---""")
                    
    except Exception as e:
        print(f'---Error while restarting {target} News Bot: {str(e)}---')
        send_INFO_message_to_slack_channel(channel_id="C06FTS38JRX",
                                        title_message=f'Error while restarting {target} News Bot', 
                                        sub_title="Response", 
                                        message=f"{str(e)}")
   

   
scheduler.add_listener(job_error, EVENT_JOB_ERROR)
scheduler.add_listener(job_max_instances_reached, EVENT_JOB_MAX_INSTANCES)
scheduler.add_listener(job_executed, EVENT_JOB_EXECUTED)