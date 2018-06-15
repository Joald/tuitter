from django.conf.urls import include, url
from django.contrib.auth import views as views_auth
from . import views

# Letters, digits and @/./+/-/_
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<tuit_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^users/(?P<username>(\w|@|\.|\+|-|_)+)/$', views.user_page, name='user_page'),
    url(r'^users/(?P<username>(\w|@|\.|\+|-|_)+)/friends/$', views.friends, name='user_page'),
    url(r'^login/$', views_auth.LoginView.as_view(template_name='registration/login.html'), name='login'),
    url(r'^logout/$', views_auth.LogoutView.as_view(next_page='index'), name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^new_tuit', views.new_tuit, name='new_tuit'),
    url(r'^login_required', views.login_required, name='login_required'),
]
