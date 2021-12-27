from django import forms
from django.forms.widgets import Select
from .models import Post, UploadFiles, Category


class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields =  ['title', 'content', 'categories', 'tags']

        labels = {
            'title': 'Title',
            'content': 'Body',
            'categories': 'Categories',
            'tags': 'Tags',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'name':"post_title",
                'type':"text",
                'class':"form-control bg-dark text-light",
                # 'id':"exampleFormControlInput1",
                'style': "border-color: gray;",
                'placeholder':"Title",
            }),
            
            'content': forms.Textarea(attrs={
                'name':"post_text",
                'type':"text",
                # 'class':"editable medium-editor-textarea",
                'class': "form-control bg-dark text-light",
                'style': "border-color: gray;",
                # 'id':"exampleFormControlTextarea1",
                'placeholder':"Text",
            }),

            'categories': forms.Select(attrs = { 
                'name': 'categories',
                'class': 'form-control bg-dark text-light',
                'style': "border-color: gray;",
            }),

            'tags': forms.TextInput(attrs={
                'name':"tags",
                'class': 'form-control bg-dark text-light',
                'style': "border-color: gray;",                
            })
            #'categories':forms.Select(attrs={'class':'form-control'}),
        }

class NewPostUploads(forms.ModelForm):
    class Meta:
        model = UploadFiles
        fields =  ('file_upload',)

        widgets = {
            'file_upload': forms.ClearableFileInput(attrs={
                'name':"file",
                'type':"file",
                'multiple': True}),
        }

class NewSubject(forms.ModelForm):
    class Meta:
        model = Category
        fields =  ('title', 'description', 'deptartment')

        labels = {
            'title': 'Title'
            , 'description': 'Description'
            , 'deptartment': 'Department'
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'type':"text",
                'class':"form-control bg-dark text-light",
                # 'id':"exampleFormControlInput1",
                'style': "border-color: gray;",
                'placeholder':"Title",
            }),
            
            'description': forms.Textarea(attrs={
                'type':"text",
                # 'class':"editable medium-editor-textarea",
                'class': "form-control bg-dark text-light",
                'style': "border-color: gray;",
                # 'id':"exampleFormControlTextarea1",
                'placeholder':"Description",
            }),

            'deptartment': forms.Select(attrs = { 
                'class': 'form-control bg-dark text-light',
                'style': "border-color: gray;",
            }),
        }