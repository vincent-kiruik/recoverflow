from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.accounts.views import UserViewSet
from apps.groups.views import GroupViewSet
from apps.borrowers.views import BorrowerViewSet
from apps.loans.views import LoanViewSet
from apps.recovery.views import RecoveryCaseViewSet
from apps.collection.views import CollectionViewSet
from apps.followups.views import FollowUpActionViewSet
from apps.common.views import ImportViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'groups', GroupViewSet)
router.register(r'borrowers', BorrowerViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'recovery-cases', RecoveryCaseViewSet)
router.register(r'collections', CollectionViewSet)
router.register(r'follow-ups', FollowUpActionViewSet)
router.register(r'imports',ImportViewSet, basename='import')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Endpoints
    path('api/', include(router.urls)),
]