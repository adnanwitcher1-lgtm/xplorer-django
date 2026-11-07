from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class SiteSettings(models.Model):
    """Single record that controls all global text of the website."""

    # Branding
    site_name = models.CharField(max_length=60, default="XPLORER")
    site_suffix = models.CharField("Name suffix", max_length=40, default="Solution")
    meta_title = models.CharField(
        max_length=200,
        default="Xplorer Solution | Human-Centric Digital Architecture & Tech Solutions",
    )

    # Hero
    hero_badge = models.CharField(max_length=80, default="Humanizing Digital Architecture")
    hero_title_prefix = models.CharField(max_length=120, default="Empowering Visionaries With")
    hero_title_highlight = models.CharField(max_length=120, default="Human-Centric Digital Solutions")
    hero_description = models.TextField(
        default="At Xplorer Solution, we fuse sleek design, robust engineering, and intuitive user "
        "experiences to turn bold concepts into scalable digital powerhouses."
    )

    # Who we are (home)
    who_badge = models.CharField(max_length=60, default="Who We Are")
    who_title = models.CharField(max_length=160, default="Crafting Tech Infrastructure With a")
    who_title_highlight = models.CharField(max_length=80, default="Human Touch")
    who_text = models.TextField(
        default="Software shouldn't feel rigid or robotic to the human user. At Xplorer Solution, we "
        "bridge complex technological capabilities with warm, intuitive design aesthetics."
    )
    mission = models.TextField(default="To empower enterprises and fast-growing startups with tailored software architectures that simplify user journeys and accelerate real-world commercial growth.")
    vision = models.TextField(default="To set the modern global benchmark where advanced engineering precision harmonizes effortlessly with human empathy and intuitive digital design.")
    core_values = models.TextField(default="Continuous Innovation, Transparent Collaboration, Agile Speed, and Uncompromising Quality across every pixel and line of code.")
    capability_title = models.CharField(max_length=60, default="TECH_CAPABILITY_MATRIX")
    capability_version = models.CharField(max_length=30, default="V3.8 Active")
    capability_note = models.CharField(
        max_length=200,
        default="Enterprise-grade encryption with ISO 27001 certified development workflows.",
    )

    # Section headings
    services_heading = models.CharField(max_length=160, default="Architectural Excellence for Every Screen")
    services_subheading = models.CharField(max_length=200, default="Comprehensive tech capabilities built to scale your business cleanly and effectively.")
    process_heading = models.CharField(max_length=160, default="Our Precision Delivery Blueprint")
    process_subheading = models.CharField(max_length=200, default="A transparent 4-stage ecosystem designed for predictability and rapid execution.")

    # Estimator
    estimator_cost_per_screen = models.PositiveIntegerField(default=400, help_text="USD per screen/module")
    estimator_cost_per_design_level = models.PositiveIntegerField(default=2000, help_text="USD multiplied by design level (1-3)")
    estimator_mobile_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1.20)
    estimator_full_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1.70)

    # Trust strip (rating + badges)
    rating_value = models.CharField(max_length=6, default="4.9")
    rating_text = models.CharField(max_length=120, default="Average rating from 100+ verified client reviews")

    # Industries
    industries_badge = models.CharField(max_length=60, default="Industries We Work With")
    industries_heading = models.CharField(max_length=160, default="Expertise Across Key Industries")
    industries_text = models.CharField(max_length=300, default="We bring domain knowledge to every build, so your product speaks your market's language from day one.")

    # Clients
    clients_heading = models.CharField(max_length=120, default="Our Clients")
    clients_text = models.CharField(max_length=300, default="Trusted by forward-looking companies, startups and growing businesses.")

    # Reviews
    reviews_heading = models.CharField(max_length=160, default="Real Client Reviews")
    reviews_summary = models.CharField(max_length=120, default="Rated 5.0 based on 50 reviews")

    # Core values
    values_badge = models.CharField(max_length=60, default="Why Xplorer")
    values_heading = models.CharField(max_length=160, default="The Thinking Behind Better Growth")
    values_image = models.ImageField("Core values image", upload_to="values/", blank=True, null=True)
    process_button = models.CharField(max_length=60, default="Talk To Our Experts")

    # Free consultation form (home page)
    consult_heading = models.CharField(max_length=160, default="Get Free Consultation")
    consult_text = models.CharField(max_length=300, default="Have questions? Drop us a message and our specialists will respond promptly.")

    # Guidelines slider (Who We Are)
    guidelines_badge = models.CharField(max_length=60, default="Software Management Guidelines")
    guidelines_heading = models.CharField(max_length=160, default="How We Run Every Project")
    guidelines_text = models.CharField(max_length=300, default="Clear, repeatable practices that keep software delivery predictable from the first sprint to the final release.")

    # CTA banner
    cta_title = models.CharField(max_length=160, default="Ready to Engineer Your Breakthrough?")
    cta_text = models.CharField(max_length=250, default="Let's craft an unprecedented digital experience that sets your brand apart in modern markets.")
    cta_button = models.CharField(max_length=60, default="Get Started Today")

    # Contact
    contact_heading = models.CharField(max_length=160, default="Start Your Digital Evolution")
    contact_text = models.CharField(max_length=300, default="Have a project in mind or need expert technical advice? Drop us a message and our lead architects will respond within 24 hours.")
    email = models.EmailField(default="contact@xplorersolution.com")
    phone = models.CharField(max_length=40, default="+1 (800) 459-7567")
    address = models.CharField(max_length=200, default="Tech Tower, Floor 14, Silicon Plaza")

    # WhatsApp
    whatsapp_enabled = models.BooleanField("Show WhatsApp button", default=True)
    whatsapp_number = models.CharField("WhatsApp number", max_length=25, default="+1 800 459 7567", help_text="With country code, e.g. +92 300 1234567")
    whatsapp_message = models.CharField("Pre-filled message", max_length=200, default="Hello Xplorer Solution, I would like to discuss a project.")

    # Email (outgoing mail settings + notifications)
    email_enabled = models.BooleanField("Send emails through the SMTP settings below", default=False,
        help_text="Off = emails are only printed in the server console (safe for testing).")
    email_host = models.CharField("SMTP host", max_length=120, blank=True, default="smtp.gmail.com")
    email_port = models.PositiveIntegerField("SMTP port", default=587)
    email_use_tls = models.BooleanField("Use TLS (port 587)", default=True)
    email_use_ssl = models.BooleanField("Use SSL (port 465)", default=False)
    email_host_user = models.CharField("SMTP username / email", max_length=160, blank=True)
    email_host_password = models.CharField("SMTP password / app password", max_length=160, blank=True,
        help_text="For Gmail create an App Password (Google Account > Security > 2-Step Verification > App passwords).")
    email_from_name = models.CharField("Sender name", max_length=80, default="Xplorer Solution")
    notify_email = models.EmailField("Receive new-message alerts at", blank=True, help_text="Leave empty to use the Contact email above.")
    send_notification = models.BooleanField("Email me when a message arrives", default=True)
    send_auto_reply = models.BooleanField("Send an automatic thank-you email to the visitor", default=True)
    auto_reply_subject = models.CharField(max_length=160, default="We received your message")
    auto_reply_body = models.TextField(default="Hi {name},\n\nThank you for contacting us. Our team has received your message and will reply within 24 hours.\n\nBest regards,\nXplorer Solution")

    # About page
    about_heading = models.CharField(max_length=160, default="Humanizing Tech Solutions")
    about_intro = models.CharField(max_length=300, default="Founded on the principle that software should elevate human potential rather than complicate it.")
    about_subheading = models.CharField(max_length=160, default="Empowerment Through Human-Centered Code")
    about_paragraph_1 = models.TextField(default="Xplorer Solution began as a collective of passionate software architects, UI designers, and systems engineers determined to rethink how corporate digital products are built.")
    about_paragraph_2 = models.TextField(default="By combining clean purple-black aesthetic elegance with rock-solid server backends, we make technology feel warm, accessible, and extraordinarily effective.")
    about_image = models.ImageField(
        "About page team photo", upload_to="about/", blank=True, null=True,
        help_text="Main team picture shown beside the About text. Best size: 1200x800 (landscape).",
    )
    team_heading = models.CharField(max_length=120, default="Meet Our Team")
    team_subheading = models.CharField(max_length=250, default="The people behind every pixel and line of code.")

    # Footer / social
    footer_text = models.TextField(default="Humanized digital architecture, mobile applications, and cloud infrastructures engineered for visionary modern brands globally.")
    copyright_text = models.CharField(max_length=120, default="Xplorer Solution. All rights reserved.")
    facebook_url = models.URLField(blank=True, default="#")
    linkedin_url = models.URLField(blank=True, default="#")
    instagram_url = models.URLField(blank=True, default="#")
    github_url = models.URLField(blank=True, default="#")
    youtube_url  = models.URLField(blank=True, default="#")
    privacy_text = models.TextField(default="We value your privacy. All user interaction logs are kept encrypted strictly under modern GDPR standards.")
    terms_text = models.TextField(default="Terms governing software deployment, intellectual property ownership, and client confidentiality.")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @property
    def whatsapp_url(self):
        from urllib.parse import quote
        digits = "".join(ch for ch in (self.whatsapp_number or "") if ch.isdigit())
        if not digits:
            return ""
        url = f"https://wa.me/{digits}"
        if self.whatsapp_message:
            url += "?text=" + quote(self.whatsapp_message)
        return url

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Stat(models.Model):
    value = models.CharField(max_length=20, help_text="e.g. 250+")
    label = models.CharField(max_length=80)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Hero Statistic"

    def __str__(self):
        return f"{self.value} {self.label}"


class CapabilityBar(models.Model):
    label = models.CharField(max_length=80)
    percent = models.PositiveSmallIntegerField(default=90)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Capability Bar"

    def __str__(self):
        return f"{self.label} ({self.percent}%)"


class Service(models.Model):
    title = models.CharField(max_length=120)
    short_description = models.TextField(help_text="Shown on the home page card")
    full_title = models.CharField(max_length=160, blank=True, help_text="Title on the Services page (optional)")
    full_description = models.TextField(blank=True, help_text="Shown on the Services page")
    features = models.TextField(blank=True, help_text="One feature per line")
    icon = models.CharField(max_length=60, default="fa-solid fa-code", help_text="FontAwesome class, e.g. fa-solid fa-code")
    show_on_home = models.BooleanField(default=True)
    show_on_services_page = models.BooleanField(default=True)

    # Detail page (opens from the "View More" button)
    tagline = models.CharField(max_length=200, blank=True, help_text="One-line headline at the top of the detail page")
    overview = models.TextField(blank=True, help_text="Main text of the detail page. A blank line starts a new paragraph.")
    detail_image = models.ImageField(upload_to="services/", blank=True, null=True, help_text="Image beside the overview (900x600 works well).")
    technologies = models.TextField(blank=True, help_text="Comma separated, e.g. Django, React, PostgreSQL")
    detail_cta = models.CharField("Detail page button text", max_length=60, default="Start This Project")

    # Brochure download + Complete Guide page (outline button on the service card)
    brochure = models.FileField(upload_to="brochures/", blank=True, null=True,
                                help_text="Optional PDF for the 'Brochure' button. Leave empty and a PDF is generated automatically from the details of this service.")
    guide_intro = models.TextField(blank=True, help_text="Long introduction on the Complete Guide page. A blank line starts a new paragraph.")
    ideal_for = models.TextField(blank=True, help_text="One line per item: who this service is for")
    deliverables = models.TextField(blank=True, help_text="One line per item: what the client receives")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @property
    def feature_list(self):
        return [f.strip() for f in self.features.splitlines() if f.strip()]

    @property
    def tech_list(self):
        return [t.strip() for t in self.technologies.replace("\n", ",").split(",") if t.strip()]

    @property
    def overview_paragraphs(self):
        return [p.strip() for p in self.overview.split("\n\n") if p.strip()]

    @property
    def url_slug(self):
        return slugify(self.title) or "service"

    @property
    def guide_paragraphs(self):
        text = self.guide_intro or self.overview or self.full_description or self.short_description
        return [p.strip() for p in text.split("\n\n") if p.strip()]

    @property
    def ideal_for_list(self):
        return [x.strip() for x in self.ideal_for.splitlines() if x.strip()]

    @property
    def deliverable_list(self):
        return [x.strip() for x in self.deliverables.splitlines() if x.strip()]

    def get_absolute_url(self):
        return reverse("service_detail", args=[self.pk, self.url_slug])

    def get_guide_url(self):
        return reverse("service_guide", args=[self.pk, self.url_slug])

    def get_download_url(self):
        return reverse("service_brochure", args=[self.pk, self.url_slug])


class ServiceFeature(models.Model):
    service = models.ForeignKey(Service, related_name="detail_features", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    icon = models.CharField(max_length=60, default="fa-solid fa-circle-check", help_text="FontAwesome class")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "What's included (feature)"
        verbose_name_plural = "What's included (features)"

    def __str__(self):
        return self.title


class ServiceStep(models.Model):
    service = models.ForeignKey(Service, related_name="detail_steps", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Delivery step"
        verbose_name_plural = "Delivery steps"

    def __str__(self):
        return self.title


class ServiceOutcome(models.Model):
    service = models.ForeignKey(Service, related_name="outcomes", on_delete=models.CASCADE)
    value = models.CharField(max_length=20, help_text="e.g. 40%, 3x, 120+")
    label = models.CharField(max_length=100, help_text="e.g. Faster page loads")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Expected result"
        verbose_name_plural = "Expected results"

    def __str__(self):
        return f"{self.value} {self.label}"


class ServiceFAQ(models.Model):
    service = models.ForeignKey(Service, related_name="detail_faqs", on_delete=models.CASCADE)
    question = models.CharField(max_length=250)
    answer = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Service FAQ"
        verbose_name_plural = "Service FAQs"

    def __str__(self):
        return self.question


class GuidelineSlide(models.Model):
    """Slides of the carousel in the 'Who We Are' section (Software Management Guidelines)."""

    title = models.CharField(max_length=120)
    badge = models.CharField(max_length=40, default="GUIDELINE", help_text="Small mono label, e.g. SPRINT_FLOW")
    summary = models.CharField(max_length=250, blank=True, help_text="Short sentence under the title")
    image = models.ImageField(upload_to="guidelines/", blank=True, null=True, help_text="Shown on the right side of the slide (900x700 works well).")
    icon = models.CharField(max_length=60, default="fa-solid fa-list-check", help_text="FontAwesome class")
    points = models.TextField(help_text="One guideline point per line")
    note = models.CharField(max_length=250, blank=True, help_text="Optional tip shown in the box at the bottom")
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Guideline slide"
        verbose_name_plural = "Guideline slides"

    def __str__(self):
        return self.title

    @property
    def point_list(self):
        return [p.strip() for p in self.points.splitlines() if p.strip()]


class ProcessStep(models.Model):
    number = models.CharField(max_length=4, default="01")
    title = models.CharField(max_length=100)
    description = models.TextField()
    deliverable = models.CharField(max_length=200, blank=True, help_text="Shown in bold under the step, e.g. 'Approved roadmap'")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.number} - {self.title}"


class Project(models.Model):
    CATEGORY_CHOICES = [("web", "Web"), ("mobile", "Mobile"), ("saas", "SaaS")]

    title = models.CharField(max_length=120)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="web")
    badge = models.CharField(max_length=40, help_text="Small label on image, e.g. SaaS Enterprise")
    description = models.TextField()
    details = models.TextField(blank=True, help_text="Overview text of the case-study page. A blank line starts a new paragraph.")
    image = models.ImageField(upload_to="projects/", blank=True, null=True, help_text="Card image and the big cover of the case-study page.")
    is_featured = models.BooleanField(default=True, help_text="Show on the home page")

    # Case-study page ("View Case Details")
    client = models.CharField(max_length=100, blank=True)
    year = models.CharField(max_length=10, blank=True)
    duration = models.CharField(max_length=40, blank=True, help_text="e.g. 12 weeks")
    role = models.CharField("Our role / services", max_length=160, blank=True, help_text="e.g. Design, Development, Cloud")
    live_url = models.URLField("Live website / app link", blank=True)
    challenge = models.TextField(blank=True, help_text="What problem did the client have?")
    solution = models.TextField(blank=True, help_text="How did we solve it?")
    technologies = models.TextField(blank=True, help_text="Comma separated, e.g. Django, React, AWS")
    techniques = models.TextField(blank=True, help_text="One per line. Write 'Name: short explanation' to show a title and a sentence.")
    key_features = models.TextField(blank=True, help_text="One feature per line")
    quote = models.TextField("Client quote", blank=True)
    quote_author = models.CharField("Quote author", max_length=120, blank=True, help_text="e.g. Sarah Jenkins, CTO at Nexus Fintech")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @property
    def url_slug(self):
        return slugify(self.title) or "project"

    def get_absolute_url(self):
        return reverse("project_detail", args=[self.pk, self.url_slug])

    @property
    def overview_paragraphs(self):
        return [p.strip() for p in (self.details or self.description).split("\n\n") if p.strip()]

    @property
    def challenge_paragraphs(self):
        return [p.strip() for p in self.challenge.split("\n\n") if p.strip()]

    @property
    def solution_paragraphs(self):
        return [p.strip() for p in self.solution.split("\n\n") if p.strip()]

    @property
    def tech_list(self):
        return [t.strip() for t in self.technologies.replace("\n", ",").split(",") if t.strip()]

    @property
    def feature_list(self):
        return [f.strip() for f in self.key_features.splitlines() if f.strip()]

    @property
    def technique_list(self):
        items = []
        for line in self.techniques.splitlines():
            line = line.strip()
            if not line:
                continue
            name, sep, text = line.partition(":")
            items.append((name.strip(), text.strip()) if sep else (line, ""))
        return items


class ProjectResult(models.Model):
    project = models.ForeignKey(Project, related_name="results", on_delete=models.CASCADE)
    value = models.CharField(max_length=20, help_text="e.g. 42%, 3x, 1.2M+")
    label = models.CharField(max_length=100, help_text="e.g. Higher checkout conversion")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Project result"
        verbose_name_plural = "Project results"

    def __str__(self):
        return f"{self.value} {self.label}"


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name="gallery", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=150, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Gallery image"
        verbose_name_plural = "Gallery images"

    def __str__(self):
        return self.caption or f"Image {self.pk}"


class Testimonial(models.Model):
    name = models.CharField(max_length=80)
    role = models.CharField(max_length=120)
    quote = models.TextField()
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=5)
    show_on_home_slider = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.name} - {self.role}"


class TrustBadge(models.Model):
    name = models.CharField(max_length=60, help_text="e.g. Top Rated")
    subtitle = models.CharField(max_length=80, blank=True, help_text="e.g. 4.9 / 5 Rating")
    icon = models.CharField(max_length=60, default="fa-solid fa-award", help_text="FontAwesome class")
    url = models.URLField(blank=True, help_text="Optional link (your real profile page)")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to="industries/", blank=True, null=True, help_text="Square image works best (400x400).")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "Industries"

    def __str__(self):
        return self.name


class ClientLogo(models.Model):
    name = models.CharField(max_length=80)
    logo = models.ImageField(upload_to="clients/", blank=True, null=True, help_text="Transparent PNG/SVG-like image, wide format.")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class ClientReview(models.Model):
    name = models.CharField(max_length=80)
    date_text = models.CharField(max_length=40, blank=True, help_text="e.g. September 2026")
    rating = models.PositiveSmallIntegerField(default=5)
    text = models.TextField()
    source = models.CharField(max_length=60, blank=True, default="Verified client")
    avatar = models.ImageField(upload_to="reviews/", blank=True, null=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.name} ({self.rating}*)"


class CoreValue(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=80)
    role = models.CharField(max_length=120)
    photo = models.ImageField(upload_to="team/", blank=True, null=True, help_text="Square photo works best (600x600).")
    bio = models.CharField(max_length=250, blank=True)
    linkedin_url = models.URLField(blank=True)
    show_on_about = models.BooleanField("Show on About page", default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.name} - {self.role}"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=60)
    excerpt = models.TextField()
    content = models.TextField(blank=True, help_text="Full article (blank lines make paragraphs)")
    image = models.ImageField(upload_to="blog/", blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "post"
            slug, n = base, 2
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def paragraphs(self):
        return [p.strip() for p in self.content.split("\n\n") if p.strip()]


class FAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    email_status = models.CharField("Email status", max_length=200, blank=True)
    reply = models.TextField("Your reply", blank=True, help_text="Write your answer, save, then use the action 'Send reply by email'.")
    replied_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-subscribed_at"]

    def __str__(self):
        return self.email
