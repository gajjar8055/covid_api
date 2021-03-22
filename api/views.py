import json
from datetime import timedelta
import requests
import pandas as pd

from django.conf import settings
from django.utils import timezone

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Country
from api.serializers import UserSignUpSerializer, ValidateCountryAndDatetime, CountrySerializer
from api.tasks import send_email_graph_image
import logging

logger = logging.getLogger(__name__)


def get_date_range_data(start_date, end_date, time_line):
    """
    This method help to get range data based on response coming from API.

    :param start_date: Start date for date range
    :param end_date: End date for date range.
    :param time_line: Timeline data from API response.
    :return: return range data as dictionary.
    """
    if not (start_date and end_date):
        today = timezone.datetime.now()
        start_date = (today - timedelta(days=15)).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")

    pd_data = pd.DataFrame(time_line)
    pd_data['date'] = pd.to_datetime(pd_data['date'])
    after_start_date = pd_data["date"] >= start_date
    before_end_date = pd_data["date"] <= end_date
    between_two_dates = after_start_date & before_end_date
    pd_data = pd_data.loc[between_two_dates]
    pd_data['date'] = pd_data['date'].dt.strftime("%Y-%m-%d")
    return json.loads(pd_data.to_json(orient='records'))


class SignUp(CreateAPIView):
    """
      SignUp is rest framework CreateAPIView class.Help user to signup in web application.

    """
    permission_classes = [AllowAny]
    serializer_class = UserSignUpSerializer


class CountryListAPI(ListAPIView):
    """
        API to list all countries
    """
    permission_classes = [AllowAny]
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class CovidDataAPI(GenericAPIView):
    serializer_class = ValidateCountryAndDatetime

    def post(self, request, *args, **kwargs):
        try:
            params = {'include': 'timeline'}
            country = request.data.get('country')
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            email = request.data.get('email')
            logger.info("Request data from user.")
            logger.info(request.data)
            param_validation = ValidateCountryAndDatetime(data=request.data)
            param_validation.is_valid(raise_exception=True)

            if country:
                Country.objects.get(code=country)
                url = settings.COVID_API_BASE_URL.format("/countries/{0}".format(country))
            else:
                url = settings.COVID_API_BASE_URL.format("/countries/{0}".format(request.user.country.code))
            response = requests.get(url, params=params)
            logger.info("Total Time taken by API Call.: {0}".format(str(response.elapsed.total_seconds())))

            response_json = response.json()
            if not response.ok:
                return Response({"message": "API calling error."}, status=status.HTTP_400_BAD_REQUEST)
            date_filtered_timeline = get_date_range_data(start_date, end_date,
                                                         response_json.get('data').get('timeline'))
            response_json['data']['timeline'] = date_filtered_timeline
            if email:
                send_email_graph_image.delay(date_filtered_timeline, request.user.email, request.user.full_name)

            return Response(response_json, status=status.HTTP_200_OK)
        except Country.DoesNotExist:
            logger.exception("Country Object not found")
            return Response({"message": "Country not found."}, status=status.HTTP_404_NOT_FOUND)
        except APIException as e:
            raise e
        except Exception:
            logger.exception("Unknown Server error occurred. ")
            return Response({"message": "Unknown Server error occurred. "}, status=status.HTTP_400_BAD_REQUEST)
