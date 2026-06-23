from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('post.urls')),
    path('register/', include('userAcc.urls')),
    path('profile/', include('userProfile.urls')),
    path('login/', auth_views.LoginView.as_view(
        template_name='userAcc/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),
         name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


# http://localhost:8000/главныйurls/urlsприложения
# http://localhost:8000/blog/posts/