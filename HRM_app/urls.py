from django.urls import path
from .views import DeptCreateView,DeptList,DeptDetailView,soft_delete_department,UserCreate,UserList,edit_user,deactivate_user
from django.contrib.auth.views import LoginView , LogoutView 

urlpatterns = [
    # path('',DeptList.as_view(),name='home'),
    path('',DeptList.as_view(),name='dept_list'),
    path('create_dept/',DeptCreateView.as_view(),name='create_dept'),
    path('dept_update/<int:pk>/',DeptDetailView.as_view(),name='dept_update'),
    path('dept_delete/<int:pk>/',soft_delete_department,name='dept_delete'),
    path('user_create/',UserCreate,name='user_create'),
    path('login/',LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('user_list',UserList.as_view(),name='user_list'),
     path('user_update/<int:pk>/', edit_user, name='edit_user'),
    path('user_delete/<int:pk>/', deactivate_user, name='deactivate_user'),
]