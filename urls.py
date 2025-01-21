from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="Home"),
    path('Query_Results',views.Query_Results),
    path('Add_Actor_to_Movie',views.add_Actor),
    path('Record_Watching',views.record_watching),
]
