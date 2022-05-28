from django.shortcuts import render
from ecommerce.models import Item
# Create your views here.


def home(request):
    items_list = Item.objects.all()
    items_list = items_list.order_by("-id")
    first_new_item = items_list[0]
    second_new_item = items_list[1]
    third_new_item = items_list[2]
    new_items_list = [first_new_item, second_new_item, third_new_item]
    context = {
        #"first_new_item": first_new_item,
        #"second_new_item": second_new_item,
        #"third_new_item": third_new_item,
        "new_items_list": new_items_list
    }

    return render(request, "home.html", context)

def handle_404(request, exception):
    return render(request, "Errors/404.html")