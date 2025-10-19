from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import QuickLink, LegalLink, WebsiteSetting

def quick_link_detail(request, slug):
    """Display detail page for a quick link"""
    quick_link = get_object_or_404(QuickLink, slug=slug, is_active=True)
    setting = WebsiteSetting.objects.first()
    
    context = {
        'quick_link': quick_link,
        'setting': setting,
    }
    return render(request, 'businessprofile/quick_link_detail.html', context)


def legal_link_detail(request, slug):
    """Display detail page for a legal link"""
    legal_link = get_object_or_404(LegalLink, slug=slug, is_active=True)
    setting = WebsiteSetting.objects.first()
    
    context = {
        'legal_link': legal_link,
        'setting': setting,
    }
    return render(request, 'businessprofile/legal_link_detail.html', context)

