from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers

from . import models


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['is_superuser'] = user.is_superuser

        return token


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     style={
                                         'input_type': 'password'
                                     })

    class Meta:
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        password = validated_data.get('password')

        user = models.User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.set_password(raw_password=password)
        user.save()

        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = '__all__'


class PupilSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pupil
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    group_name = serializers.CharField(read_only=True)

    class Meta:
        model = models.Payment
        fields = ['id', 'created', 'updated', 'pupil', 'group', 'first_name', 'last_name', 'group_name', 'amount', 'date']

    def create(self, validated_data):
        new_amount = validated_data.get('amount')
        new_date = validated_data.get('date')
        pupil = validated_data.get('pupil')
        group = validated_data.get('group')
        payment_year = validated_data.get('date').year
        payment_month = validated_data.get('date').month

        try:
            payment = models.Payment.objects.get(pupil=pupil,
                                                 group=group,
                                                 date__year=payment_year,
                                                 date__month=payment_month)
        except:
            payment = None

        if payment:
            payment.amount += new_amount
            payment.date = new_date
            payment.save()

            return payment

        else:
            return super().create(validated_data)
