from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from .forms import CreateUserForm,QuestionForm,UserProfileForm,UserProfileMain
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Topic,Question,Point,Message,CorrectAnswer,Profile
from django.contrib.auth.models import User

@login_required(login_url='login')
def home(request):
    q = request.GET.get('search') if request.GET.get('search') != None else ''
    questions = Question.objects.filter(
        Q(topic__name__icontains =q) |
        Q(name__icontains =q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    top_users = Point.objects.all().order_by('-points')[:7]
    context = {'topics':topics, 'questions':questions,'top_users':top_users }
    return render(request,"base/index.html",context)

@login_required(login_url='login')
def question(request):
    return HttpResponse("Question Page")

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        username = request.POST['username']

        if form.is_valid():
            form.save()
            user = User.objects.get(username=username)
            point = Point(user=user,points=100)
            pictures = Profile(user=user)
            pictures.save()
            point.save()
        

            return redirect('home')

    context = {'form':form}
    return render(request,"base/login.html",context)

def loginPage(request):
    page = "login"
    if request.method == 'POST':
       username= request.POST.get('username')
       password= request.POST.get('password')
       user = authenticate(request,username=username,password=password)

       if user is not None:
        login(request,user)
  
        return redirect('home')
    
    context = {'page':page}
    return render(request, "base/login.html",context)

def following(request):
    q = request.GET.get('search') if request.GET.get('search') != None else ''
    questions = Question.objects.filter(
        Q(topic__name__icontains =q) |
        Q(name__icontains =q) |
        Q(description__icontains=q) 
        
    )

    topics = Topic.objects.all()
    top_users = Point.objects.all().order_by('-points')[:7]
    context = {'topics':topics, 'questions':questions,'top_users':top_users }
    return render(request,"base/following.html",context)


@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def createPost(request):
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
    
        if form.is_valid():
            
            question = form.save(commit=False)
            question.host = request.user
            question.save()
            changePoints(request.user,-question.point)
            return redirect('home')
    context = {'form':form,'topics':Topic.objects.all()}
    return render(request,"base/post_question.html",context)

@login_required(login_url='login')
def question(request,pk):

    
    quest = Question.objects.get(id=pk)
    quest_messages = quest.message_set.all().order_by('-created')
    participants = quest.participants.all()
    correctans = CorrectAnswer.objects.filter(question = quest)
    quest.participants.add(quest.host)
    if not correctans:
        msg_id = None
    else:
        msg_id = CorrectAnswer.objects.get(question= quest).message.id


    
    
    if request.POST.get('message_submit') == 'submit':
        
        Message.objects.create(
            user = request.user,
            question = quest,
            message = request.POST.get('answer')
        )
        quest.participants.add(request.user)
        return redirect('question',pk=quest.id)

    if request.POST.get('like_message'):
        
        msg_like = quest.message_set.get(id=request.POST.get('like_message'))
        if msg_like.like.exists():
            msg_like.like.remove(request.user)
        else:
            msg_like.like.add(request.user)

        if msg_like.dislike.exists():
            msg_like.dislike.remove(request.user)
        

        return redirect('question',pk=quest.id) 

    if request.POST.get('unlike_message'):
        
        msg_unlike = quest.message_set.get(id=request.POST.get('unlike_message'))
        if msg_unlike.dislike.exists():
            msg_unlike.dislike.remove(request.user)
        else:
            msg_unlike.dislike.add(request.user)

        
        if msg_unlike.like.exists():
            msg_unlike.like.remove(request.user)
        

        return redirect('question',pk=quest.id)

    if request.POST.get('like_post'):
        if quest.like.exists():
            quest.like.remove(request.user)
        else:
            quest.like.add(request.user)

        if quest.dislike.exists():
            quest.dislike.remove(request.user)
        return redirect('question',pk=quest.id)
    
    if request.POST.get('unlike_post'):
        if quest.dislike.exists():
            quest.dislike.remove(request.user)
        else:
            quest.dislike.add(request.user)

        if quest.like.exists():
            quest.like.remove(request.user)

        
        return redirect('question',pk=quest.id)
    
    if request.POST.get('correct_message'): 
        msg_correct = quest.message_set.get(id=request.POST.get('correct_message'))

        if not correctans:
            CorrectAnswer.objects.create(
                question = quest,
                message = msg_correct
            )
            changePoints(msg_correct.user,+quest.point)
            msg_id = CorrectAnswer.objects.get(question= quest).message.id
            
        else:
            msg_id = CorrectAnswer.objects.get(question= quest).message.id
            changePoints(msg_correct.user,-quest.point)
            correctans.delete()
            if( msg_id != int(request.POST.get('correct_message'))):
                CorrectAnswer.objects.create(
                question = quest,
                message = msg_correct
                )
                changePoints(msg_correct.user,+quest.point)

            
        return redirect('question',pk=quest.id)
    
        
    
    context={'question':quest,'messages':quest_messages,'msg_id':msg_id,
    'topics':Topic.objects.all(),
    'user_post_like':quest.like.filter(username=request.user).exists(),
    'user_post_dislike':quest.dislike.filter(username=request.user).exists(),
    'participants':participants
    }
    return render(request,'base/question.html',context)
@login_required(login_url='login')
def userProfile(request,un):
    profileuser = User.objects.get(username=un)
    question =  Question.objects.filter(host = profileuser)
    if request.POST.get('follow'):
        
        if profileuser.extendprofile.follower.exists():
            profileuser.extendprofile.follower.remove(request.user)
            request.user.extendprofile.following.remove(profileuser)
        else:
            profileuser.extendprofile.follower.add(request.user)
            request.user.extendprofile.following.add(profileuser)
        
        return redirect('userprofile',un=profileuser)

        
        

    context = {'user':profileuser,'questions':question}
    return render(request,'base/profile.html',context)
@login_required(login_url='login')
def userEdit(request,pk):
    profile = User.objects.get(id=pk)
    form = UserProfileForm(instance=profile.extendprofile)

    if request.user != profile :
        return redirect('home')

    if request.method == 'POST':
        print("Pressed")
        form = UserProfileForm(request.POST,request.FILES,instance=profile.extendprofile)

        if  form.is_valid():
            print(form)
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'base/user-edit.html',context)

def userFollow(request,pk):
    un = User.objects.get(id=pk)
    un.follower.add(request.user)
    return redirect('home')
    
@login_required(login_url='login')
def updatePost(request,pk):

    question = Question.objects.get(id=pk)
    form = QuestionForm(instance=question)

    if request.user != question.host :
        return redirect('home')

    if request.method == 'POST':
        form = QuestionForm(request.POST,instance=question)
        if form.is_valid():
            form.save()
            changePoints(request.user,-question.point)
            return redirect('home')
    
    context = {'form':form,'topics':Topic.objects.all(),'update':True}
    return render(request,"base/post_question.html",context)
@login_required(login_url='login')
def deletePost(request,pk):
    print(pk)
    question = Question.objects.get(id=pk)
    question.delete()
    return redirect('home')
@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return redirect('home')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    return render(request,'base/delete.html',{'obj':message})
    

def changePoints(username,value):
    user = User.objects.get(username=username)
    def_point = Point.objects.get(user=user)
    def_point.points = def_point.points + value
    def_point.save()



        