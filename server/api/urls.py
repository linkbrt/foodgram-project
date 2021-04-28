from django.urls import include, path
from rest_framework import routers, viewsets
from rest_framework.authtoken import views

from .views import FavoriteViewSet, FollowViewSet, IngredientViewSet, PurchasesViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('purchases', PurchasesViewSet, basename='purchases')
router_v1.register('favorites', FavoriteViewSet, basename='favorites')
router_v1.register('subscribe', FollowViewSet, basename='subscribes')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')

auth_urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token)
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_urlpatterns)),
]
