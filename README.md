# Xplorer Solution - Django version

Original HTML design ka Django version. Poora content admin panel se manage hota hai.

## Chalane ka tareeqa

Windows: `setup.bat` double-click karein (ya terminal me chalayen).
Linux/Mac: `bash setup.sh`

Manually:

```
python -m venv venv
venv\Scripts\activate        (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python manage.py makemigrations agency
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/  (username `admin`, password `admin12345`)

Update ke baad (naye models): `python manage.py makemigrations agency` phir `python manage.py migrate` phir `python manage.py seed_data`.

Dark/Light mode: navbar ke moon/sun button se (choice browser me save hoti hai).

Dummy data dobara load karna ho: `python manage.py seed_data --reset`

## Admin panel me kya manage hota hai

| Section | Kya control karta hai |
|---|---|
| Site Settings | Brand name, hero text, mission/vision/values, section headings, estimator prices, CTA banner, contact info, About page (text + image), footer, social links, privacy/terms text |
| Hero Statistics | Home page ke 4 counter cards |
| Capability Bars | Dark card ke progress bars |
| Services | Home cards + Services page (icon, features list) |
| Process Steps | "How We Work" 4 steps |
| Projects | Project cards + full case-study page (client, year, duration, technologies, techniques, challenge/solution, results, gallery, quote) - /projects/ |
| Testimonials | Home slider + Testimonials page (avatar upload) |
| Blog Posts | Blog list + detail page (image upload) |
| FAQs | Home accordion |
| Trust Badges | Rating strip ke badges (icon, naam, subtitle, link) |
| Industries | "Industries We Work With" grid (image upload) |
| Client Logos | "Our Clients" scrolling logo strip (logo upload) |
| Client Reviews | Reviews grid (avatar upload, rating, date) |
| Core Values | "Thinking Behind Better Growth" list (image Site Settings se) |
| Team Members | About page team grid (photo upload) |
| Services (detail page) | "View More" page of each service: tagline, overview, image, technologies, plus inline What's included / Delivery steps / Service FAQs |
| Guideline Slides | Software management guideline slides in the "Who We Are" carousel |
| Contact Messages | Contact form se aaye messages |
| Newsletter Subscribers | Footer form se aaye emails |

Uploaded images `media/` folder me save hoti hain.

## Notes

- Production me `config/settings.py` me `DEBUG=False`, apni `SECRET_KEY` aur `ALLOWED_HOSTS` set karein.
- Footer ke "Capabilities" links static hain; baaki sab database se aata hai.


## v4 additions (admin panel mein sab editable)
- **Site Settings > Guidelines Slider**: heading/badge/text. **Guideline slides**: title, badge, summary, points, note, **image** (right side par dikhti hai).
- **Services**: har card par outline "Brochure" button -> guide page khulta hai aur PDF download hota hai. Service mein "Brochure download & Complete Guide page" section: apna PDF upload karein (warna PDF khud ban jata hai), intro, ideal for, deliverables. Inlines: Expected results, Features, Steps, FAQs.
- **Projects**: "Case-study page" section + inlines Results aur Gallery images. "View Case Details" -> /projects/<id>/<slug>/. Techniques ki line format: `Name: short explanation`.
- Purana /portfolio/ link /projects/ par redirect hota hai.
- Update ke baad: `python manage.py makemigrations agency`, `python manage.py migrate`, `python manage.py seed_data` (sirf khali data bharta hai).

## v5 additions
- Home page se "Who We Are" (text + capability card) aur "How We Work" sections hata diye gaye.
- **WhatsApp**: Admin > Site Settings > WhatsApp (number, pre-filled message, on/off). Site par floating button + Contact page card.
- **Email**: Admin > Site Settings > "Email settings". SMTP host/port/user/password bharein aur "Send emails through SMTP" on karein (Gmail ke liye App Password). Contact ya consultation form bharne par aapko alert email aati hai (Reply dabane se seedha visitor ko jawab jata hai) aur visitor ko auto thank-you email jati hai.
- **Reply**: Admin > Contact messages > message kholein > "Your reply" likhein > list mein message select karke action "Send reply by email".
- SMTP band ho to emails server terminal mein print hoti hain (testing).
- Update: `python manage.py makemigrations agency` aur `python manage.py migrate`.
