from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("services/<int:pk>/<slug:slug>/", views.service_detail, name="service_detail"),
    path("services/<int:pk>/<slug:slug>/guide/", views.service_guide, name="service_guide"),
    path("services/<int:pk>/<slug:slug>/brochure/", views.service_brochure, name="service_brochure"),
    path("projects/", views.portfolio, name="portfolio"),
    path("projects/<int:pk>/<slug:slug>/", views.project_detail, name="project_detail"),
    path("portfolio/", RedirectView.as_view(pattern_name="portfolio", permanent=True)),
    path("about/", views.about, name="about"),
    path("testimonials/", views.testimonials, name="testimonials"),
    path("blog/", views.blog_list, name="blog"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("contact/", views.contact, name="contact"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("search/", views.search, name="search"),
]
