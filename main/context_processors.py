from .models import Category, CategoryDept

def search_function(request):
    search_context = {}
    topic = Category.objects.all()
    if "search" in request.GET:
        query = request.GET.get("q")
        #Filter starts here
        search_box = request.GET.get("search-box")
        if search_box == "Descriptions":
            objects = topic.filter(content__icontains=query)
        else:
            objects = topic.filter(title__icontains=query)
        #ends here
        search_context = {
            "objects":objects,
            "query":query,
        }
    return search_context

def list_department_function(request):
    dept_context = {
        "departments": CategoryDept.objects.all()
    }
    return dept_context
