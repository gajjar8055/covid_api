from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api.views import SignUp, CovidDataAPI, CountryListAPI

urlpatterns = [
    path('signup/', SignUp.as_view()),
    # Obtain token from the Token table using built-in method.
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('covid_api/', CovidDataAPI.as_view()),
    path('country_list/', CountryListAPI.as_view()),

]
