from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.models import Country

UserModel = get_user_model()


class UserSignUpSerializer(serializers.ModelSerializer):
    """
        UserSignUpSerializer help to connect with User model for signup functionality.
        country_name: It return instead of id to the the representation.
        ...
        Methods
        -------
        create(resquest=""):
            Override create method to set user encrypted password
        to_representation
            Method helps to remove or add to representation block.

    """

    country_name = serializers.CharField(source='country.name', read_only=True)

    class Meta:
        model = UserModel
        fields = ('email', 'first_name', 'last_name', 'password', 'country', 'country_name')

    def create(self, validated_data):
        user = UserModel.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            country=validated_data['country']
        )
        # Here user.set_password method will  encrypt password from  plain password string.
        user.set_password(validated_data['password'])
        user.save()

        return user

    def to_representation(self, instance):
        data = super(UserSignUpSerializer, self).to_representation(instance)
        data.pop('password')
        data.pop('country')
        return data


class ValidateCountryAndDatetime(serializers.Serializer):
    """
      ValidateCountryAndDatetime is used here for validate request data coming from the user end.

    """
    country = serializers.CharField(max_length=2, required=False)
    start_date = serializers.DateField(input_formats=["%Y-%m-%d"], required=False)
    end_date = serializers.DateField(input_formats=["%Y-%m-%d"], required=False)
    email = serializers.BooleanField(required=False)

    def validate(self, attrs):
        # Below we are checking start date not before date from end date.
        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError("Start date must be before `end_date`.")
        return attrs


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"
