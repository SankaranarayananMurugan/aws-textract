from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from analysedocument import views

urlpatterns = [
    path('analysis/', views.DocumentAnalysisView.as_view()),
    path('train/', views.MachineLearningView.as_view()),
    path('predict/', views.PatternRecognitionView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)