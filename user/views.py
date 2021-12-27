from django.http.response import Http404
# from django.urls.base import reverse
from django.urls import reverse
from django.views import generic, View
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UpdateForm, UserForm
from django.urls import reverse_lazy
from main.models import Author, Post, Comment, Reply
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView, DetailView, UpdateView, DeleteView, ListView, #FormView
)

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator

from django.contrib.auth.models import User

class Register(generic.CreateView): 
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url =  reverse_lazy('user:login')

def signup(request):
    context = {}
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            #username = form.cleaned_data.get('username')
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            domain = get_current_site(request).domain
            link = reverse('user:activate', kwargs={'uidb64': uidb64, 'token': token})

            activate_url = 'http://' + domain + link

            email_subject = "Account Activation"
            email_body = f"Hi {user.username}, Please use the following link to activate your account\n {activate_url}"

            email = EmailMessage(
                email_subject,
                email_body,
                'praguestudentcenter@gmail.com',
                [user.email],
            )
            email.send(fail_silently=False)

            login(request, user)
            return redirect("user:verify")
    else:
        form = UserRegisterForm()

    context.update({
        "form": form, 
        "title": "Signup",
    })
    return render(request, 'users/register.html', context)

def verification(request):
    context= {}
    return render(request, 'users/verification.html', context)

def profile(request, pk, username):
    user = request.user
    profile = User.objects.get(id=pk)
    profile_info = Author.objects.get(user=pk)
    posts = Post.objects.filter(user=profile.id)
    # comments = Comment.objects.filter(user=profile.id)
    # replies = Reply.objects.filter(user=profile.id)
    for post in posts[:5]:
        print(post.date)

    context = {"user": user,
                "profile": profile,
                "profile_info": profile_info,
                }
    return render(request, "users/profile.html", context)

# @login_required
# def update_profile(request):
#     try:
#         context = {}
#         user = request.user
#         update_form = UpdateForm(request.POST, request.FILES, instance = user, use_required_attribute=True)
#         user_form = UserRegisterForm(request.POST, instance = user, use_required_attribute=True)
#         if request.method == "POST" :
#             if update_form.is_valid() and user_form.is_valid():
#                 update_profile = update_form.save(commit=False)
#                 update_profile.user = user 
#                 update_profile.save()
#                 user_form.save
#                 return redirect("forum:home")
        
#         context.update({
#             "update_form": update_form,
#             "user_form": user_form,
#             "user": user
#         })
#     except UnboundLocalError:
#         raise "Create an User info first" 
    
#     # finally:
#     #     context.update({
#     #         "form": form,
#     #         "user": user_info
#     #     })
#     return render(request, "users/profile_update.html", context)

class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url= "/login/"
    template_name = 'users/profile_update.html'
    model = User
    second_model = Author
    form_class = UpdateForm
    second_form_class = UserForm

    def test_func(self):
        profile = self.get_object()
        if str(self.request.user) == str(profile.username):
            return True
        print(str(profile.username)== str(self.request.user))
        return False

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        # user = UpdateForm(user=self.request.user)
        context['form2'] = self.second_form_class(instance = self.request.user)
        context['profile'] = self.second_model(user=self.request.user)
        return context

    def get_success_url(self, **kwargs):
        return reverse('user:profile', kwargs={'pk': self.request.user.id, "username": self.request.user})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = Author.objects.get(user=request.user.id)
        form = self.form_class(request.POST, request.FILES, instance = user)
        form2 = self.second_form_class(request.POST, instance = request.user)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            # return redirect("forum:home")
            return redirect('user:profile', request.user.pk, request.user.username)
        else:
            print('summit')
            return self.render_to_response(
              self.get_context_data(form2=form2))
    

class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url= "/login/"
    template_name = 'users/profile_delete.html'
    model = User
    context_object_name = 'user'
    success_url = '/'

    def test_func(self):
        user = self.get_object()
        if str(self.request.user) == str(user.username):
            return True
        return False


class VerificationView(View):
    def get(self, request, uidb64, token):
        p = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=p)
        user.is_active = True
        user.save()
        author_form = UpdateForm()
        # if author_form.is_valid():
        #     print('somthing')
        #     update_profile = author_form.save(commit=False)
        #     update_profile.user = user 
        #     update_profile.save()
        print(user)
        update_profile = author_form.save(commit=False)
        update_profile.user = user 
        update_profile.save()

        # return redirect('user:login')
        return redirect('user:update', user.pk, user)




