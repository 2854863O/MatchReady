from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

#Assumptions - 
# announcements is a simple model with a stack field so we can pop off the latest announcements
# matches might have to have a datetime field and be an object for a specific match
# matches could also have a deque datatype and when a match is played it gets removed

#make these models, player, fan and coach could all be subclasses of a base

from MatchReady.models import Team, Player, Fan, Coach, TeamSheet, Matches

#make these forms, player, fan and coach form could all be subclasses of a base
from MatchReady.forms import NewTeamForm, FindTeamForm, PlayerForm, FanForm, CoachForm, UserForm, AnnouncementForm




def home (request):
    context_dict = {}
    #
    #
    response = render(request, 'MatchReady/home.html', context=context_dict)
    return response


def about (request):
    context_dict = {}
    #
    #
    response = render(request, 'MatchReady/about.html', context=context_dict)
    return response




def player_register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = PlayerProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            #Add coach, fan into models
            user.set_password(user.password)
            user.set_coach(user.isCoach)
            user.set_fan(user.isFan)
            user.set_player(user.isPlayer)

            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()

            registered = True
    else:
        user_form = UserForm()
        profile_form = PlayerProfileForm()

    return render(request, 'MatchReady/register.html', context={
        'user_form':user_form,
        'profile_form':profile_form,
        'registered':registered
    })

def fan_register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = FanProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            #Add coach, fan into models
            user.set_password(user.password)
            user.set_coach(user.isCoach)
            user.set_fan(user.isFan)
            user.set_player(user.isPlayer)

            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()

            registered = True
    else:
        user_form = UserForm()
        profile_form = FanProfileForm()

    return render(request, 'MatchReady/register.html', context={
        'user_form':user_form,
        'profile_form':profile_form,
        'registered':registered
    })

def coach_register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = CoachProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            #Add coach, fan into models

            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()

            registered = True
    else:
        user_form = UserForm()
        profile_form = CoachProfileForm()

    return render(request, 'MatchReady/register.html', context={
        'user_form':user_form,
        'profile_form':profile_form,
        'registered':registered
    })

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('MatchReady:home'))
            else:
                return HttpResponse("Your MatchReady account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'MatchReady/login.html')
    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('MatchReady:home'))

def contact(request):
    context_dict={}
    #
    #
    return render(request,'MatchReady/contact.html', context=context_dict)

def matches(request):
    #next_matches = Match.objects.filter(finished=False).orderby('match_day')[:15]

    #for x in range 15:
    #   next_matches.append(Match.objects.all().deque.frontDequeue())
    #for x in range 15:
    #   Match.objects.all().deque.frontQueue(next_matches[x])

    context_dict = {}
    return render(request,'MatchReady/matches.html',context=context_dict)

@login_required
def my_team(request):
    context_dict = {}
    #
    #
    return render(request,'MatchReady/my_team.html',context=context_dict)

@login_required
def find_team(request):
    context_dict = {}
    #
    #
    return render(request,'MatchReady/find_team.html',context=context_dict)

@login_required
def create_team(request):
    context_dict = {}
    #
    #
    return render(request,'MatchReady/create_team.html',context=context_dict)

@login_required
def create_announcement(request):
    form = AnnouncementForm()
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('MatchReady:home'))
        else:
            print(form.errors)
            return render(request, "MatchReady/create_announcements.html", {"form": form, "errors": form.errors})  
    return render(request, 'MatchReady/create_announcements.html',{'form':form}) 

@login_required
def team_detail(request):
    context_dict = {}
    #
    #
    return render(request,'MatchReady/team_detail.html',context=context_dict)

@login_required
def team_sheet(request):
    context_dict = {}
    team_sheet = TeamSheet.objects.get
    context_dict['team_sheet'] = 
    #
    return render(request,'MatchReady/team_sheet.html',context=context_dict)

@login_required
def announcements(request):
    #
    #
    return render(request,'MatchReady/announcements.html',context=context_dict)
 

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request,'visits','1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    if (datetime.now()-last_visit_time).days>0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits

def get_server_side_cookie(request,cookie,default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category=None

    if category is None:
        return redirect(reverse('MatchReady:home'))
    
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('MatchReady:show_category',kwargs={'category_name_slug':category_name_slug}))
            else:
                print(form.errors)
    context_dict = {'form': form,'category': category}
    return render(request, 'MatchReady/add_page.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict={}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages']=None
        context_dict['category']=None
    return render(request, 'MatchReady/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('MatchReady:home'))
        else:
            print(form.errors)
            return render(request, "MatchReady/add_category.html", {"form": form, "errors": form.errors})  
    return render(request, 'MatchReady/add_category.html',{'form':form}) 