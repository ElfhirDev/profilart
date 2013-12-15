from work.form import *
from profilart.settings import USER_IMAGE_AVERAGE_PATH
from buildengine.views import userBackOfficePermission
from django.shortcuts import render_to_response, HttpResponseRedirect, render
from buildengine.models import *
from work.models import *
from django.template import RequestContext
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from buildengine.form import TextForm, ImageForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import StringIO
import os

def home(request, username, idWork):
    work = Work.objects.get(id=idWork)
    return render(request, 'buildengine/work.html', {'work' : work})

def addWork(request, idTopic, username):
    if userBackOfficePermission(request, username):
        workForm = WorkForm()
        #If the form has been sent
        if request.method == 'POST':
            form = WorkForm(request.POST, request.FILES)
            if form.is_valid():
                requestName = request.POST['name']
                requestImage = request.FILES['image']  
                requestText = request.POST['text']
                requestKeywords = request.POST['keywords']
                requestWidth = request.POST['width']
                requestHeight = request.POST['height']
                requestCreated = request.POST['dateCreated']
                requestMaterial = request.POST['material']
                requestLocal = request.POST['current_local']
                requestType = request.POST.getlist('type')
                #Create new image in the database
                user = User.objects.get(username=username)
                workTopic = WorkTopic.objects.get(id=idTopic)
                #Create Work in the database
                contentType = ContentType.objects.get(model="work")
                work = Work(name=requestName, text=requestText, user_id=user.id, image=requestImage, content_type_id=contentType.id,
                            work_topic_id=workTopic.id, keywords=requestKeywords, date_created=requestCreated ,width=requestWidth, height=requestHeight,
                            material=requestMaterial, current_local=requestLocal)
                work.save()
                #Create WorkType in the database
                for value in requestType:
                    workType = WorkType(idType=value, idWork=work)
                    workType.save()
                #Resize
                image = Image.open(work.image)
                image.thumbnail((820, 820), Image.ANTIALIAS)
                image.save(work.image.path)
                return HttpResponseRedirect("/"+username+"/build/managework")
            return render(request, 'form/addwork.html', {'form' : form, 'idTopic': idTopic})
        return render(request, 'form/addwork.html', {'form' : workForm, 'idTopic': idTopic})
    return HttpResponseRedirect("/")

def addTopic(request, username):
    if userBackOfficePermission(request, username):
        workForm = WorkTopicForm()
        if request.method == 'POST':
                form = WorkTopicForm(request.POST)
                if form.is_valid():
                    requestName = request.POST['name']
                    requestText = request.POST['text']
                    requestType = request.POST.getlist('type')
                    user = User.objects.get(username=username)
                    contentType = ContentType.objects.get(model="worktopic")
                    workTopic = WorkTopic(name=requestName, text=requestText, user_id=user.id, content_type_id=contentType.id)
                    workTopic.save()
                    #Create WorkType in the database
                    for value in requestType:
                        workType = WorkTopicType(idType=value, idWork=workTopic)
                        workType.save()
                    return HttpResponseRedirect("/"+username+"/build/managework")
                return render(request, 'form/addtopicwork.html', {'form' : form})
        return render(request, 'form/addtopicwork.html', {'form' : workForm})
    return HttpResponseRedirect("/")

def editTopic(request, idTopic, username):
    if userBackOfficePermission(request, username):
        topic = WorkTopic.objects.get(id=idTopic)
        workTopicTypeTuple = WorkTopicType.objects.filter(idWork_id=idTopic)
        form = WorkTopicForm(initial={'name' : topic.name, 'text': topic.text, 'type' : workTopicTypeTuple})
        workTopic = WorkTopic.objects.get(id=idTopic)
        works = Work.objects.filter(work_topic_id=idTopic)
        workTopicType = WorkTopicType.objects.filter(idWork_id=idTopic)
        if request.method == 'POST':
            form = WorkTopicForm(request.POST)
            if form.is_valid():
                requestName = request.POST['name']
                requestText = request.POST['text']
                requestType = request.POST.getlist('type')
                workTopic.name = requestName
                workTopic.text = requestText
                workTopic.save()
                WorkTopicType.objects.filter(idWork_id=idTopic).delete()
                for value in requestType:
                    workTopicType = WorkTopicType(idType=value, idWork=workTopic)
                    workTopicType.save()
                return HttpResponseRedirect("/"+username+"/build/edittopic/"+idTopic)
        return render(request, 'buildengine/managetopic.html', {'idTopic' : idTopic, 'workTopic' : workTopic, 'works' : works,
                                                                'workType' : workTopicType, 'form' : form})
    return HttpResponseRedirect("/")

def deleteTopic(request, idTopic, username):
    if userBackOfficePermission(request, username):
        workTopic = WorkTopic.objects.get(id=idTopic).delete()
    return HttpResponseRedirect("/"+username+"/build/managework/")

def manageWork(request, username):
    if userBackOfficePermission(request, username):
        workType = WorkType.objects.all()
        workTopic = WorkTopic.objects.filter(user_id=request.user.id)
        works = Work.objects.filter(user_id=request.user.id)
        return render(request, 'buildengine/managework.html', {'username' : username, 'blockTopic' : workTopic, 'workType' : workType,
                                                               'works' : works})
    return HttpResponseRedirect("/")

def editWork(request, username, idWork):
    if userBackOfficePermission(request, username):
        work = Work.objects.get(id=idWork)
        workTypeTuple = WorkType.objects.filter(idWork_id=idWork)
        editMetaWorkForm = EditMetaWork(initial={'name': work.name, 'text': work.text, 'keywords' : work.keywords,
                                                 'dateCreated' : work.date_created, 'width' : work.width, 'height' : work.height,
                                                 'material' : work.material, 'current_local' : work.current_local,
                                                 'type' : workTypeTuple})
        editImageWorkForm = EditImageWork()
        workType = WorkType.objects.all()
        #If the form has been sent
        if request.method == 'POST':
            form = EditMetaWork(request.POST, request.FILES)
            if form.is_valid():
                requestName = request.POST['name']
                requestText = request.POST['text']
                requestType = request.POST.getlist('type')
                work.name = requestName
                work.text = requestText
                work.save()
                WorkType.objects.filter(idWork_id=idWork).delete()
                for value in requestType:
                    workType = WorkType(idType=value, idWork=work)
                    workType.save()
                return HttpResponseRedirect("/"+username+"/build/editwork/"+idWork)
            return render(request, 'form/editwork.html', {'editMetaWorkForm' : form, 'editImageWorkForm' : editImageWorkForm,
                                                      'work': work, 'workType' : workType})
        return render(request, 'form/editwork.html', {'editMetaWorkForm' : editMetaWorkForm, 'editImageWorkForm' : editImageWorkForm,
                                                      'work': work, 'workType' : workType})
    return HttpResponseRedirect("/")

def editImageWork(request, username, idWork):
    if userBackOfficePermission(request, username):
        if request.method == 'POST':
            form = EditImageWork(request.POST, request.FILES)
            if form.is_valid():
                work = Work.objects.get(id=idWork)
                requestImage = request.FILES['image']
                work.image = requestImage
                work.save()
                #Resize
                image = Image.open(work.image)
                image.thumbnail((820, 820), Image.ANTIALIAS)
                image.save(work.image.path)
                return HttpResponseRedirect("/"+username+"/build/editwork/"+idWork)
        return HttpResponseRedirect("/"+username+"/build/editwork/"+idWork)
    return HttpResponseRedirect("/")

def deleteWork(request, username, idWork):
    if userBackOfficePermission(request, username):
        work = Work.objects.filter(id=idWork)
        work.delete()
        return HttpResponseRedirect("/"+username+"/build")
    return HttpResponseRedirect("/")

def displayTopic(request, username, nameTopic):
    user = User.objects.get(username=username)
    prefWebsite = PrefWebsite.objects.get(user_id=user.id)
    if nameTopic == "paintings": idTopic = "1"
    if nameTopic == "photographies": idTopic = "2"
    if nameTopic == "video": idTopic = "3"
    if nameTopic == "sculptures": idTopic = "4"
    if nameTopic == "installations": idTopic = "5"
    if nameTopic == "Others": idTopic = "6"
    workTopic = WorkTopicType.objects.filter(idType=idTopic, idWork_id__user=user.id)
    topics = WorkTopic.objects.filter(user_id=user.id)
    works = Work.objects.filter(user_id=user.id)
    workTopicType = WorkTopicType.objects.filter(idWork_id__user_id=user.id).order_by("idType").values_list("idType")
    firstname = user.first_name
    name = user.last_name
    return render(request, 'buildengine/templates/template1/frontoffice/topic.html', {'username' : username, 'prefWebsite' : prefWebsite,
                                                               'firstname' : firstname, 'name' : name, 'workType' : set(workTopicType),
                                                               'nameTopic' : nameTopic, 'workTopic' : workTopic, 'works' : works,
                                                               'topics': topics})

def displayCartelTopic(request, username, idTopic):
    user = User.objects.get(username=username)
    prefWebsite = PrefWebsite.objects.get(user_id=user.id)
    workTopic = WorkTopic.objects.get(id=idTopic)
    works = Work.objects.filter(work_topic_id=workTopic)
    workTopicType = WorkTopicType.objects.filter(idWork_id__user_id=user.id).order_by("idType").values_list("idType")
    firstname = user.first_name
    name = user.last_name
    return render(request, 'buildengine/templates/template1/frontoffice/carteltopic.html', {'username' : username, 'prefWebsite' : prefWebsite,
                                                           'firstname' : firstname, 'name' : name, 'topic': workTopic, 'works' : works,
                                                           'workType' : set(workTopicType)})

def displayCartelWork(request, username, idWork):
    user = User.objects.get(username=username)
    prefWebsite = PrefWebsite.objects.get(user_id=user.id)
    work = Work.objects.get(id=idWork)
    workTopic = WorkTopic.objects.get(id=work.work_topic_id)
    workTopicType = WorkTopicType.objects.filter(idWork_id__user_id=user.id).order_by("idType").values_list("idType")
    firstname = user.first_name
    name = user.last_name
    return render(request, 'buildengine/templates/template1/frontoffice/cartel.html', {'username' : username, 'prefWebsite' : prefWebsite,
                                                           'firstname' : firstname, 'name' : name, 'work' : work, 'workTopic' : workTopic,
                                                           'workType' : set(workTopicType)})


