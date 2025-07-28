from django.shortcuts import render
from .models import Store
from rest_framework import views
from .serializers import StoreSerializer
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings
import joblib

model_path = os.path.join(settings.BASE_DIR, 'model.pkl')
scaler_path = os.path.join(settings.BASE_DIR, 'scaler.pkl')

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

Category = ['Furniture', 'Office Supplies', 'Technology']

SubCategory = ['Bookcases', 'Chairs', 'Labels', 'Tables', 'Storage', 'Furnishings', 'Art',
 'Phones', 'Binders', 'Appliances', 'Paper', 'Accessories', 'Envelopes',
 'Fasteners', 'Supplies', 'Machines', 'Copiers']

Segment = ['Consumer', 'Corporate', 'Home Office']

# Region = ['South', 'West', 'Central', 'East']

ShipMode = ['Second Class', 'Standard Class', 'First Class', 'Same Day']


class SalesPrediction(views.APIView):
    def post(self, request):
        instance = StoreSerializer(data=self.request.data)
        if instance.is_valid():
            data = instance.validated_data
            new_category = data.get('category')
            new_sub_category = data.get('sub_category')
            new_segment = data.get('segment')
            new_region = data.get('region')
            new_ship_mode = data.get('ship_mode')

            category1_0 = [1 if new_category == name else 0 for name in Category]
            sub_category1_0 = [1 if new_sub_category == name else 0 for name in SubCategory]
            segment1_0 = [1 if new_segment == name else 0 for name in Segment]
            # region1_0 = [1 if new_region == name else 0 for name in Region]
            ship_mode1_0 = [1 if new_ship_mode == name else 0 for name in ShipMode]

            features = [data['quantity'],
                        data['month'],
                        data['dayofweek']
                        ] + category1_0 + sub_category1_0 + segment1_0 + ship_mode1_0
            scaled_data = scaler.transform([features])
            pred = model.predict(scaled_data)[0]
            shop = instance.save(predicted_sales=pred)
            return Response({'predicted_sales': round(pred),
                            'data': StoreSerializer(shop).data}, status=status.HTTP_201_CREATED)
        return Response(instance.errors, status=status.HTTP_400_BAD_REQUEST)
