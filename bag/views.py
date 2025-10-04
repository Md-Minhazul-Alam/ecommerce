from django.shortcuts import render, redirect
from product.models import Category

# Create your views here.
def view_bag(request):
   # Menus
    menuCategories = Category.objects.filter(
        is_active=True,
        parent_category__isnull=True
    ).prefetch_related("subcategories")

    
    context = {
        'menuCategories': menuCategories,
    }

    return render(request, "bag/bag.html", context)


def add_to_bag(request, item_id):
   
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)


def remove_from_bag(request, item_id):
    # Remove iTem
    bag = request.session.get('bag', {})
    redirect_url = request.POST.get('redirect_url') or request.META.get('HTTP_REFERER', '/')

    if str(item_id) in bag:
        bag.pop(str(item_id))
        request.session['bag'] = bag
        print("Updated bag:", bag)
    else:
        print("Item not found in bag:", item_id)

    return redirect(redirect_url)

