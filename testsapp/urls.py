from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^signup/$', views.signup_form, name='signup'),
    url(r'^login/$', views.login_form, name='login'),
    url(r'^logout/$', views.logout_form, name='logout'),
    url(r'^$', views.home, name='home'),
    url(r'^add_test/(?P<testgroup_id>[0-9])?$', views.add_test, name='add_test'),
    url(r'^edit_test/(?P<test_id>[0-9]+)$', views.edit_test, name='edit_test'),
    url(r'^del_test/(?P<test_id>[0-9]+)$', views.delete_test, name='del_test'),
    url(r'^add_question/(?P<test_id>[0-9]+)$', views.add_question, name='add_question'),
    url(r'^edit_question/(?P<question_id>[0-9]+)$', views.edit_question, name='edit_question'),
    url(r'^del_question/(?P<question_id>[0-9]+)$', views.delete_question, name='del_question'),
    url(r'^add_testgroup/$', views.add_testgroup, name='add_testgroup'),
    url(r'^edit_testgroup/(?P<testgroup_id>[0-9]+)$', views.edit_testgroup, name='edit_testgroup'),
    url(r'^del_testgroup/(?P<testgroup_id>[0-9]+)$', views.delete_testgroup, name='del_testgroup'),
    url(r'^tests_without_group/$', views.tests_without_group, name='tests_without_group'),
    url(r'^next_question/(?P<test_id>[0-9]+)$', views.UserQuestion.as_view(), name='next_question'),
    url(r'^permission_denied/$', TemplateView.as_view(template_name='testsapp/permission_denied.html'), name='permission_denied'),
    url(r'^show_tests/(?P<testgroup_id>[0-9]+)?$', views.show_tests, name='show_tests'),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
