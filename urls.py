import os

from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import redirect

from tagging.views import tagged_object_list

from djangopeople import views, api #, clustering
from djangopeople.models import DjangoPerson


def perm_redirect(url):
    return lambda req: redirect(url, permanent=True)

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^about/$', views.about, name='about'),
    url(r'^recent/$', views.recent, name='recent'),
    url(r'^recover/$', views.lost_password, name='recover'),
    url(r'^recover/(?P<username>[a-z0-9]{3,})/(?P<days>[a-f0-9]+)/(?P<hash>[a-f0-9]{32})/$',
        views.lost_password_recover, name='do_recover'),
    url(r'^signup/$', views.signup, name='signup'),

    #openid stuff
    url(r'^openid/$', 'django_openidconsumer.views.begin', {
        'sreg': 'email,nickname,fullname',
        'redirect_to': '/openid/complete/',
    }, name='openid_begin'),
    url(r'^openid/complete/$', 'django_openidconsumer.views.complete', name='openid_complete'),
    url(r'^openid/whatnext/$', views.openid_whatnext, name='opeind_whatnext'),
    url(r'^openid/signout/$', 'django_openidconsumer.views.signout', name='openid_signout'),
    url(r'^openid/associations/$', 'django_openidauth.views.associations', name='openid_associations'),

    url(r'^search/$', views.search, name='search'),
#    (r'^openid/$', views.openid),

    url(r'^skills/(?P<tag>.*)/$', views.skill, name='skill_detail'),
    url(r'^skills/$', views.skill_cloud, name='skill_cloud'),

    url(r'^api/irc_lookup/(.*?)/$', api.irc_lookup, name='irc_lookup'),
    url(r'^api/irc_spotted/(.*?)/$', api.irc_spotted, name='irc_spotted'),
    url(r'^irc/active/$', views.irc_active, name='irc_active'),
    url(r'^irc/(.*?)/$', api.irc_redirect, name='irc_redirect'),

    (r'^uk/$', perm_redirect('/gb/')),
    url(r'^([a-z]{2})/$', views.country, name='country_detail'),
    url(r'^([a-z]{2})/sites/$', views.country_sites, name='country_sites'),
    url(r'^([a-z]{2})/skills/$', views.country_skill_cloud, name='country_skill_cloud'),
    url(r'^([a-z]{2})/skills/(.*)/$', views.country_skill, name='country_skill'),
    url(r'^([a-z]{2})/looking-for/(freelance|full-time)/$', views.country_looking_for, name='country_looking_for'),
    url(r'^([a-z]{2})/(\w+)/$', views.region, name='country_region'),

    url(r'^([a-z0-9]{3,})/$', views.profile, name='user_profile'),
    url(r'^([a-z0-9]{3,})/bio/$', views.edit_bio, name='edit_bio'),
    url(r'^([a-z0-9]{3,})/skills/$', views.edit_skills, name='edit_skills'),
    url(r'^(?P<username>[a-z0-9]{3,})/password/$',
        views.edit_password, name='edit_password'),
    url(r'^([a-z0-9]{3,})/account/$', views.edit_account, name='edit_account'),
    url(r'^([a-z0-9]{3,})/portfolio/$', views.edit_portfolio, name='edit_portfolio'),
    url(r'^([a-z0-9]{3,})/location/$', views.edit_location, name='edit_location'),
    url(r'^([a-z0-9]{3,})/finding/$', views.edit_finding, name='edit_finding'),
    url(r'^([a-z0-9]{3,})/upload/$', views.upload_profile_photo, name='upload_profile_photo'),
    url(r'^([a-z0-9]{3,})/upload/done/$', views.upload_done, name='upload_done'),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)