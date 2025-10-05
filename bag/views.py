from django.shortcuts import render, redirect, get_object_or_404
from product.models import Category, Product

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
    # Product
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    # Collect variation
    variations = {}
    for key, value in request.POST.items():
        if key not in ['csrfmiddlewaretoken', 'quantity', 'redirect_url']:
            variations[key] = value

    # Unique identifier 
    variation_key = '-'.join([f"{k}:{v}" for k, v in variations.items()]) if variations else None

    # Bag items
    if product.has_variation and variation_key:
        # Has Variation
        if str(item_id) in bag:
            if variation_key in bag[str(item_id)]['items_by_variation']:
                bag[str(item_id)]['items_by_variation'][variation_key]['quantity'] += quantity
            else:
                bag[str(item_id)]['items_by_variation'][variation_key] = {
                    'quantity': quantity,
                    'variations': variations,
                }
        else:
            bag[str(item_id)] = {
                'items_by_variation': {
                    variation_key: {
                        'quantity': quantity,
                        'variations': variations,
                    }
                }
            }
    else:
        # No variation
        if str(item_id) in bag:
            bag[str(item_id)]['quantity'] = bag[str(item_id)].get('quantity', 0) + quantity
        else:
            bag[str(item_id)] = {'quantity': quantity}

    request.session['bag'] = bag
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


def increment_bag_item(request, item_id):
    bag = request.session.get('bag', {})
    redirect_url = request.POST.get('redirect_url') or request.META.get('HTTP_REFERER', '/')

    variation_key = request.POST.get('variation_key')

    if str(item_id) in bag:
        item_data = bag[str(item_id)]

        # Product has variations
        if 'items_by_variation' in item_data and variation_key:
            if variation_key in item_data['items_by_variation']:
                current_qty = item_data['items_by_variation'][variation_key]['quantity']
                if current_qty < 99:
                    item_data['items_by_variation'][variation_key]['quantity'] = current_qty + 1

        # No variation
        elif 'quantity' in item_data:
            if item_data['quantity'] < 99:
                item_data['quantity'] += 1

    request.session['bag'] = bag
    return redirect(redirect_url)


def decrement_bag_item(request, item_id):
    bag = request.session.get('bag', {})
    redirect_url = request.POST.get('redirect_url') or request.META.get('HTTP_REFERER', '/')
    variation_key = request.POST.get('variation_key')

    if str(item_id) in bag:
        item_data = bag[str(item_id)]

        # Product has variations
        if 'items_by_variation' in item_data and variation_key:
            if variation_key in item_data['items_by_variation']:
                current_qty = item_data['items_by_variation'][variation_key]['quantity']
                if current_qty > 1:
                    item_data['items_by_variation'][variation_key]['quantity'] = current_qty - 1
                else:
                    item_data['items_by_variation'][variation_key]['quantity'] = 1

        # No variations
        elif 'quantity' in item_data:
            if item_data['quantity'] > 1:
                item_data['quantity'] -= 1
            else:
                item_data['quantity'] = 1

    request.session['bag'] = bag
    return redirect(redirect_url)




