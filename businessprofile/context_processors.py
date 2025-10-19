from .models import QuickLink, WebsiteSetting, LegalLink

def website_settings(request):
    setting = WebsiteSetting.objects.first()
    return {'setting': setting}

def footer_quick_links(request):
    quick_links = QuickLink.objects.filter(is_active=True)
    return {'footerQuickLinks': quick_links}

def footer_legal_links(request):
    legal_links = LegalLink.objects.filter(is_active=True)
    return {'footerLegalLinks': legal_links}

