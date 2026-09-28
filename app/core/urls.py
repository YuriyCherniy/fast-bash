from django.urls import path

from core.views import IndexView, ServeScriptView

urlpatterns = [
    path('', IndexView.as_view(), name='index-view'),
    path('scripts/<str:filename>', ServeScriptView.as_view(), name='serve-script'),
]
