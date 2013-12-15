from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^/$', 'buildengine.views.home'),
    url(r'^/build/$', 'buildengine.views.backOffice'),
    url(r'^/build/edittext/(?P<idText>\w+)/$', 'buildengine.views.editText'),
    url(r'^/build/addimage/$', 'buildengine.views.addImage'),
    url(r'^/build/deleteimage/(?P<idImage>\w+)/$', 'buildengine.views.deleteImage'),
    url(r'^/build/editwebsite/$', 'buildengine.views.editWebsite'),
    url(r'^/build/addwork/(?P<idTopic>\w+)/$', 'work.views.addWork'),
    url(r'^/build/addtopic/$', 'work.views.addTopic'),
    url(r'^/build/edittopic/(?P<idTopic>\w+)/$', 'work.views.editTopic'),
    url(r'^/build/deletetopic/(?P<idTopic>\w+)/$', 'work.views.deleteTopic'),
    url(r'^/build/editwork/(?P<idWork>\w+)/$', 'work.views.editWork'),
    url(r'^/build/editimagework/(?P<idWork>\w+)/$', 'work.views.editImageWork'),
    url(r'^/build/managework/$', 'work.views.manageWork'),
    url(r'^/build/deletework/(?P<idWork>\w+)/$', 'work.views.deleteWork'),
    url(r'^/build/editaccount', 'authentification.views.editAccount'),
)