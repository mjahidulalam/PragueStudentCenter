from django.urls import path
from .views import ( 
    
    department_subjects,
    subject_list_by_department,
    post_list_all,
    post_list_categories,
    post_detail,
    create_post,
    PostUpdateView,
    PostDeleteView,
    create_subject,
    search_result,
    test_subject_list
)

app_name = 'forum'

urlpatterns = [
    path("", department_subjects, name="home"),
    path("posts/", post_list_all, name="post_all"),
    path("department/<int:dept_id>", subject_list_by_department, name="dept_filter"),
    path("posts/<slug>", post_list_categories, name="posts"),
    path("post/<pk>/<slug>/", post_detail, name="detail"),
    path("create_post/", create_post, name="create_post"),
    path("post/<int:pk>/<slug>/update/", PostUpdateView.as_view(), name="update_post"),
    path("post/<int:pk>/<slug>/delete/", PostDeleteView.as_view(), name="delete_post"),
    path("new_topic/", create_subject, name="create_subject"),
    path("search_topic/", search_result, name="search_topic"),
    path("test_list_post/", test_subject_list, name="test"),
]