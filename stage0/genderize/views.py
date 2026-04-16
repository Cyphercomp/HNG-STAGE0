from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
import requests
from rest_framework.decorators import action
from rest_framework import status 
from django.utils import timezone

class GenderizeViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def classify(self, request):
        name = request.query_params.get('name')
        if not name:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif not name.isalpha():
            return Response( status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        response  = requests.get(f'https://api.genderize.io?name={name}')
        data = response.json()

        if response.status_code != 200:
            return Response({
                'Status' : 'Error',
                'Message' : 'Failed to fetch data from Genderize API'
            }, status=status.HTTP_502_BAD_GATEWAY)
        else:
            if data['gender'] is None or data['count'] == 0:
                return Response({
                    'Status' : 'Error',
                    'Message' : 'No Prediction Available for the provided name'
                }, status=status.HTTP_404_NOT_FOUND)
            probability = data['probability']
            sample_size = data['count']
            is_confident = False

            print(f"Probability: {probability}, Sample Size: {sample_size}")
            if probability >= 0.8 and sample_size >= 100:
                is_confident = True
            print(f"Is Confident: {is_confident}")
            payload = {
                'status': 'success',
                'data':{
                    'name': data.get('name'),
                    'gender': data.get('gender'),
                    'probability': probability,
                    'sample_size': sample_size,
                    'is_confident': is_confident,
                    'processed_at': timezone.now().isoformat()  
                }
            }
            print(f"Payload: {payload}")
        return Response(payload, status=status.HTTP_200_OK)

# Create your views here.
