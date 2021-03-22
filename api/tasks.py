import uuid
import plotly.express as px
import pandas as pd
from celery import shared_task

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from api.utils import email_embed_image


@shared_task
def send_email_graph_image(time_line, to_email, name):
    """
    Generate Image from based on time_line dataframe.Based on email it will send in background USING celery task.
    :param time_line:
    :param to_email:
    :param name:
    :return:
    """
    df = pd.DataFrame(time_line)
    fig = px.bar(df, x="date", y="new_confirmed", title='Corona Case in India')
    img_data = fig.to_image(format="jpeg")
    html_content = render_to_string("email.html", context={'name': name})
    email = EmailMultiAlternatives("Covid data graph.", 'Body', 'from@example.com', [to_email])
    email.attach_alternative(html_content, "text/html")
    email_embed_image(email, uuid.uuid4().hex, img_data)
    email.send()
