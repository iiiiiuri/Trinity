from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('fileupload/', views.fileupload, name='fileupload'),
    path('fileData/', views.fileData, name='fileData'),
    path('fileEdit/<int:id>/<str:data>', views.edit_funcionario, name='fileEdit'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),


    #api
    path('atualizar_horario/', views.atualizar_horario, name='atualizar_horario'),
    path('criar_nova_marcacao/', views.criar_nova_marcacao, name='criar_nova_marcacao'),
    path('<int:funcionario_id>/alterar_registro/', views.alterar_registro, name='alterar_registro'),
    path('deletar_marcacao/', views.deletar_marcacao, name='deletar_marcacao'),
    path('delete_marcacao_unica/', views.delete_marcacao_unica, name='delete_marcacao_unica'),
    path('atualizar_configuracao/', views.atualizar_configuracao, name='atualizar_configuracao'),
    path('reset_database/', views.reset_database, name='reset_database'),
    ]