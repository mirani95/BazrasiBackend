from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api import (
    RoleViewSet,
    PermissionViewSet,
    UserRelationViewSet,
)

router = DefaultRouter()  # set router

# register route to router
router.register(r'role', RoleViewSet, basename='role')
router.register(r'permission', PermissionViewSet, basename='permission')
router.register(r'user-relations', UserRelationViewSet, basename='organization-role')

urlpatterns = [
    path('', include(router.urls))
]
