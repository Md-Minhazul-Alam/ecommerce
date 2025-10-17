from django.shortcuts import render, redirect, get_object_or_404
from product.models import Category, Product
from django.contrib import messages
from decimal import Decimal

# View Bag
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


# Add to Bad
def add_to_bag(request, item_id):
    try:
        # Product
        product = get_object_or_404(Product, pk=item_id)
        quantity = int(request.POST.get('quantity', 1))
        redirect_url = request.POST.get('redirect_url') or request.META.get('HTTP_REFERER', '/')
        bag = request.session.get('bag', {})

        # Collect variations
        variations = {}
        for key, value in request.POST.items():
            if key not in ['csrfmiddlewaretoken', 'quantity', 'redirect_url'] and value:
                variations[key] = value

        # Unique key for variation
        variation_key = '-'.join([f"{k}:{v}" for k, v in variations.items()]) if variations else None

        # Add item to bag
        if product.has_variation and variation_key:
            # Product has variations
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

            # Variation message
            variation_text = ', '.join([f"{k}: {v}" for k, v in variations.items()])
            messages.success(request, f"{product.product_name} ({variation_text}) added to your bag!")

        elif not product.has_variation:
            # Product has no variation
            if str(item_id) in bag:
                bag[str(item_id)]['quantity'] = bag[str(item_id)].get('quantity', 0) + quantity
            else:
                bag[str(item_id)] = {'quantity': quantity}
            messages.success(request, f"{product.product_name} added to your bag!")

        else:
            messages.error(request, f"Please select all required variations for {product.product_name}.")
            return redirect(redirect_url)

        # Save session
        request.session['bag'] = bag
        return redirect(redirect_url)

    except Exception as e:
        messages.error(request, f"Something went wrong: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', '/'))


# Remove Item 
def remove_from_bag(request, item_id):
    try:
        bag = request.session.get('bag', {})
        redirect_url = request.POST.get('redirect_url') or request.META.get('HTTP_REFERER', '/')

        if str(item_id) in bag:
            bag.pop(str(item_id))
            request.session['bag'] = bag
            messages.success(request, "Item removed from your bag.")
        else:
            messages.error(request, "Item not found in your bag.")

        return redirect(redirect_url)

    except Exception as e:
        messages.error(request, f"Something went wrong: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', '/'))


# Increment Item
def increment_bag_item(request, item_id):
    try:
        bag = request.session.get('bag', {})
        redirect_url = request.POST.get('redirect_url') or request.META.get('HTTP_REFERER', '/')
        variation_key = request.POST.get('variation_key')

        product = get_object_or_404(Product, pk=item_id)
        item_data = bag.get(str(item_id))

        if not item_data:
            messages.error(request, "Item not found in your bag.")
            return redirect(redirect_url)

        # Product with variations
        if product.has_variation:
            if 'items_by_variation' not in item_data:
                messages.error(request, "Item data missing variations.")
            elif not variation_key or variation_key not in item_data['items_by_variation']:
                messages.error(request, f"Variation not found in your bag. Available keys: {list(item_data.get('items_by_variation', {}).keys())}")
            else:
                current_qty = item_data['items_by_variation'][variation_key]['quantity']
                if current_qty < 99:
                    item_data['items_by_variation'][variation_key]['quantity'] += 1
                    messages.success(request, "Quantity increased.")
                else:
                    messages.error(request, "Maximum quantity reached for this item.")

        # Product without variations
        else:
            if 'quantity' not in item_data:
                messages.error(request, "Item data missing quantity.")
            else:
                if item_data['quantity'] < 99:
                    item_data['quantity'] += 1
                    messages.success(request, "Quantity increased.")
                else:
                    messages.error(request, "Maximum quantity reached for this item.")

        # Save back to session
        bag[str(item_id)] = item_data
        request.session['bag'] = bag
        return redirect(redirect_url)

    except Exception as e:
        messages.error(request, f"Something went wrong: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', '/'))


# Decrement Item
def decrement_bag_item(request, item_id):
    try:
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
                        messages.success(request, "Quantity decreased.")
                    else:
                        messages.error(request, "Minimum quantity is 1.")
                else:
                    messages.error(request, "Variation not found in your bag.")

            # No variations
            elif 'quantity' in item_data:
                if item_data['quantity'] > 1:
                    item_data['quantity'] -= 1
                    messages.success(request, "Quantity decreased.")
                else:
                    messages.error(request, "Minimum quantity is 1.")
            else:
                messages.error(request, "Item data is invalid.")

        else:
            messages.error(request, "Item not found in your bag.")

        request.session['bag'] = bag
        return redirect(redirect_url)

    except Exception as e:
        messages.error(request, f"Something went wrong: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', '/'))

