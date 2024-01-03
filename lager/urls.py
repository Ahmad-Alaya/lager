"""
URL configuration for lager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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


from django.urls import path
from django.contrib import admin
from inventory.views import inventar_liste, verkauf, verkaufliste, send_email, statistic, storniere_rechnung, stornoliste

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inventar_liste, name='inventar_liste'),
    path('verkauf/<int:id>/<str:type>/', verkauf, name='verkauf'),
    path('verkauf_liste/', verkaufliste, name='verkauf_liste'),
    path('storno_liste/', stornoliste, name='storno_liste'),
    path('send-email/', send_email, name='send_email'),
    path('statistic/', statistic, name="statistic"),
    path('storniere-rechnung/', storniere_rechnung, name='storniere_rechnung'),

]

