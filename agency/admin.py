from django.contrib import admin
from django.utils.html import format_html

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
    ProjectImage,
    ProjectResult,
    Service,
    ServiceFAQ,
    ServiceFeature,
    ServiceOutcome,
    ServiceStep,
    SiteSettings,
    Stat,
    TeamMember,
    Testimonial,
    TrustBadge,
)


class ImagePreviewMixin:
    image_field = "image"

    @admin.display(description="Preview")
    def preview(self, obj):
        img = getattr(obj, self.image_field, None)
        if img:
            return format_html(
                '<img src="{}" style="height:48px;border-radius:8px;object-fit:cover;">', img.url
            )
        return "-"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Branding", {"fields": ("site_name", "site_suffix", "meta_title")}),
        ("Hero Section", {"fields": ("hero_badge", "hero_title_prefix", "hero_title_highlight", "hero_description")}),
        ("Who We Are (Home)", {"fields": (
            "who_badge", "who_title", "who_title_highlight", "who_text",
            "mission", "vision", "core_values",
            "capability_title", "capability_version", "capability_note",
        )}),
        ("Guidelines Slider (Who We Are)", {"fields": ("guidelines_badge", "guidelines_heading", "guidelines_text")}),
        ("Section Headings", {"fields": ("services_heading", "services_subheading", "process_heading", "process_subheading")}),
        ("Cost Estimator", {"fields": (
            "estimator_cost_per_screen", "estimator_cost_per_design_level",
            "estimator_mobile_multiplier", "estimator_full_multiplier",
        )}),
        ("Trust Strip (rating)", {"fields": ("rating_value", "rating_text")}),
        ("Industries Section", {"fields": ("industries_badge", "industries_heading", "industries_text")}),
        ("Clients Section", {"fields": ("clients_heading", "clients_text")}),
        ("Reviews Section", {"fields": ("reviews_heading", "reviews_summary")}),
        ("Core Values Section", {"fields": ("values_badge", "values_heading", "values_image", "values_image_preview", "process_button")}),
        ("Free Consultation Form (Home)", {"fields": ("consult_heading", "consult_text")}),
        ("Call To Action Banner", {"fields": ("cta_title", "cta_text", "cta_button")}),
        ("Contact Page", {"fields": ("contact_heading", "contact_text", "email", "phone", "address")}),
        ("WhatsApp", {"fields": ("whatsapp_enabled", "whatsapp_number", "whatsapp_message")}),
        ("Email settings (send & receive)", {"fields": (
            "email_enabled", "email_host", "email_port", "email_use_tls", "email_use_ssl",
            "email_host_user", "email_host_password", "email_from_name",
            "send_notification", "notify_email", "send_auto_reply", "auto_reply_subject", "auto_reply_body",
        )}),
        ("About Page", {"fields": (
            "about_heading", "about_intro", "about_subheading",
            "about_paragraph_1", "about_paragraph_2", "about_image", "about_image_preview",
            "team_heading", "team_subheading",
        )}),
        ("Footer & Social", {"fields": (
            "footer_text", "copyright_text", "facebook_url", "linkedin_url", "instagram_url",
            "github_url", "youtube_url", "privacy_text", "terms_text",
        )}),
    )

    readonly_fields = ("about_image_preview", "values_image_preview")

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        ff = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "email_host_password":
            from django import forms
            ff.widget = forms.PasswordInput(render_value=True, attrs={"autocomplete": "new-password"})
        return ff

    @admin.display(description="Current team photo")
    def about_image_preview(self, obj):
        if obj and obj.about_image:
            return format_html(
                '<img src="{}" style="max-height:160px;border-radius:12px;object-fit:cover;">',
                obj.about_image.url,
            )
        return "No photo uploaded yet"

    @admin.display(description="Current image")
    def values_image_preview(self, obj):
        if obj and obj.values_image:
            return format_html(
                '<img src="{}" style="max-height:160px;border-radius:12px;object-fit:cover;">',
                obj.values_image.url,
            )
        return "No image uploaded yet"

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        from django.shortcuts import redirect
        from django.urls import reverse

        obj = SiteSettings.load()
        return redirect(reverse("admin:agency_sitesettings_change", args=[obj.pk]))


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "order")
    list_editable = ("order",)


@admin.register(CapabilityBar)
class CapabilityBarAdmin(admin.ModelAdmin):
    list_display = ("label", "percent", "order")
    list_editable = ("percent", "order")


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1


class ServiceStepInline(admin.TabularInline):
    model = ServiceStep
    extra = 1


class ServiceOutcomeInline(admin.TabularInline):
    model = ServiceOutcome
    extra = 1


class ServiceFAQInline(admin.StackedInline):
    model = ServiceFAQ
    extra = 0


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "show_on_home", "show_on_services_page", "order")
    list_editable = ("show_on_home", "show_on_services_page", "order")
    search_fields = ("title",)
    readonly_fields = ("detail_image_preview",)
    inlines = [ServiceFeatureInline, ServiceStepInline, ServiceOutcomeInline, ServiceFAQInline]
    fieldsets = (
        (None, {"fields": ("title", "icon", "order", "show_on_home", "show_on_services_page")}),
        ("Card text (Home & Services page)", {"fields": ("short_description", "full_title", "full_description", "features")}),
        ("Detail page (opens from the 'View More' button)", {
            "description": "Add the feature cards, delivery steps and FAQs in the sections below this form.",
            "fields": ("tagline", "overview", "detail_image", "detail_image_preview", "technologies", "detail_cta"),
        }),
        ("Brochure download & Complete Guide page (outline 'Brochure' button)", {
            "description": "The button downloads the PDF and opens the guide page. Leave the PDF empty to auto-generate one. Add expected results below this form.",
            "fields": ("brochure", "guide_intro", "ideal_for", "deliverables"),
        }),
    )

    @admin.display(description="Current image")
    def detail_image_preview(self, obj):
        if obj and obj.detail_image:
            return format_html(
                '<img src="{}" style="max-height:140px;border-radius:12px;object-fit:cover;">',
                obj.detail_image.url,
            )
        return "No image uploaded yet"


@admin.register(GuidelineSlide)
class GuidelineSlideAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("preview", "title", "badge", "is_active", "order")
    list_display_links = ("title",)
    list_editable = ("is_active", "order")


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ("number", "title", "deliverable", "order")
    list_editable = ("order",)


class ProjectResultInline(admin.TabularInline):
    model = ProjectResult
    extra = 1


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("preview", "title", "category", "is_featured", "order")
    list_display_links = ("title",)
    list_editable = ("is_featured", "order")
    list_filter = ("category", "is_featured")
    search_fields = ("title", "description")
    inlines = [ProjectResultInline, ProjectImageInline]
    fieldsets = (
        (None, {"fields": ("title", "category", "badge", "description", "image", "is_featured", "order")}),
        ("Case-study page (opens from 'View Case Details')", {
            "description": "Add the result numbers and gallery images in the sections below this form.",
            "fields": ("details", "client", "year", "duration", "role", "live_url", "challenge", "solution",
                       "technologies", "techniques", "key_features", "quote", "quote_author"),
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(ImagePreviewMixin, admin.ModelAdmin):
    image_field = "avatar"
    list_display = ("preview", "name", "role", "rating", "show_on_home_slider", "order")
    list_display_links = ("name",)
    list_editable = ("show_on_home_slider", "order")


@admin.register(TrustBadge)
class TrustBadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "subtitle", "icon", "order")
    list_editable = ("order",)


@admin.register(Industry)
class IndustryAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("preview", "name", "order")
    list_display_links = ("name",)
    list_editable = ("order",)


@admin.register(ClientLogo)
class ClientLogoAdmin(ImagePreviewMixin, admin.ModelAdmin):
    image_field = "logo"
    list_display = ("preview", "name", "order")
    list_display_links = ("name",)
    list_editable = ("order",)


@admin.register(ClientReview)
class ClientReviewAdmin(ImagePreviewMixin, admin.ModelAdmin):
    image_field = "avatar"
    list_display = ("preview", "name", "rating", "date_text", "is_published", "order")
    list_display_links = ("name",)
    list_editable = ("is_published", "order")


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)


@admin.register(TeamMember)
class TeamMemberAdmin(ImagePreviewMixin, admin.ModelAdmin):
    image_field = "photo"
    list_display = ("preview", "name", "role", "show_on_about", "order")
    list_display_links = ("name",)
    list_editable = ("show_on_about", "order")
    search_fields = ("name", "role")


@admin.register(BlogPost)
class BlogPostAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("preview", "title", "category", "is_published", "created_at")
    list_display_links = ("title",)
    list_editable = ("is_published",)
    list_filter = ("category", "is_published")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order")
    list_editable = ("order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read", "replied_at", "email_status")
    list_editable = ("is_read",)
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at", "email_status", "replied_at")
    fieldsets = (
        ("Message", {"fields": ("name", "email", "subject", "message", "created_at", "is_read", "email_status")}),
        ("Reply to the visitor", {"fields": ("reply", "replied_at")}),
    )
    actions = ["send_reply_email"]

    @admin.action(description="Send reply by email (uses the 'Your reply' text)")
    def send_reply_email(self, request, queryset):
        from . import mailer
        ok = 0
        for cm in queryset:
            if not cm.reply.strip():
                self.message_user(request, f"{cm}: write a reply first.", level="warning")
                continue
            sent, err = mailer.send_reply(cm)
            if sent:
                ok += 1
            else:
                self.message_user(request, f"{cm}: could not send ({err})", level="error")
        if ok:
            self.message_user(request, f"{ok} reply email(s) sent.")


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_at")
    search_fields = ("email",)
