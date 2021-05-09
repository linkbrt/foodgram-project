from django.http.response import JsonResponse
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Favorite, Follow, Purchase
from .serializers import (FavoriteSerializer, FollowSerializer,
                          PurchaseSerializer)

from foodgram.models import Ingredient


SUCCESS_RESPONSE = Response(
    data={'success': 'true'},
    status=status.HTTP_200_OK
)

BAS_RESPONSE = Response(
    data={'success': 'false'},
    status=status.HTTP_400_BAD_REQUEST
)


class ApiBaseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return SUCCESS_RESPONSE
        if 'non_field_errors' in serializer._errors:
            return SUCCESS_RESPONSE
        return BAS_RESPONSE

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(recipe__pk=kwargs['pk'])
        if instance:
            instance.delete()
            return SUCCESS_RESPONSE
        return BAS_RESPONSE


class PurchasesViewSet(ApiBaseViewSet):
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)


class FavoriteViewSet(ApiBaseViewSet):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class FollowViewSet(ApiBaseViewSet):
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(author__pk=kwargs['pk'])
        if instance:
            instance.delete()
            return SUCCESS_RESPONSE
        return BAS_RESPONSE


class IngredientViewSet(viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        start_ingredient = request.GET.get('query')
        result = self.get_queryset().filter(title__startswith=start_ingredient)
        result = [
            {'title': ingredient.title, 'dimension': ingredient.unit}
            for ingredient in result
        ]
        return JsonResponse(data=result, safe=False)
