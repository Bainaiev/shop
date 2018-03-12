from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'shop/registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'shop/registration/logged_out.html', 'next_page': '/shop/home'}, name='logout'),
    url(r'^password_reset/$', auth_views.password_reset, {
        'template_name': 'shop/registration/password_reset_form.html',
        'email_template_name': 'shop/registration/password_reset_email.html',
        'subject_template_name': 'shop/registration/password_reset_subject.txt'
        }, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {
        'template_name': 'shop/registration/password_reset_done.html'
        }, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {
        'template_name': 'shop/registration/password_reset_confirm.html'
        }, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, {
        'template_name': 'shop/registration/password_reset_complete.html'
        }, name='password_reset_complete'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/change_password/$', views.change_password, name='change_password'),
    url(r'^home/$', views.home),
    url(r'^about/$', views.about),
    url(r'^clothing/$', views.clothing),
    url(r'^shoes/$', views.shoes),
    url(r'^electronics/$', views.electronics),
    url(r'^perfumes/$', views.perfumes),
    url(r'^contact/$', views.contact),
    url(r'^item/([0-9]{1,6})$', views.item),
    url(r'^add_checkout/([0-9]{1,6})$', views.add_checkout),
    url(r'^nav/$', views.nav),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
]
