from django.http import JsonResponse
import requests
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from .serializers import AadharSerializer,AddressSerializer,QualificationSerializer,BankSerializer,PersonalDetailsSerializer,PastJobExperienceSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Aadhar,Address,Qualification,Bank,PersonalDetails,PastJobExperience
# Create your views here.

User = get_user_model()


class AllDetails(generics.ListAPIView):
    serializer_class = AadharSerializer
    permission_classes = [IsAdminUser,]
    def list(self,request,pk):
        if pk == '0':
            queryset = Aadhar.objects.all()
            serializer = AadharSerializer(queryset, many = True)
            return JsonResponse(serializer.data,safe = False, status = status.HTTP_200_OK)
        else:
            try:
                queryset = Aadhar.objects.get(aadhar_number=pk)
            except Aadhar.DoesNotExist:
                content = {'detail': 'No such Aadhar exists'}
                return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
            serializer = AadharSerializer(queryset, many =False)
            return JsonResponse(serializer.data, status = status.HTTP_200_OK)


class AadharView(APIView):
    serializer_class = AadharSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        examDetails = AadharSerializer(aadhar, many=False)
        return JsonResponse(examDetails.data,status = status.HTTP_200_OK)


    def post(self, request):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        print(user)
        serializer = AadharSerializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.create(user)
            examDetails = AadharSerializer(serializer, many=False)
            return JsonResponse(examDetails.data, status = status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)




class AddressView(APIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        if pk == 0:
            address = Address.objects.filter(user=aadhar)
        else:
            try:
                address = Address.objects.get(id=pk)
            except Address.DoesNotExist:
                content = {'detail': 'No such Address'}
                return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
            try:
                address = Address.objects.get(id=pk,user=aadhar)
            except Address.DoesNotExist:
                content = {'detail': 'No such Address of this user'}
                return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
            addressDetails = AddressSerializer(address, many=False)
            return JsonResponse(addressDetails.data,status = status.HTTP_200_OK)
        addressDetails = AddressSerializer(address, many=True)
        return JsonResponse(addressDetails.data, safe=False,status = status.HTTP_200_OK)


    def post(self, request, pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        # print(user)
        address = Address(user = aadhar)
        serializer = AddressSerializer(address,data=request.data)
        if serializer.is_valid():
            serializer = serializer.save()
            examDetails = AddressSerializer(serializer, many=False)
            return JsonResponse(examDetails.data, status = status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            address = Address.objects.get(id=pk)
        except Address.DoesNotExist:
            content = {'detail': 'No such Address'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            address = Address.objects.get(id=pk,user=aadhar)
        except Address.DoesNotExist:
            content = {'detail': 'No such Address of this user'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(instance = address, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            address = Address.objects.get(id=pk)
        except Address.DoesNotExist:
            content = {'detail': 'No such Address'}
        try:
            address = Address.objects.get(id=pk,user=aadhar)
        except Address.DoesNotExist:
            content = {'detail': 'No such Address of this user'}
        address.delete()
        return JsonResponse({'Response': 'Address succsesfully delete!'},status = status.HTTP_200_OK)





class QualificationView(APIView):
    serializer_class = QualificationSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        if pk == 0:
            qualification = Qualification.objects.filter(user=aadhar)
        else:
            try:
                qualification = Qualification.objects.get(id=pk)
            except Qualification.DoesNotExist:
                content = {'detail': 'No such Qualification'}
                return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
            try:
                qualification = Qualification.objects.get(id=pk,user=aadhar)
            except Address.DoesNotExist:
                content = {'detail': 'No such Qualification of this user'}
                return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
            qualificationDetails = QualificationSerializer(qualification, many=False)
            return JsonResponse(qualificationDetails.data,status = status.HTTP_200_OK)
        qualificationDetails = QualificationSerializer(qualification, many=True)
        return JsonResponse(qualificationDetails.data, safe=False,status = status.HTTP_200_OK)


    def post(self, request, pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        # print(user)
        qualification = Qualification(user = aadhar)
        serializer = QualificationSerializer(qualification,data=request.data)
        if serializer.is_valid():
            serializer = serializer.save()
            examDetails = QualificationSerializer(serializer, many=False)
            return JsonResponse(examDetails.data, status = status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            qualification = Qualification.objects.get(id=pk)
        except Qualification.DoesNotExist:
            content = {'detail': 'No such Qualification'}
        try:
            qualification = Qualification.objects.get(id=pk,user=aadhar)
        except Qualification.DoesNotExist:
            content = {'detail': 'No such Qualification of this user'}
        serializer = QualificationSerializer(instance = qualification, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            qualification = Qualification.objects.get(id=pk)
        except Qualification.DoesNotExist:
            content = {'detail': 'No such Qualification'}
        try:
            qualification = Qualification.objects.get(id=pk,user=aadhar)
        except Qualification.DoesNotExist:
            content = {'detail': 'No such Qualification of this user'}
        qualification.delete()
        return JsonResponse({'Response': 'Qualification succsesfully delete!'},status = status.HTTP_200_OK)


class BankView(APIView):
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        if pk == 0:
            bank = Bank.objects.filter(user=aadhar)
        else:
            try:
                bank = Bank.objects.get(id=pk)
            except Bank.DoesNotExist:
                content = {'detail': 'No such Bank'}
                return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
            try:
                bank = Bank.objects.get(id=pk,user=aadhar)
            except Bank.DoesNotExist:
                content = {'detail': 'No such Bank of this user'}
                return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
            BankDetails = BankSerializer(bank, many=False)
            return JsonResponse(BankDetails.data,status = status.HTTP_200_OK)
        BankDetails = BankSerializer(bank, many=True)
        return JsonResponse(BankDetails.data, safe=False,status = status.HTTP_200_OK)


    def post(self, request, pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        # print(user)
        bank = Bank(user = aadhar)
        serializer = BankSerializer(bank,data=request.data)
        if serializer.is_valid():
            serializer = serializer.save()
            BankDetails = BankSerializer(serializer, many=False)
            return JsonResponse(BankDetails.data, status = status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            bank = Bank.objects.get(id=pk)
        except Bank.DoesNotExist:
            content = {'detail': 'No such Bank'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
             bank = Bank.objects.get(id=pk,user=aadhar)
        except  Bank.DoesNotExist:
            content = {'detail': 'No such  Bank of this user'}
        serializer =  BankSerializer(instance =  bank, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            bank = Bank.objects.get(id=pk)
        except Bank.DoesNotExist:
            content = {'detail': 'No such Bank'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
             bank = Bank.objects.get(id=pk,user=aadhar)
        except  Bank.DoesNotExist:
            content = {'detail': 'No such  Bank of this user'}
        bank.delete()
        return JsonResponse({'Response': 'Bank succsesfully delete!'},status = status.HTTP_200_OK)


class PersonalDetailsView(APIView):
    serializer_class = PersonalDetailsSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        if pk == 0:
            bank = PersonalDetails.objects.filter(user=aadhar)
        else:
            try:
                bank = PersonalDetails.objects.get(id=pk)
            except PersonalDetails.DoesNotExist:
                content = {'detail': 'No such PersonalDetails'}
                return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
            try:
                bank = PersonalDetails.objects.get(id=pk,user=aadhar)
            except PersonalDetails.DoesNotExist:
                content = {'detail': 'No such PersonalDetails of this user'}
                return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
            BankDetails = PersonalDetailsSerializer(bank, many=False)
            return JsonResponse(BankDetails.data,status = status.HTTP_200_OK)
        BankDetails = PersonalDetailsSerializer(bank, many=True)
        return JsonResponse(BankDetails.data, safe=False,status = status.HTTP_200_OK)


    def post(self, request, pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        # print(user)
        bank = PersonalDetails(user = aadhar)
        serializer = PersonalDetailsSerializer(bank,data=request.data)
        if serializer.is_valid():
            serializer = serializer.save()
            BankDetails = PersonalDetailsSerializer(serializer, many=False)
            return JsonResponse(BankDetails.data, status = status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            bank = PersonalDetails.objects.get(id=pk)
        except PersonalDetails.DoesNotExist:
            content = {'detail': 'No such PersonalDetails'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
             bank = PersonalDetails.objects.get(id=pk,user=aadhar)
        except  PersonalDetails.DoesNotExist:
            content = {'detail': 'No such  PersonalDetails of this user'}
        serializer =  PersonalDetailsSerializer(instance =  bank, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            bank = PersonalDetails.objects.get(id=pk)
        except PersonalDetails.DoesNotExist:
            content = {'detail': 'No such PersonalDetails'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
             bank = PersonalDetails.objects.get(id=pk,user=aadhar)
        except  PersonalDetails.DoesNotExist:
            content = {'detail': 'No such  PersonalDetails of this user'}
        bank.delete()
        return JsonResponse({'Response': 'PersonalDetails succsesfully delete!'},status = status.HTTP_200_OK)


class PastJobExperienceView(APIView):
    serializer_class = PastJobExperienceSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        if pk == 0:
            bank = PastJobExperience.objects.filter(user=aadhar)
        else:
            try:
                bank = PastJobExperience.objects.get(id=pk)
            except PastJobExperience.DoesNotExist:
                content = {'detail': 'No such PastJobExperience'}
                return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
            try:
                bank = PastJobExperience.objects.get(id=pk,user=aadhar)
            except PastJobExperience.DoesNotExist:
                content = {'detail': 'No such PastJobExperience of this user'}
                return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
            BankDetails = PastJobExperienceSerializer(bank, many=False)
            return JsonResponse(BankDetails.data,status = status.HTTP_200_OK)
        BankDetails = PastJobExperienceSerializer(bank, many=True)
        return JsonResponse(BankDetails.data, safe=False,status = status.HTTP_200_OK)


    def post(self, request, pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        # print(user)
        bank = PastJobExperience(user = aadhar)
        serializer = PastJobExperienceSerializer(bank,data=request.data)
        if serializer.is_valid():
            serializer = serializer.save()
            BankDetails = PastJobExperienceSerializer(serializer, many=False)
            return JsonResponse(BankDetails.data, status = status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            bank = PastJobExperience.objects.get(id=pk)
        except PastJobExperience.DoesNotExist:
            content = {'detail': 'No such PastJobExperience'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            bank = PastJobExperience.objects.get(id=pk,user=aadhar)
        except  PastJobExperience.DoesNotExist:
            content = {'detail': 'No such  PastJobExperience of this user'}
        serializer =  PastJobExperienceSerializer(instance =  bank, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        try:
            user = User.objects.get(email = request.user)
        except User.DoesNotExist:
            content = {'detail': 'No such user exists'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            aadhar = Aadhar.objects.get(user = user)
        except Aadhar.DoesNotExist:
            content = {'detail': 'Created your Aadhar first!'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
            bank = PastJobExperience.objects.get(id=pk)
        except PastJobExperience.DoesNotExist:
            content = {'detail': 'No such PastJobExperience'}
            return JsonResponse(content, status = status.HTTP_404_NOT_FOUND)
        try:
             bank = PastJobExperience.objects.get(id=pk,user=aadhar)
        except  PastJobExperience.DoesNotExist:
            content = {'detail': 'No such  PastJobExperience of this user'}
        bank.delete()
        return JsonResponse({'Response': 'PastJobExperience succsesfully delete!'},status = status.HTTP_200_OK)
