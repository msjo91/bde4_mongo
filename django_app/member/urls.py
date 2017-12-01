from django.conf.urls import url

from . import views

app_name = 'member'
urlpatterns = [
    url(r'^signin/$', views.signin_fbv, name='signin'),
    url(r'^signout/$', views.signout_fbv, name='signout'),
    url(r'^signup/$', views.signup_fbv, name='signup'),
    url(r'^signup-modelform/$', views.signup_model_form_fbv, name='signup_modelform'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/change-profile-image/$',
        views.change_profile_image, name='change_profile_image'),
]
