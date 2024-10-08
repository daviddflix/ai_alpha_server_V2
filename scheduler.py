from config import DATABASE_URL
from apscheduler.schedulers.background import BackgroundScheduler
from routes.slack.templates.news_message import send_INFO_message_to_slack_channel
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MAX_INSTANCES, EVENT_JOB_MISSED

SLACK_LOGS_CHANNEL_ID = "C06FTS38JRX"

scheduler = BackgroundScheduler(executors={'default': {'type': 'threadpool', 'max_workers': 50}})
scheduler.add_jobstore('sqlalchemy', url=DATABASE_URL)
if scheduler.state != 1:
    scheduler.start()
    print("---- Main Scheduler started ----")

def job_error(event):
    job_id = str(event.job_id).capitalize()
    send_INFO_message_to_slack_channel(channel_id=SLACK_LOGS_CHANNEL_ID,
                                       title_message=f'{job_id} News Bot had an internal error in the last execution', 
                                       sub_title="Response", 
                                       message=f"{event.retval}")


def job_max_instances_reached(event):  
    job_id = str(event.job_id).capitalize() 
    send_INFO_message_to_slack_channel(channel_id=SLACK_LOGS_CHANNEL_ID,
                                    title_message=f'{job_id} News Bot has reached the maximum number of instances', 
                                    sub_title="Response", 
                                    message='Maximum number of running instances reached, *Upgrade* the time interval'
                                    )          

def job_missed(event):
    job_id = str(event.job_id).capitalize()
    send_INFO_message_to_slack_channel(channel_id=SLACK_LOGS_CHANNEL_ID,
                                    title_message=f'{job_id} News Bot has missed a scheduled execution', 
                                    sub_title="Response", 
                                    message='Missed execution, check the job details and configuration'
                                    )
  
   

   
scheduler.add_listener(job_error, EVENT_JOB_ERROR)
scheduler.add_listener(job_max_instances_reached, EVENT_JOB_MAX_INSTANCES)
scheduler.add_listener(job_missed, EVENT_JOB_MISSED)


