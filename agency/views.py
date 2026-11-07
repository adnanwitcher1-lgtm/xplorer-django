import os

from django.contrib import messages
from django.http import FileResponse, HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from . import mailer, pdfgen
from .models import (
    FAQ,
    BlogPost,
    CapabilityBar,
    ClientLogo,
    ClientReview,
    ContactMessage,
    CoreValue,
    GuidelineSlide,
    Industry,
    NewsletterSubscriber,
    ProcessStep,
    Project,
    Service,
    SiteSettings,
    Stat,
    TeamMember,
    Testimonial,
    TrustBadge,
)


def home(request):
    slider = Testimonial.objects.filter(show_on_home_slider=True)
    testimonial_data = [
        {
            "quote": t.quote,
            "name": t.name,
            "role": t.role,
            "avatar": t.avatar.url if t.avatar else "",
            "rating": max(1, min(t.rating, 5)),
        }
        for t in slider
    ]
    return render(request, "agency/home.html", {
        "testimonial_data": testimonial_data,
        "active": "home",
        "stats": Stat.objects.all(),
        "bars": CapabilityBar.objects.all(),
        "services": Service.objects.filter(show_on_home=True),
        "steps": ProcessStep.objects.all(),
        "projects": Project.objects.filter(is_featured=True),
        "testimonials": slider,
        "faqs": FAQ.objects.all(),
        "guideline_slides": GuidelineSlide.objects.filter(is_active=True),
        "badges": TrustBadge.objects.all(),
        "industries": Industry.objects.all(),
        "client_logos": ClientLogo.objects.all(),
        "reviews": ClientReview.objects.filter(is_published=True),
        "core_values": CoreValue.objects.all(),
    })


def services(request):
    return render(request, "agency/services.html", {
        "active": "services",
        "services": Service.objects.filter(show_on_services_page=True),
    })


def service_detail(request, pk, slug):
    service = get_object_or_404(Service, pk=pk)
    if slug != service.url_slug:
        return redirect(service.get_absolute_url(), permanent=True)
    return render(request, "agency/service_detail.html", {
        "active": "services",
        "service": service,
        "features": service.detail_features.all(),
        "steps": service.detail_steps.all(),
        "faqs": service.detail_faqs.all(),
        "related": Service.objects.filter(show_on_services_page=True).exclude(pk=service.pk)[:3],
    })


def service_guide(request, pk, slug):
    service = get_object_or_404(Service, pk=pk)
    if slug != service.url_slug:
        url = service.get_guide_url()
        if request.GET:
            url += "?" + request.GET.urlencode()
        return redirect(url, permanent=True)
    return render(request, "agency/service_guide.html", {
        "active": "services",
        "service": service,
        "features": service.detail_features.all(),
        "steps": service.detail_steps.all(),
        "faqs": service.detail_faqs.all(),
        "outcomes": service.outcomes.all(),
        "auto_download": request.GET.get("download") == "1",
    })


def service_brochure(request, pk, slug):
    """Download the uploaded brochure, or a PDF generated from the service details."""
    service = get_object_or_404(Service, pk=pk)
    if service.brochure:
        try:
            ext = os.path.splitext(service.brochure.name)[1] or ".pdf"
            return FileResponse(service.brochure.open("rb"), as_attachment=True,
                                filename=f"{service.url_slug}-brochure{ext}")
        except (FileNotFoundError, ValueError):
            pass  # uploaded file went missing: fall back to the generated one
    pdf = pdfgen.build_service_pdf(service, SiteSettings.load())
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{service.url_slug}-brochure.pdf"'
    return response


def portfolio(request):
    return render(request, "agency/portfolio.html", {
        "active": "portfolio",
        "projects": Project.objects.all(),
    })


def project_detail(request, pk, slug):
    project = get_object_or_404(Project, pk=pk)
    if slug != project.url_slug:
        return redirect(project.get_absolute_url(), permanent=True)
    ordered = list(Project.objects.all())
    idx = next((i for i, p in enumerate(ordered) if p.pk == project.pk), 0)
    prev_project = next_project = None
    if len(ordered) > 1:
        prev_project = ordered[idx - 1]
        next_project = ordered[(idx + 1) % len(ordered)]
    return render(request, "agency/project_detail.html", {
        "active": "portfolio",
        "project": project,
        "results": project.results.all(),
        "gallery": project.gallery.all(),
        "prev_project": prev_project,
        "next_project": next_project,
    })


def about(request):
    return render(request, "agency/about.html", {
        "active": "about",
        "team": TeamMember.objects.filter(show_on_about=True),
    })


def testimonials(request):
    return render(request, "agency/testimonials.html", {
        "active": "testimonials",
        "testimonials": Testimonial.objects.all(),
    })


def blog_list(request):
    return render(request, "agency/blog.html", {
        "active": "blog",
        "posts": BlogPost.objects.filter(is_published=True),
    })


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, "agency/blog_detail.html", {"active": "blog", "post": post})


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()
        try:
            validate_email(email)
            valid = bool(name and message)
        except ValidationError:
            valid = False
        if valid:
            cm = ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
            mailer.on_new_message(cm)
            messages.success(
                request,
                "Message Received!|Thank you for reaching out to Xplorer Solution. "
                "Our architectural team will review your inquiry and get back to you shortly.",
            )
        else:
            messages.error(request, "Oops!|Please fill in your name, a valid email and a message.")
        return redirect("contact")
    return render(request, "agency/contact.html", {"active": "contact"})


@require_POST
def subscribe(request):
    email = request.POST.get("email", "").strip()
    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "Oops!|Please enter a valid email address.")
    else:
        _, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if created:
            messages.success(request, "Subscribed!|You have successfully subscribed to the Xplorer Tech Insights newsletter.")
        else:
            messages.info(request, "Already Subscribed|This email is already on our newsletter list.")
    return redirect(request.META.get("HTTP_REFERER") or "home")


def search(request):
    q = request.GET.get("q", "").strip()
    results = {"services": [], "projects": [], "posts": []}
    if q:
        results["services"] = Service.objects.filter(
            Q(title__icontains=q) | Q(short_description__icontains=q) | Q(full_description__icontains=q)
        )
        results["projects"] = Project.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))
        results["posts"] = BlogPost.objects.filter(is_published=True).filter(
            Q(title__icontains=q) | Q(excerpt__icontains=q) | Q(content__icontains=q)
        )
    total = sum(len(v) for v in results.values())
    return render(request, "agency/search.html", {"q": q, "results": results, "total": total})
