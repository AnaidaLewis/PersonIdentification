from rest_framework import serializers
from .models import Aadhar,Address,Qualification,Bank,PersonalDetails,PastJobExperience
from accounts.serializers import UserSerializer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class PersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetails
        fields = '__all__'


class PastJobExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastJobExperience
        fields = '__all__'


class AadharSerializer(serializers.ModelSerializer):
    personal_details_user = PersonalDetailsSerializer(many=True)
    address_user = AddressSerializer(many=True)
    qualification_user = QualificationSerializer(many=True)
    past_job_experience_user = PastJobExperienceSerializer(many = True)
    bank_user = BankSerializer(many = True)

    class Meta:
        model = Aadhar
        fields = [
            'user',
            'aadhar_number',
            'active',
            'personal_details_user',
            'address_user',
            'qualification_user',
            'past_job_experience_user',
            'bank_user',

        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response

    def create(self,user):
        personal_details_user_data = self.validated_data.pop('personal_details_user')
        address_user_user_data = self.validated_data.pop('address_user')
        qualification_user_data = self.validated_data.pop('qualification_user')
        past_job_experience_user_data = self.validated_data.pop('past_job_experience_user')
        bank_user_data = self.validated_data.pop('bank_user')
        
        aadhar = Aadhar.objects.create(**self.validated_data, user = user)
        for data in personal_details_user_data:
            PersonalDetails.objects.create(user=aadhar, **data)

        for data in address_user_user_data:
            Address.objects.create(user=aadhar, **data)

        for data in qualification_user_data :
            Qualification.objects.create(user=aadhar, **data)

        for data in past_job_experience_user_data :
            PastJobExperience.objects.create(user=aadhar, **data)

        for data in bank_user_data:
            Bank.objects.create(user=aadhar, **data)
        return aadhar