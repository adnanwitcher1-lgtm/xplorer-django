"""Fill the database with dummy content (same as the original HTML design).

Usage:
    python manage.py seed_data            # add data (only if tables are empty)
    python manage.py seed_data --reset    # wipe content tables and re-seed
"""
import io

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont

from agency.models import (
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
    ProjectImage,
    ProjectResult,
    Service,
    ServiceOutcome,
    ServiceFAQ,
    ServiceFeature,
    ServiceStep,
    SiteSettings,
    Stat,
    TeamMember,
    Testimonial,
    TrustBadge,
)


def _font(size):
    for name in ("DejaVuSans-Bold.ttf", "arialbd.ttf", "Arial Bold.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def banner(text, c1, c2, size=(600, 400), fg="#ffffff"):
    """Diagonal gradient banner with centered text."""
    w, h = size
    img = Image.new("RGB", size)
    a, b = _hex(c1), _hex(c2)
    px = img.load()
    for y in range(h):
        for x in range(w):
            t = (x / w + y / h) / 2
            px[x, y] = tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
    d = ImageDraw.Draw(img)
    # decorative translucent circles
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((w * 0.6, -h * 0.3, w * 1.2, h * 0.5), fill=(255, 255, 255, 30))
    od.ellipse((-w * 0.2, h * 0.6, w * 0.3, h * 1.3), fill=(255, 255, 255, 25))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img)
    font = _font(max(18, w // 16))
    words, lines, line = text.split(), [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if d.textlength(trial, font=font) > w * 0.8 and line:
            lines.append(line)
            line = word
        else:
            line = trial
    lines.append(line)
    lh = font.size + 10 if hasattr(font, "size") else 30
    y = (h - lh * len(lines)) / 2
    for ln in lines:
        tw = d.textlength(ln, font=font)
        d.text(((w - tw) / 2, y), ln, fill=fg, font=font)
        y += lh
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return ContentFile(buf.getvalue())


def avatar(initial, color):
    size = (200, 200)
    img = Image.new("RGB", size, _hex(color))
    d = ImageDraw.Draw(img)
    font = _font(90)
    tw = d.textlength(initial, font=font)
    d.text(((200 - tw) / 2, 50), initial, fill="#ffffff", font=font)
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return ContentFile(buf.getvalue())


def logo(text, color):
    """Transparent wordmark-style placeholder logo."""
    font = _font(34)
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    tw = int(probe.textlength(text, font=font))
    img = Image.new("RGBA", (tw + 70, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 12, 40, 52), radius=10, fill=_hex(color))
    d.text((12, 16), text[0], fill="#ffffff", font=_font(26))
    d.text((52, 14), text, fill=_hex(color), font=font)
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return ContentFile(buf.getvalue())


class Command(BaseCommand):
    help = "Seed the database with dummy website content and an admin user."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete existing content first")

    def handle(self, *args, **opts):
        if opts["reset"]:
            for m in (Stat, CapabilityBar, Service, ProcessStep, Project, Testimonial,
                      TeamMember, TrustBadge, Industry, ClientLogo, ClientReview, CoreValue, GuidelineSlide,
                      BlogPost, FAQ, ContactMessage, NewsletterSubscriber):
                m.objects.all().delete()
            SiteSettings.objects.all().delete()

        site = SiteSettings.load()
        if not site.about_image:
            site.about_image.save("team.png", banner("Xplorer Team Culture", "#8b5cf6", "#4c1d95"), save=False)
            site.save()
        if not site.values_image:
            site.values_image.save("values.png", banner("Global Growth Partner", "#6d28d9", "#a78bfa", size=(800, 600)), save=False)
            site.save()

        if not Stat.objects.exists():
            for i, (v, l) in enumerate([
                ("250+", "Global Projects Delivered"),
                ("99.8%", "Client Satisfaction Rate"),
                ("15+", "International Design Awards"),
                ("12M+", "End-Users Impacted"),
            ]):
                Stat.objects.create(value=v, label=l, order=i)

        if not TeamMember.objects.exists():
            for i, (n, r, b, col) in enumerate([
                ("Ayesha Khan", "Founder & CEO", "Leads product vision and client strategy.", "#7c3aed"),
                ("Bilal Ahmed", "Lead Software Architect", "Designs scalable backends and cloud systems.", "#4c1d95"),
                ("Sara Malik", "Head of UI/UX Design", "Crafts humanized, accessible interfaces.", "#8b5cf6"),
                ("Usman Raza", "DevOps Engineer", "Keeps releases fast and uptime high.", "#6d28d9"),
            ]):
                m = TeamMember(name=n, role=r, bio=b, order=i)
                m.photo.save(f"team-{i + 1}.png", avatar(n[0], col), save=False)
                m.save()

        deliverables = {
            "01": "Technical brief and audit scope",
            "02": "Approved roadmap",
            "03": "Staged rollouts with review cycles",
            "04": "Monthly reports and quarterly pivots",
        }
        for step in ProcessStep.objects.filter(deliverable=""):
            if step.number in deliverables:
                step.deliverable = deliverables[step.number]
                step.save()

        if not TrustBadge.objects.exists():
            for i, (n, sub, icon) in enumerate([
                ("Top Rated", "4.9 / 5 Client Score", "fa-solid fa-star"),
                ("Verified Reviews", "100+ Happy Clients", "fa-solid fa-circle-check"),
                ("Quality Assured", "ISO-aligned Workflow", "fa-solid fa-shield-halved"),
                ("Trusted Partner", "10+ Years Experience", "fa-solid fa-handshake"),
            ]):
                TrustBadge.objects.create(name=n, subtitle=sub, icon=icon, order=i)

        if not Industry.objects.exists():
            for i, (n, c1, c2) in enumerate([
                ("Fashion", "#7c3aed", "#c4b5fd"), ("Food", "#6d28d9", "#a78bfa"),
                ("Retail", "#4c1d95", "#8b5cf6"), ("Technology", "#1e1b4b", "#7c3aed"),
                ("Startups", "#5b21b6", "#a78bfa"), ("Healthcare", "#4c1d95", "#c4b5fd"),
                ("Hospitality", "#6d28d9", "#ddd6fe"), ("Education", "#311042", "#8b5cf6"),
            ]):
                ind = Industry(name=n, order=i)
                ind.image.save(f"industry-{i + 1}.png", banner(n, c1, c2, size=(400, 400)), save=False)
                ind.save()

        if not ClientLogo.objects.exists():
            for i, (n, col) in enumerate([
                ("Nexus Labs", "#6d28d9"), ("BioPulse", "#4c1d95"), ("Zenith Co", "#7c3aed"),
                ("CloudScale", "#5b21b6"), ("HealthDirect", "#4338ca"), ("Aura Retail", "#8b5cf6"),
                ("Apex Supply", "#4c1d95"), ("Krypton Pay", "#6d28d9"),
            ]):
                cl = ClientLogo(name=n, order=i)
                cl.logo.save(f"client-{i + 1}.png", logo(n, col), save=False)
                cl.save()

        if not ClientReview.objects.exists():
            for i, (n, d, t, col) in enumerate([
                ("Hamza Ali", "September 2026", "Delivered our platform ahead of schedule. Communication was clear and the final result looks fantastic.", "#7c3aed"),
                ("Noor Fatima", "August 2026", "Very professional team. They listened carefully and turned our rough idea into a polished product.", "#4c1d95"),
                ("Daniel Brooks", "August 2026", "Great experience from kickoff to launch. Fast responses and genuinely high quality work.", "#8b5cf6"),
                ("Maria Santos", "July 2026", "Our conversion rate improved noticeably after the redesign. Highly recommended.", "#6d28d9"),
            ]):
                r = ClientReview(name=n, date_text=d, text=t, rating=5, order=i)
                r.avatar.save(f"review-{i + 1}.png", avatar(n[0], col), save=False)
                r.save()

        if not CoreValue.objects.exists():
            for i, (t, d) in enumerate([
                ("Radical Transparency", "Clear scope and pricing from day one, so there are no surprises later."),
                ("Verifiable Authority", "Real projects, real results, and references you can check yourself."),
                ("Direct Specialist Access", "Talk straight to the engineers and designers doing your work."),
                ("90%+ Client Retention", "Most of our clients stay with us because the results keep compounding."),
            ]):
                CoreValue.objects.create(title=t, description=d, order=i)

        if not CapabilityBar.objects.exists():
            for i, (l, p) in enumerate([
                ("Humanized UI/UX Precision", 98),
                ("Cloud Scalability & Resilience", 95),
                ("Real-time Data Processing", 99),
            ]):
                CapabilityBar.objects.create(label=l, percent=p, order=i)

        if not Service.objects.exists():
            services = [
                ("Custom Web Architecture", "fa-solid fa-code",
                 "High-performance Single Page Applications, SaaS portals, and responsive websites optimized for lightning speed and SEO superiority.",
                 "Custom Web Platform Architecture",
                 "We build modern enterprise web applications designed for infinite scalability, high traffic concurrency, and intuitive content administration.",
                 "Single Page Applications (SPA) & Progressive Web Apps (PWA)\nHeadless CMS & Microservices Integrations\nUltra-low latency API Gateway engineering"),
                ("Mobile App Engineering", "fa-solid fa-mobile-screen-button",
                 "Native and cross-platform iOS/Android mobile apps engineered for seamless performance, fluid gestures, and offline-first functionality.",
                 "Native & Cross-Platform Mobile Apps",
                 "Delivering fluid, feature-rich iOS and Android mobile experiences that leverage native hardware acceleration and seamless biometrics.",
                 "Flutter & React Native high-speed builds\nOffline data syncing algorithms\nApp Store & Play Store publishing compliance"),
                ("UI/UX Humanized Design", "fa-solid fa-wand-magic-sparkles",
                 "Design systems, interactive wireframes, and intuitive user interfaces built on deep cognitive psychology and accessibility principles.",
                 "UI/UX Humanized Design",
                 "Design systems and interfaces that feel warm, clear and accessible, validated with real users at every iteration.",
                 "Design systems & component libraries\nInteractive prototypes & usability testing\nWCAG accessibility audits"),
                ("Cloud & DevOps Infrastructure", "fa-solid fa-cloud-bolt",
                 "Automated deployment pipelines, AWS/Azure cloud architecture, serverless scaling, and microservices management.",
                 "Cloud & DevOps Infrastructure",
                 "Resilient cloud foundations with automated delivery, so releases are boring and uptime is not.",
                 "CI/CD pipelines & infrastructure as code\nAWS / Azure architecture\n24/7 monitoring & incident response"),
                ("AI Integration & Automation", "fa-solid fa-diagram-project",
                 "Smart workflow automation, LLM integrations, predictive analytics engines, and custom machine learning pipelines.",
                 "AI Integration & Automation",
                 "Practical AI that removes repetitive work and surfaces insight from your own data.",
                 "LLM-powered assistants & workflows\nPredictive analytics engines\nCustom ML pipelines"),
                ("Digital Growth Strategy", "fa-solid fa-chart-line",
                 "Data-driven performance marketing, conversion rate optimization (CRO), and strategic technical product roadmap planning.",
                 "Digital Growth Strategy",
                 "Strategy and experimentation that connect product decisions to measurable business growth.",
                 "Conversion rate optimization\nProduct roadmap planning\nAnalytics & performance marketing"),
            ]
            for i, (t, icon, short, ft, fd, feats) in enumerate(services):
                Service.objects.create(title=t, icon=icon, short_description=short, full_title=ft,
                                       full_description=fd, features=feats, order=i)

        if not ProcessStep.objects.exists():
            for i, (n, t, d) in enumerate([
                ("01", "Discovery & Blueprint", "Deep dive into stakeholder vision, market analysis, user personas, and core technical specification."),
                ("02", "Human Centric UX", "Wireframing, clickable design prototypes, design system build, and iterative UX validations."),
                ("03", "Agile Engineering", "Clean modular code creation, continuous integration, automated testing, and sprint reviews."),
                ("04", "Launch & Scale", "Cloud deployment, performance auditing, 24/7 proactive monitoring, and post-launch evolution."),
            ]):
                ProcessStep.objects.create(number=n, title=t, description=d, order=i)

        if not Project.objects.exists():
            projects = [
                ("Nova Fintech Analytics", "saas", "SaaS Enterprise", "Next-gen banking dashboard with real-time portfolio tracking and AI forecasting.",
                 "A comprehensive cloud platform handling millions of daily micro-transactions with zero latency.", "#1e1b4b", "#7c3aed", True),
                ("Pulse Telehealth Mobile", "mobile", "Mobile iOS/Android", "Encrypted patient monitoring mobile app with live biometric integrations.",
                 "Seamless doctor-patient video consultations with HIPAA compliant cloud storage.", "#4c1d95", "#8b5cf6", True),
                ("Aura Luxury Marketplace", "web", "Web Platform", "Ultra-fast headless e-commerce store with 3D product customizer integrations.",
                 "Boosted checkout conversions by 42% through interactive 3D product previews.", "#311042", "#6d28d9", True),
                ("Apex Global Supply Chain", "web", "Web Platform", "Automated IoT fleet tracking engine reducing operational downtime by 34%.",
                 "Real-time fleet telemetry across 12 countries with predictive maintenance alerts.", "#1e1b4b", "#4338ca", False),
                ("Krypton Pay Gateway", "saas", "SaaS Enterprise", "PCI-DSS compliant cross-border payment checkout system processing $50M+ monthly.",
                 "Multi-currency settlement with fraud scoring and sub-second authorization.", "#6d28d9", "#a78bfa", False),
                ("Medix Diagnostic Portal", "saas", "SaaS Enterprise", "AI-driven radiology scan analyzer assisting medical practitioners globally.",
                 "Assistive imaging analysis that shortens report turnaround for radiology teams.", "#0f172a", "#5b21b6", False),
            ]
            for i, (t, cat, badge, desc, det, c1, c2, feat) in enumerate(projects):
                p = Project(title=t, category=cat, badge=badge, description=desc, details=det,
                            is_featured=feat, order=i)
                p.image.save(f"project-{i + 1}.png", banner(t, c1, c2), save=False)
                p.save()

        if not Testimonial.objects.exists():
            people = [
                ("Sarah Jenkins", "CTO at Nexus Fintech", "#8b5cf6",
                 "Xplorer Solution completely transformed our SaaS infrastructure. Their attention to subtle human details, combined with rigid security standards, delivered our best product launch to date."),
                ("Michael Chang", "Product VP, BioPulse Health", "#4c1d95",
                 "The team at Xplorer Solution brings a rare level of engineering perfection. They rebuilt our mobile healthcare application with incredible speed and elegance."),
                ("Amara Patel", "Founder, Zenith Ecommerce", "#6d28d9",
                 "Incredible UX design sensitivity combined with clean cloud backend execution. They feel like a natural extension of our in-house engineering team."),
                ("David Miller", "Founder, CloudScale Inc", "#7c3aed",
                 "The speed of delivery and humanized UI components built by Xplorer Solution allowed us to secure our Series A funding ahead of schedule."),
                ("Elena Rostova", "VP Product, HealthDirect", "#4c1d95",
                 "Professionalism at its peak. The interactive subtle canvas elements and fast loading speeds give our mobile web users an extraordinary experience."),
            ]
            for i, (n, r, col, q) in enumerate(people):
                t = Testimonial(name=n, role=r, quote=q, rating=5, order=i, show_on_home_slider=i < 3)
                t.avatar.save(f"avatar-{i + 1}.png", avatar(n[0], col), save=False)
                t.save()

        if not BlogPost.objects.exists():
            posts = [
                ("Why Humanized UI Principles Win Modern SaaS Markets", "Design Systems",
                 "Exploring how soft light palettes, gentle micro-interactions, and clear hierarchy reduce cognitive user fatigue.",
                 "Modern SaaS buyers compare products on how they feel as much as on feature lists. Interfaces that respect attention win trials, and trials win revenue.\n\nSoft palettes, generous spacing and predictable motion reduce the effort needed to understand a screen. Small micro-interactions confirm actions without shouting.\n\nThe practical takeaway: audit your product for moments of hesitation, then remove one source of friction per sprint.",
                 "#8b5cf6", "#4c1d95"),
                ("Architecting Zero-Downtime Microservices", "DevOps",
                 "A technical walkthrough of automated health checks and failover redundancy strategies.",
                 "Zero downtime is a property of the release process, not only of the infrastructure.\n\nStart with health checks that test real dependencies, route traffic gradually with rolling or canary deployments, and keep rollback one command away.\n\nFinally, rehearse failures. A failover that has never been exercised is a guess, not a plan.",
                 "#0f172a", "#6d28d9"),
                ("Balancing Canvas WebGL Effects with Speed", "Web Animation",
                 "How to render fluid interactive background mesh particles without compromising mobile frame rates.",
                 "Interactive backgrounds are cheap to build and easy to overspend on.\n\nCap particle counts by viewport area, pause animation when the tab is hidden, and avoid per-frame allocations. Measure on a mid-range phone, not on your development laptop.\n\nWhen in doubt, fewer particles with better motion beat more particles with dropped frames.",
                 "#6d28d9", "#a78bfa"),
            ]
            for t, cat, ex, body, c1, c2 in posts:
                bp = BlogPost(title=t, category=cat, excerpt=ex, content=body)
                bp.image.save(f"blog-{cat.lower().replace(' ', '-')}.png", banner(t, c1, c2), save=False)
                bp.save()

        if not FAQ.objects.exists():
            for i, (q, a) in enumerate([
                ("How long does a typical custom software project take?",
                 "Project timelines vary based on scope, but standard web and mobile MVP projects usually take between 4 to 8 weeks from initial discovery to production deployment."),
                ("Do you provide post-launch support and maintenance?",
                 "Yes, we offer comprehensive SLA maintenance packages that cover continuous security patches, server infrastructure optimization, feature updates, and 24/7 technical monitoring."),
                ("How do you ensure data security and privacy?",
                 "We adhere strictly to ISO 27001 standards, execute thorough penetration testing, utilize end-to-end encryption for all sensitive payloads, and sign strict Mutual NDAs before project commencement."),
            ]):
                FAQ.objects.create(question=q, answer=a, order=i)

        if not ContactMessage.objects.exists():
            ContactMessage.objects.create(
                name="Alex Morgan", email="alex@example.com", subject="Custom Web Platform",
                message="Hi, we would like a quote for a customer portal. Can we schedule a call?",
            )
        if not NewsletterSubscriber.objects.exists():
            NewsletterSubscriber.objects.create(email="reader@example.com")

        # ---------- Service detail pages (fills only services that have no detail text yet) ----------
        details = [
            {
                "title": "Custom Web Architecture",
                "colors": ("#4c1d95", "#8b5cf6"),
                "tagline": "Fast, secure and scalable web platforms engineered around your business model.",
                "overview": "We design and build web applications that stay quick under heavy traffic and easy to change as your business grows. From the data model to the last pixel, every layer is chosen for performance, security and maintainability.\n\nWhether you need a customer portal, a SaaS product or a high-traffic marketing site, our engineers pair clean architecture with a content workflow your team can run without a developer.",
                "technologies": "Django, React, PostgreSQL, Redis, REST APIs, Docker, Nginx",
                "features": [
                    ("Scalable Backend", "Modular services and caching that keep response times low as traffic grows.", "fa-solid fa-server"),
                    ("Lightning-Fast Frontend", "Optimised bundles, lazy loading and Core Web Vitals tuned from day one.", "fa-solid fa-gauge-high"),
                    ("Admin & CMS Control", "A clean admin panel so your team can update content without code.", "fa-solid fa-sliders"),
                    ("Security by Design", "Hardened authentication, input validation and encrypted data at rest.", "fa-solid fa-lock"),
                    ("SEO-Ready Pages", "Semantic markup, fast loading and structured data for better rankings.", "fa-solid fa-magnifying-glass-chart"),
                    ("API Integrations", "Payments, CRMs and third-party tools connected through reliable APIs.", "fa-solid fa-plug"),
                ],
                "steps": [
                    ("Discovery & Architecture", "We map goals, users and data, then agree a technical blueprint."),
                    ("Design & Prototype", "Clickable prototypes validate the flow before any code is written."),
                    ("Build in Sprints", "Two-week sprints with working demos and automated tests."),
                    ("Launch & Support", "Staged release, monitoring and a maintenance plan you can rely on."),
                ],
                "faqs": [
                    ("How long does a custom web project take?", "Most platforms take between 6 and 12 weeks, depending on features and integrations. We give a fixed timeline after discovery."),
                    ("Can my team manage content ourselves?", "Yes. Everything editable is exposed in an admin panel, so no developer is needed for day-to-day updates."),
                ],
            },
            {
                "title": "Mobile App Engineering",
                "colors": ("#311042", "#7c3aed"),
                "tagline": "Native-feeling iOS and Android apps that people keep on their home screen.",
                "overview": "We build mobile apps that feel fast, behave predictably offline and look right on every screen size. Our team ships from a single codebase when it makes sense, and goes fully native when performance demands it.\n\nFrom push notifications to biometric login, we handle the details that decide whether users stay or uninstall.",
                "technologies": "Flutter, React Native, Swift, Kotlin, Firebase, GraphQL",
                "features": [
                    ("Cross-Platform Delivery", "One codebase for iOS and Android with native-grade performance.", "fa-solid fa-mobile-screen-button"),
                    ("Offline-First Sync", "Apps keep working without a connection and sync safely afterwards.", "fa-solid fa-cloud-arrow-down"),
                    ("Push & In-App Messaging", "Timely, targeted notifications that bring users back.", "fa-solid fa-bell"),
                    ("Biometric Security", "Face and fingerprint login with secure token storage.", "fa-solid fa-fingerprint"),
                    ("Store Publishing", "We handle App Store and Play Store submissions and compliance.", "fa-solid fa-store"),
                ],
                "steps": [
                    ("Product Definition", "User journeys and a prioritised feature list for the first release."),
                    ("UX & UI Design", "Platform-aware screens designed for thumbs, not mice."),
                    ("Build & Test on Devices", "Continuous builds tested on real phones and tablets."),
                    ("Release & Improve", "Store launch, crash monitoring and data-driven updates."),
                ],
                "faqs": [
                    ("Native or cross-platform: which is better?", "For most products a cross-platform build saves time and budget. We recommend native only when you need heavy graphics or device-level features."),
                    ("Do you publish the app for us?", "Yes. We prepare store listings, screenshots and compliance, and submit the app on your behalf."),
                ],
            },
            {
                "title": "UI/UX Humanized Design",
                "colors": ("#5b21b6", "#c4b5fd"),
                "tagline": "Interfaces that feel warm, clear and effortless to use.",
                "overview": "Good design removes friction people never notice. We research your users, sketch the journey, and build interfaces that are accessible, consistent and pleasant to use.\n\nEvery project ships with a reusable design system, so your product stays coherent as it grows.",
                "technologies": "Figma, Design Systems, Prototyping, Usability Testing, WCAG, Motion Design",
                "features": [
                    ("User Research", "Interviews and analytics that reveal what people actually need.", "fa-solid fa-users-viewfinder"),
                    ("Design Systems", "Reusable components and tokens for consistent, faster delivery.", "fa-solid fa-swatchbook"),
                    ("Interactive Prototypes", "Test ideas with real users before investing in development.", "fa-solid fa-hand-pointer"),
                    ("Accessibility Audits", "WCAG-aligned checks so everyone can use your product.", "fa-solid fa-universal-access"),
                    ("Micro-Interactions", "Subtle motion that guides attention and confirms actions.", "fa-solid fa-wand-magic-sparkles"),
                ],
                "steps": [
                    ("Understand", "Stakeholder workshops and user research set the direction."),
                    ("Explore", "Wireframes and visual concepts compared side by side."),
                    ("Refine", "Usability tests and iteration until the flow feels obvious."),
                    ("Hand Off", "A documented design system and developer-ready specs."),
                ],
                "faqs": [
                    ("Do you work with our existing brand?", "Absolutely. We extend your current identity into a consistent, scalable interface system."),
                    ("Will developers get usable files?", "Yes. You receive organised design files, tokens and specs that engineers can build from directly."),
                ],
            },
            {
                "title": "Cloud & DevOps Infrastructure",
                "colors": ("#1e1b4b", "#6d28d9"),
                "tagline": "Reliable cloud foundations and automated delivery, so releases stay boring.",
                "overview": "We design cloud environments that scale with demand and recover from failure automatically. Infrastructure is defined as code, deployments are automated, and monitoring tells you about problems before your users do.\n\nThe result is faster releases, lower hosting costs and far fewer late-night incidents.",
                "technologies": "AWS, Azure, Docker, Kubernetes, Terraform, GitHub Actions, Prometheus",
                "features": [
                    ("CI/CD Pipelines", "Every commit is built, tested and deployed automatically.", "fa-solid fa-arrows-rotate"),
                    ("Infrastructure as Code", "Repeatable environments defined in version-controlled templates.", "fa-solid fa-code-branch"),
                    ("Auto-Scaling", "Capacity that grows with traffic and shrinks to save cost.", "fa-solid fa-maximize"),
                    ("24/7 Monitoring", "Dashboards and alerts for uptime, errors and performance.", "fa-solid fa-chart-line"),
                    ("Backup & Recovery", "Tested disaster-recovery plans with clear recovery targets.", "fa-solid fa-life-ring"),
                    ("Cost Optimisation", "Right-sized resources and budgets that avoid surprise bills.", "fa-solid fa-piggy-bank"),
                ],
                "steps": [
                    ("Assess", "Review your current hosting, risks and monthly cost."),
                    ("Architect", "Design a secure, scalable target environment."),
                    ("Automate", "Build pipelines, templates and monitoring."),
                    ("Operate", "Ongoing support, tuning and incident response."),
                ],
                "faqs": [
                    ("Can you migrate our existing servers?", "Yes. We plan migrations in stages with rollback options so there is minimal or zero downtime."),
                    ("Which cloud providers do you support?", "We work with AWS and Azure, and can design provider-neutral setups using containers and Terraform."),
                ],
            },
            {
                "title": "AI Integration & Automation",
                "colors": ("#4c1d95", "#a78bfa"),
                "tagline": "Practical AI that removes repetitive work and surfaces real insight.",
                "overview": "We add AI where it genuinely saves time: answering customer questions, classifying documents, forecasting demand and automating routine workflows.\n\nEvery solution is built with human review where it matters, clear measurement of results, and safeguards around your data.",
                "technologies": "Python, LLM APIs, LangChain, Vector Databases, TensorFlow, Airflow",
                "features": [
                    ("Smart Assistants", "Chat and voice assistants trained on your own knowledge base.", "fa-solid fa-robot"),
                    ("Workflow Automation", "Hand repetitive approvals and data entry over to reliable bots.", "fa-solid fa-gears"),
                    ("Predictive Analytics", "Forecast demand, churn and risk from your historical data.", "fa-solid fa-chart-column"),
                    ("Document Intelligence", "Extract, classify and search information across files.", "fa-solid fa-file-lines"),
                    ("Data Privacy Controls", "Access rules and redaction so sensitive data stays protected.", "fa-solid fa-shield-halved"),
                ],
                "steps": [
                    ("Find the Use Case", "We pick high-impact tasks with measurable outcomes."),
                    ("Prototype Quickly", "A working proof of concept in weeks, not months."),
                    ("Integrate Safely", "Connect to your systems with review steps and logging."),
                    ("Measure & Improve", "Track accuracy and savings, then keep tuning."),
                ],
                "faqs": [
                    ("Is our data used to train public models?", "No. We configure solutions so your data stays within your environment and is not used for public model training."),
                    ("How do you measure success?", "We agree clear metrics up front, such as hours saved, response time or accuracy, and report on them regularly."),
                ],
            },
            {
                "title": "Digital Growth Strategy",
                "colors": ("#6d28d9", "#ddd6fe"),
                "tagline": "Data-led strategy that turns your product into a growth engine.",
                "overview": "We connect product decisions to business results. Through analytics, experimentation and conversion work, we find the changes that actually move revenue.\n\nYou get a clear roadmap, transparent reporting and a partner who tests ideas instead of guessing.",
                "technologies": "Google Analytics, A/B Testing, SEO, Heatmaps, CRM Automation, Looker Studio",
                "features": [
                    ("Growth Audit", "A full review of funnel, traffic and conversion bottlenecks.", "fa-solid fa-magnifying-glass-chart"),
                    ("Conversion Optimisation", "Structured experiments that lift sign-ups and sales.", "fa-solid fa-bullseye"),
                    ("SEO & Content Strategy", "Topic plans and technical fixes that earn lasting traffic.", "fa-solid fa-pen-nib"),
                    ("Analytics Setup", "Clean tracking and dashboards you can trust.", "fa-solid fa-chart-pie"),
                    ("Product Roadmapping", "Priorities backed by data and user feedback.", "fa-solid fa-map"),
                ],
                "steps": [
                    ("Baseline", "Measure where you are today and set targets."),
                    ("Hypothesise", "Rank improvement ideas by impact and effort."),
                    ("Experiment", "Run tests, learn quickly and keep what works."),
                    ("Scale", "Roll out winners and plan the next quarter."),
                ],
                "faqs": [
                    ("How soon will we see results?", "Quick wins often appear within the first month, while SEO and content gains compound over three to six months."),
                    ("Do you provide regular reports?", "Yes. You receive a monthly report with clear metrics, learnings and next steps."),
                ],
            },
        ]
        by_title = {d["title"]: d for d in details}
        for idx, svc in enumerate(Service.objects.all()):
            if svc.overview:
                continue  # keep anything already written in the admin
            d = by_title.get(svc.title) or details[idx % len(details)]
            svc.tagline = d["tagline"]
            svc.overview = d["overview"]
            svc.technologies = d["technologies"]
            c1, c2 = d["colors"]
            svc.detail_image.save(f"service-{svc.pk}.png", banner(svc.title, c1, c2, size=(900, 600)), save=False)
            svc.save()
            if not svc.detail_features.exists():
                for i, (t, desc, icon) in enumerate(d["features"]):
                    ServiceFeature.objects.create(service=svc, title=t, description=desc, icon=icon, order=i)
            if not svc.detail_steps.exists():
                for i, (t, desc) in enumerate(d["steps"]):
                    ServiceStep.objects.create(service=svc, title=t, description=desc, order=i)
            if not svc.detail_faqs.exists():
                for i, (q, a) in enumerate(d["faqs"]):
                    ServiceFAQ.objects.create(service=svc, question=q, answer=a, order=i)

        # ---------- Software management guideline slides (Who We Are carousel) ----------
        if not GuidelineSlide.objects.exists():
            for i, (t, badge, icon, pts, note) in enumerate([
                ("Agile Sprint Management", "SPRINT_FLOW", "fa-solid fa-arrows-rotate",
                 "Define a clear sprint goal and a prioritised backlog\nBreak stories into tasks of one day or less\nHold a 15-minute daily stand-up focused on blockers\nDemo working software at the end of every sprint\nRun a short retrospective and pick one improvement",
                 "Two-week sprints keep feedback fast and scope honest."),
                ("Code Quality & Version Control", "GIT_WORKFLOW", "fa-solid fa-code-branch",
                 "Use short-lived feature branches with clear commit messages\nReview every pull request with at least one peer\nRun linting and unit tests automatically on each push\nProtect the main branch and merge only when checks pass\nTag every release so rollbacks take minutes",
                 "Small pull requests are reviewed faster and break less."),
                ("Testing & QA Pipeline", "QA_PIPELINE", "fa-solid fa-bug",
                 "Cover business logic with unit tests and APIs with integration tests\nAutomate checks on the most important user journeys\nRun performance and security scans before every release\nKeep a staging environment that mirrors production\nTrack defects by severity with a named owner",
                 "Catching a bug in staging costs a fraction of fixing it live."),
                ("Release & Monitoring", "RELEASE_OPS", "fa-solid fa-rocket",
                 "Deploy through an automated CI/CD pipeline with one-click rollback\nUse feature flags for gradual, low-risk rollouts\nWatch uptime, errors and speed on live dashboards\nHold a health check within 24 hours of each release\nKeep a changelog so everyone knows what shipped",
                 "Ship small and often: smaller releases are safer releases."),
            ]):
                GuidelineSlide.objects.create(title=t, badge=badge, icon=icon, points=pts, note=note, order=i)

        # ---------- Guideline slide images + summaries (fills only what is empty) ----------
        slide_extra = {
            "SPRINT_FLOW": ("A repeatable two-week rhythm that keeps every stakeholder aligned and every release predictable.", ("#1e1b4b", "#7c3aed")),
            "GIT_WORKFLOW": ("A clean branching and review discipline so quality is built in, not bolted on at the end.", ("#312e81", "#8b5cf6")),
            "QA_PIPELINE": ("Layered automated and manual testing that finds problems while they are still cheap to fix.", ("#4c1d95", "#6d28d9")),
            "RELEASE_OPS": ("Safe, automated releases with live monitoring, so launches are calm and rollbacks are quick.", ("#0f172a", "#5b21b6")),
        }
        for g in GuidelineSlide.objects.all():
            summ, (c1, c2) = slide_extra.get(g.badge, ("A proven step in the way we manage every software project.", ("#1e1b4b", "#7c3aed")))
            changed = False
            if not g.summary:
                g.summary = summ
                changed = True
            if not g.image:
                g.image.save(f"guideline-{g.pk}.png", banner(g.title, c1, c2, size=(900, 700)), save=False)
                changed = True
            if changed:
                g.save()

        # ---------- Service guide pages: intro, audience, deliverables, results ----------
        svc_extra = {
            "Custom Web Architecture": (
                "This guide explains how we plan, build and launch custom web platforms, what you receive at each stage and the results teams typically see.",
                "Startups launching a first product\nBusinesses outgrowing a template website\nTeams that need a portal or SaaS platform\nCompanies with slow or insecure legacy sites",
                "Architecture document and data model\nResponsive production-ready website or web app\nAdmin panel with training\nDeployment and 30 days of support",
                [("2x", "Faster page loads"), ("99.9%", "Uptime target"), ("40%", "Less admin effort"), ("30+", "Projects shipped")]),
            "Mobile App Engineering": (
                "A walk-through of our mobile process, from product discovery to store release and ongoing improvement.",
                "Founders building an iOS or Android product\nCompanies extending a web service to mobile\nHealthcare, fintech and retail teams\nBusinesses replacing an ageing app",
                "Clickable prototype\niOS and Android builds\nApp Store and Google Play submission\nAnalytics and crash reporting setup",
                [("4.8", "Average store rating"), ("60%", "Faster time to market"), ("2", "Platforms, one codebase"), ("25+", "Apps launched")]),
            "UI/UX Humanized Design": (
                "How our research-led design process turns user needs into interfaces people enjoy using.",
                "Products with low conversion or high drop-off\nTeams starting a new product\nBrands needing a consistent design system\nStartups preparing for investor demos",
                "User research summary\nWireframes and high-fidelity screens\nInteractive prototype\nDesign system and handoff files",
                [("35%", "Higher conversion"), ("50%", "Fewer support tickets"), ("120+", "Screens designed"), ("98%", "Client satisfaction")]),
            "Cloud & DevOps Infrastructure": (
                "A clear overview of how we move you to resilient cloud infrastructure with automated delivery.",
                "Teams deploying manually and slowly\nBusinesses with costly or unstable hosting\nCompanies preparing for traffic growth\nProducts that need strong security and compliance",
                "Infrastructure as code\nCI/CD pipelines\nMonitoring dashboards and alerts\nCost and security report",
                [("60%", "Faster deployments"), ("30%", "Lower cloud bill"), ("99.95%", "Availability"), ("24/7", "Monitoring")]),
            "AI Integration & Automation": (
                "This guide shows where AI and automation create real value and how we bring them into your product safely.",
                "Teams with repetitive manual work\nProducts that need search, chat or recommendations\nOperations that depend on document processing\nBusinesses exploring AI with clear goals",
                "Use-case assessment\nWorking AI or automation prototype\nIntegration with your systems\nEvaluation report and usage guidelines",
                [("70%", "Manual work removed"), ("5x", "Faster processing"), ("90%", "Answer accuracy"), ("12", "Automations live")]),
            "Digital Growth Strategy": (
                "How we combine SEO, content, analytics and campaigns into a growth plan you can measure.",
                "Businesses with traffic but few leads\nBrands entering a new market\nTeams without clear analytics\nStartups that need predictable growth",
                "Audit and growth roadmap\nSEO and content plan\nCampaign setup and tracking\nMonthly performance reports",
                [("3x", "Organic traffic"), ("45%", "Lower cost per lead"), ("120%", "Lead growth"), ("6", "Months to compound")]),
        }
        default_extra = ("A complete overview of how this service works, what you receive and the results you can expect.",
                         "Teams that want a reliable delivery partner\nBusinesses planning a new digital product\nCompanies replacing outdated systems",
                         "Project plan and timeline\nWorking deliverables at every milestone\nDocumentation and handover\nPost-launch support",
                         [("98%", "Client satisfaction"), ("30+", "Projects delivered"), ("24/7", "Support"), ("5x", "Faster delivery")])
        for svc in Service.objects.all():
            intro, ideal, deliv, outs = svc_extra.get(svc.title, default_extra)
            if not svc.guide_intro:
                svc.guide_intro = intro
            if not svc.ideal_for:
                svc.ideal_for = ideal
            if not svc.deliverables:
                svc.deliverables = deliv
            svc.save()
            if not svc.outcomes.exists():
                for i, (v, l) in enumerate(outs):
                    ServiceOutcome.objects.create(service=svc, value=v, label=l, order=i)

        # ---------- Project case-study pages (fills only empty fields) ----------
        case = {
            "Nova Fintech Analytics": dict(client="Nexus Fintech", year="2025", duration="16 weeks", role="UX design, Web development, Cloud", technologies="Django, React, PostgreSQL, Redis, WebSockets, AWS",
                challenge="Analysts worked across five disconnected tools, so portfolio numbers were always minutes behind the market.\n\nThe old system also struggled whenever trading volume spiked.",
                solution="We built one real-time dashboard fed by streaming market data and a forecasting service that scores each portfolio.\n\nA caching layer and queue-based processing keep the interface instant, even at peak load.",
                techniques="Event streaming: Market ticks are pushed to the browser over WebSockets instead of polling.\nPredictive scoring: A forecasting model ranks risk and opportunity per portfolio.\nQuery caching: Hot dashboards are served from Redis in milliseconds.\nRole-based access: Every widget respects the analyst's permissions.",
                key_features="Real-time portfolio tracking\nAI forecasting and alerts\nCustom report builder\nAudit trail for every change",
                quote="Xplorer Solution completely transformed our SaaS infrastructure and delivered our best product launch to date.", quote_author="Sarah Jenkins, CTO at Nexus Fintech",
                results=[("3x", "Faster reporting"), ("99.9%", "Uptime"), ("40%", "Less analyst time"), ("2M+", "Daily transactions")]),
            "Pulse Telehealth Mobile": dict(client="BioPulse Health", year="2025", duration="14 weeks", role="Mobile engineering, Security, UI design", technologies="React Native, Node.js, WebRTC, PostgreSQL, AWS",
                challenge="Doctors needed to watch patient vitals and hold video visits without juggling separate apps, while keeping all data private.",
                solution="One encrypted mobile app combines live biometric feeds, secure video consultations and a clinician dashboard.\n\nAll records are stored in a compliant cloud with strict access logging.",
                techniques="End-to-end encryption: Video and messages are encrypted on the device.\nDevice integrations: Wearable data is synced through background services.\nOffline-first design: Readings are queued and uploaded when the network returns.\nAccessibility review: Large text and clear contrast for every patient.",
                key_features="Secure video consultations\nLive biometric monitoring\nAppointment scheduling\nDoctor and patient dashboards",
                quote="The team rebuilt our mobile healthcare application with incredible speed and elegance.", quote_author="Michael Chang, Product VP at BioPulse Health",
                results=[("4.8", "Store rating"), ("65%", "Fewer clinic visits"), ("50K", "Active patients"), ("12 wk", "To launch")]),
            "Aura Luxury Marketplace": dict(client="Zenith Ecommerce", year="2024", duration="12 weeks", role="UX design, Headless e-commerce, 3D", technologies="Next.js, Django, Stripe, Three.js, Elasticsearch, Cloudflare",
                challenge="Shoppers hesitated to buy high-value products they could not inspect, and the old storefront was slow on mobile.",
                solution="A headless storefront with an interactive 3D customizer lets buyers rotate and personalise products before they pay.\n\nEdge caching keeps every page fast worldwide.",
                techniques="Headless commerce: The front end and the catalogue are separate, so each can scale on its own.\n3D product viewer: Lightweight models load on demand and run smoothly on phones.\nSmart search: Instant, typo-tolerant product search.\nOne-step checkout: Fewer fields and saved wallets.",
                key_features="3D product customizer\nInstant search and filters\nOne-step checkout\nMulti-currency pricing",
                quote="Incredible UX sensitivity combined with clean cloud backend execution.", quote_author="Amara Patel, Founder at Zenith Ecommerce",
                results=[("42%", "Higher conversion"), ("1.2s", "Page load"), ("2.5x", "Mobile revenue"), ("-30%", "Returns")]),
            "Apex Global Supply Chain": dict(client="Apex Logistics", year="2024", duration="20 weeks", role="IoT platform, Data engineering, Web app", technologies="Python, Kafka, TimescaleDB, React, MQTT, Kubernetes",
                challenge="Fleet managers had no live view of vehicles across twelve countries, so breakdowns were discovered only after delays happened.",
                solution="We connected vehicle sensors to a streaming platform and built a control tower that predicts maintenance needs before failures occur.",
                techniques="Streaming ingestion: Thousands of sensor messages per second are processed in real time.\nPredictive maintenance: Models flag parts likely to fail.\nGeofencing: Automatic alerts for route and zone breaches.\nMulti-region deployment: Local processing keeps latency low.",
                key_features="Live fleet map\nPredictive maintenance alerts\nRoute and fuel analytics\nCustomer delivery tracking",
                quote="Downtime dropped sharply once the control tower went live.", quote_author="Operations Director, Apex Logistics",
                results=[("34%", "Less downtime"), ("12", "Countries"), ("8K", "Vehicles tracked"), ("18%", "Fuel saved")]),
            "Krypton Pay Gateway": dict(client="Krypton Financial", year="2025", duration="18 weeks", role="Payments engineering, Security, Compliance", technologies="Go, Django, PostgreSQL, Kafka, Redis, Kubernetes",
                challenge="Cross-border merchants lost sales to slow authorisations and high fraud, and needed full PCI-DSS compliance.",
                solution="A multi-currency gateway with sub-second authorisation, real-time fraud scoring and automatic settlement.\n\nCard data is tokenised so merchants never touch it.",
                techniques="Tokenisation: Card details are replaced with safe tokens.\nFraud scoring: Every payment is scored in milliseconds.\nIdempotent APIs: Retries never create double charges.\nLedger design: Double-entry records make reconciliation exact.",
                key_features="Multi-currency settlement\nFraud scoring engine\nMerchant dashboard\nWebhooks and developer API",
                quote="Authorisation speed and reliability beat every provider we tested.", quote_author="Head of Payments, Krypton Financial",
                results=[("$50M+", "Monthly volume"), ("<1s", "Authorisation"), ("-60%", "Fraud losses"), ("PCI", "DSS compliant")]),
            "Medix Diagnostic Portal": dict(client="Medix Imaging", year="2025", duration="22 weeks", role="AI integration, Web app, Security", technologies="Python, PyTorch, Django, React, DICOM, AWS",
                challenge="Radiologists faced growing scan backlogs and needed a second opinion tool that fits into their existing workflow.",
                solution="We built a secure portal that analyses scans, highlights areas of interest and drafts structured reports for the radiologist to review and approve.",
                techniques="Assistive imaging AI: Models highlight regions for review; the doctor always decides.\nDICOM integration: Works with existing scanners and archives.\nHuman-in-the-loop review: Every report is confirmed by a clinician.\nPrivacy by design: Data is anonymised and access is logged.",
                key_features="AI-assisted scan analysis\nStructured report drafting\nWorklist prioritisation\nSecure sharing with clinicians",
                quote="Report turnaround time fell dramatically without changing how our doctors work.", quote_author="Chief Radiologist, Medix Imaging",
                results=[("45%", "Faster reports"), ("96%", "Detection accuracy"), ("200+", "Clinicians"), ("1M", "Scans analysed")]),
        }
        for pj in Project.objects.all():
            d = case.get(pj.title)
            if not d:
                continue
            if not pj.client:
                for f in ("client", "year", "duration", "role", "technologies", "challenge", "solution", "techniques", "key_features", "quote", "quote_author"):
                    if not getattr(pj, f):
                        setattr(pj, f, d[f])
                pj.save()
            if not pj.results.exists():
                for i, (v, l) in enumerate(d["results"]):
                    ProjectResult.objects.create(project=pj, value=v, label=l, order=i)
            if not pj.gallery.exists():
                for i, (cap, c1, c2) in enumerate([("Dashboard overview", "#1e1b4b", "#7c3aed"), ("Core workflow", "#312e81", "#8b5cf6"), ("Mobile experience", "#4c1d95", "#6d28d9")]):
                    gi = ProjectImage(project=pj, caption=cap, order=i)
                    gi.image.save(f"project-{pj.pk}-g{i + 1}.png", banner(f"{pj.title} - {cap}", c1, c2, size=(800, 600)), save=False)
                    gi.save()

        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin12345")
            self.stdout.write(self.style.SUCCESS("Admin created -> username: admin  password: admin12345"))

        self.stdout.write(self.style.SUCCESS("Dummy data ready."))
