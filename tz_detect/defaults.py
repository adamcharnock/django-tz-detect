from django.conf import settings

# These countries will be prioritised in the search
# for a matching timezone. Consider putting your
# app's most popular countries first.
# Defaults to top Internet using countries.
TZ_DETECT_COUNTRIES = getattr(settings, 'TZ_DETECT_COUNTRIES', ('CN', 'US', 'IN', 'JP', 'BR', 'RU', 'DE', 'FR', 'GB'))

# Should the page reload upon determination of the 
# user's timezone. This allows your app to have the 
# user's timezone available for the first page view.
TZ_RELOAD = getattr(settings, 'TZ_RELOAD', False)

# The default URL the user should be redirected to 
# once their timezone has been stored. This only 
# applies if TZ_RELOAD=True
TZ_DEFAULT_RELOAD_URL = getattr(settings, 'TZ_DEFAULT_RELOAD_URL', '/')