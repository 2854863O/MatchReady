from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


#make these models 
from MatchReady.models import Team, Player, Fan, Coach, TeamSheet

#make these forms
from MatchReady.forms import NewTeamForm, FindTeamForm, UserForm, UserProfileForm, AnnouncementForm




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




def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()



            #Add coach, fan into models, default is player
            user.set_password(user.password)
            user.set_coach(user.isCoach)
            user.set_fan(user.isFan)



            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()

            registered = True
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

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
    context_dict = {}
    #
    #
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
    context_dict = {}
    #
    #
    return render(request,'MatchReady/announcements.html',context=context_dict)

@login_required
def matches(request):
    context_dict = {}
    #
    #
    return render(request,'MatchReady/matches.html',context=context_dict)

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