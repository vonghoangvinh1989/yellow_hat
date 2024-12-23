"""
URL configuration for yellow_hat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="/main")),
    path("main/", include("main_app.urls")),
    path("planning/", include("planning.urls")),
    path("passive-recon/", include("passive_recon.urls")),
    path("active-recon/", include("active_recon.urls")),
    path("vulnerability-assessment/", include("vulnerability_assessment.urls")),
    path("enumeration/", include("enumeration.urls")),
    path("exploitation/", include("exploitation.urls")),
    path("post-exploitation/", include("post_exploitation.urls")),
    path("digital-forensic/", include("digital_forensic.urls")),
    path("report/", include("report.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
