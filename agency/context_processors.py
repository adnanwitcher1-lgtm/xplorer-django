from .models import SiteSettings


def site_context(request):
    return {
        "site": SiteSettings.load(),
        "nav_items": [
            ("home", "Home", "/"),
            ("services", "Services", "/services/"),
            ("portfolio", "Projects", "/projects/"),
            ("about", "About Us", "/about/"),
            ("testimonials", "Testimonials", "/testimonials/"),
            ("blog", "Blog", "/blog/"),
            ("contact", "Contact", "/contact/"),
        ],
    }
