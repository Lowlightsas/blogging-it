from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm,UserEditForm,ProfileEditForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from post.models import Post    
from django.shortcuts import redirect
from .models import Profile,Contact

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form':user_form})



@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'account/edit.html',{'user_form':user_form,'profile_form':profile_form})

@login_required
def profile(request):
    profile = request.user.profile
    followers = request.user.followers.all() 
    subscriptions = Contact.objects.filter(user_from=request.user)
    user_posts = Post.objects.filter(author=request.user)
    return render(request,'account/profile.html',{'user':request.user,'profile':profile,'followers':followers,'user_posts':user_posts,'subscriptions':subscriptions})


@login_required
def user_profile_detail(request,username):
    user = get_object_or_404(User,username=username)
    user_posts = Post.objects.filter(author=user)
    
    return render(request,'account/user_profile.html',{'user':user,'user_posts':user_posts})

@login_required 
def subscribe(request,user_id):
    user_to = get_object_or_404(User,id=user_id)
    user_from = request.user

    if user_from != user_to and not user_from.following.filter(id=user_to.id).exists():
        Contact.objects.create(user_from=user_from, user_to=user_to)
    return redirect('account:user_detail', username=user_to.username)

@login_required
def unsubscribe(request, user_id):
    user_to = get_object_or_404(User, id=user_id)
    user_from = request.user

    
    Contact.objects.filter(user_from=user_from, user_to=user_to).delete()
    
    return redirect('account:user_detail',username=user_to.username)
    
