"""Email helpers. All SMTP settings come from the admin panel (Site Settings > Email)."""
import logging

from django.core.mail import EmailMessage, get_connection
from django.utils import timezone

from .models import SiteSettings

log = logging.getLogger(__name__)


def _connection(site):
    if site.email_enabled and site.email_host:
        return get_connection(
            "django.core.mail.backends.smtp.EmailBackend",
            host=site.email_host, port=site.email_port,
            username=site.email_host_user, password=site.email_host_password,
            use_tls=site.email_use_tls, use_ssl=site.email_use_ssl and not site.email_use_tls,
            timeout=15,
        )
    return get_connection()  # console backend (prints in the terminal)


def _from(site):
    addr = site.email_host_user or site.email
    return f"{site.email_from_name} <{addr}>" if site.email_from_name else addr


def _send(site, subject, body, to, reply_to=None):
    msg = EmailMessage(subject, body, _from(site), [to], reply_to=[reply_to] if reply_to else None,
                       connection=_connection(site))
    msg.send(fail_silently=False)


def on_new_message(cm):
    """Alert the site owner and thank the visitor. Never raises; the result is stored on the message."""
    site = SiteSettings.load()
    results = []
    if site.send_notification:
        to = site.notify_email or site.email
        try:
            _send(site, f"New website message: {cm.subject or cm.name}",
                  f"From: {cm.name} <{cm.email}>\nSubject: {cm.subject}\nReceived: {timezone.localtime(cm.created_at):%Y-%m-%d %H:%M}\n\n{cm.message}\n\n"
                  "(Reply to this email to answer the visitor directly.)", to, reply_to=cm.email)
            results.append("alert sent")
        except Exception as e:  # noqa: BLE001
            log.warning("notify failed: %s", e)
            results.append(f"alert FAILED: {str(e)[:70]}")
    if site.send_auto_reply:
        try:
            body = (site.auto_reply_body or "").replace("{name}", cm.name)
            _send(site, site.auto_reply_subject, body, cm.email, reply_to=site.notify_email or site.email)
            results.append("auto-reply sent")
        except Exception as e:  # noqa: BLE001
            log.warning("auto reply failed: %s", e)
            results.append(f"auto-reply FAILED: {str(e)[:70]}")
    cm.email_status = " | ".join(results)[:200]
    cm.save(update_fields=["email_status"])


def send_reply(cm):
    """Send cm.reply to the visitor. Returns (ok, error)."""
    site = SiteSettings.load()
    try:
        _send(site, f"Re: {cm.subject or 'your message'}", cm.reply, cm.email, reply_to=site.notify_email or site.email)
    except Exception as e:  # noqa: BLE001
        return False, str(e)
    cm.replied_at = timezone.now()
    cm.is_read = True
    cm.save(update_fields=["replied_at", "is_read"])
    return True, ""
