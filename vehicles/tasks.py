from __future__ import absolute_import, unicode_literals
from celery.utils.log import get_task_logger
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from VEIO.settings import EMAIL_HOST_USER
from datetime import datetime, timedelta
from accounts.models import UserProfile
import json
import redis
import requests
import websocket
from .models import Flow, Gesveh, Regveh
# from pages.views import expirein
# from demoapp.models import Widget
import time
import pytz
logger = get_task_logger(__name__)


@shared_task
def emailsend(email):
    send_mail('Welcome to VEIO ',
              'Vehicle Entry In Out Management System\n Registration Successful',
              EMAIL_HOST_USER,
              email
              )
    # PageConsumer.exportData()


def regemail(user):
    send_date = datetime.utcnow()+timedelta(minutes=1)
    print(send_date)
    emailsend.apply_async(kwargs={'email': [
                          user.email]}, eta=send_date)


@ shared_task
def add(x, y):
    time.sleep(10)
    logger.info('Adding {0} + {1}'.format(x, y))
    print("krishna")
    return x + y


@shared_task
def listflow():
    ws = websocket.WebSocket()
    ws.connect("ws://127.0.0.1:8000/security/")
    ws.send("refreshList")
    ws.close()


def trigger(vehicle):
    send_date = vehicle.firstentry.astimezone(
        pytz.utc)+timedelta(days=vehicle.nod)
    print(send_date)
    listflow.apply_async(eta=send_date)


def expireint():
    out_data = []
    for item in Flow.objects.all().filter(timeout__isnull=True):
        data = Gesveh.objects.filter(
            vn=item.vn).order_by('-firstentry').first()
        if (data is not None) and (data.firstentry+timedelta(data.nod) < datetime.now()):
            inp = vars(data)
            inp.pop('_state')
            inp['timein'] = item.timein
            out_data.append(inp)
            out_data.reverse()
    return out_data


@shared_task
def soemail():
    sousers = UserProfile.objects.filter(is_SO=True).values('user__email')
    data = expireint()
    # html = '''<h1>List of vehicles with expired permission present inside campus</h1><hr><table><thead><th>#</th><th>Vehicle No.</th><th>Entrant Name</th><th>No of days permitted</th><th>First Entry</th><th>Last Entry</th><th>Contact No.</th>'''
    # for index, item in enumerate(data):
    #     item['firstentry'] = item['firstentry'].strftime("%d/%m/%y , %H:%M")
    #     item['timein'] = item['timein'].strftime("%d/%m/%y , %H:%M")
    #     html += f"<tr><td>{index+1}</td><td>{item['vn']}</td><td>{item['name']}</td><td>{item['firstentry']}</td><td>{item['timein']}</td><td>{item['contact']}</td></tr>"
    # html += '</thead></table>'
    # print(html)
    # print(data)
    msg_html = render_to_string('email.html', {'emails': data})
    # print(msg_html)
    so_emails = []
    for email in sousers:
        so_emails.append(email['user__email'])
    # print(so_emails)
    send_mail('VEIO LIST ',
              'Vehicle Entry In Out Management System\n List of vehicles with expired permission present inside campus',
              EMAIL_HOST_USER,
              ['genet32928@inmail3.com'],
              html_message=msg_html)
    # print(data)
