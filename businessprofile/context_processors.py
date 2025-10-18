from .models import WebsiteSetting

def website_settings(request):
    setting = WebsiteSetting.objects.first()
    return {'setting': setting}
