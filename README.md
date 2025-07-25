﻿<p align="center">
  <img src="assets/icons/casestudies_banner.png" alt="CaseStudies Banner" width="1586" height="">
</p>

# CaseStudies Platform

[![Django](https://img.shields.io/badge/Django-4.2.14-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4.0-38B2AC.svg)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **CaseStudies** is a Django-based platform for curating and presenting real-world business case studies. It helps professionals, students, and decision-makers understand complex business challenges and their solutions through hands-on, data-driven stories.

## 🌟 Features

- **📚 Case Study Library**: Curated collection of real business cases with detailed analysis
- **🔍 Advanced Search**: Filter by title, domain, difficulty level, and more
- **📱 Responsive Design**: Modern, mobile-first interface built with Tailwind CSS
- **👥 User Submissions**: Community-driven case study submissions with approval workflow
- **📧 Email Notifications**: Automated email system for submission updates
- **🔒 Admin Panel**: Comprehensive content management system
- **📊 Analytics**: Built-in logging and analytics tracking
- **🌐 SEO Optimized**: Search engine friendly with proper meta tags and sitemaps

## 🏗️ Technology Stack

### Backend
- **Django 4.2.14** - Web framework
- **Python 3.8+** - Programming language
- **PostgreSQL** - Production database (SQLite for development)
- **Gunicorn** - WSGI server
- **WhiteNoise** - Static file serving
-**CkEditor 5** - For RTF

### Frontend
- **Tailwind CSS 3.4.0** - Utility-first CSS framework
- **Alpine.js** - Lightweight JavaScript framework
- **Heroicons** - Beautiful SVG icons
- **Epilogue Font** - Google Fonts typography


## 📁 Project Structure

```
casestudy/
├── 📁 casestudies/                 # Main Django app
│   ├── 📁 migrations/             # Database migrations
│   ├── 📁 templates/              # HTML templates
│   │   └── 📁 casestudies/        # App-specific templates
│   │       ├── 📁 email/          # Email templates
│   │       └── *.html             # Page templates
│   ├── 📁 templatetags/           # Custom template tags
│   ├── 📄 models.py               # Database models
│   ├── 📄 views.py                # View logic
│   ├── 📄 urls.py                 # URL routing
│   ├── 📄 admin.py                # Admin configuration
│   ├── 📄 forms.py                # Form definitions
│   ├── 📄 utils.py                # Utility functions
│   └── 📄 apps.py                 # App configuration
├── 📁 casestudy_project/          # Django project settings
│   ├── 📄 settings.py             # Project settings
│   ├── 📄 urls.py                 # Main URL configuration
│   └── 📄 wsgi.py                 # WSGI configuration
├── 📁 assets/                     # Static assets
│   ├── 📁 css/                    # CSS files
│   │   ├── 📄 input.css           # Tailwind source
│   │   └── 📄 output.css          # Compiled CSS
│   ├── 📁 icons/                  # Icon assets
│   ├── 📁 Illustration/           # Video illustrations
│   └── 📄 tailwind.config.js      # Tailwind configuration
├── 📁 media/                      # User-uploaded files
├── 📁 staticfiles/                # Collected static files
├── 📁 logs/                       # Application logs
├── 📄 requirements.txt            # Python dependencies
├── 📄 package.json                # Node.js dependencies
├── 📄 manage.py                   # Django management script
└── 📄 README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+
- Git
- PostgreSQL (for production)

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/castudies/casestudies.git
cd casestudies

# 2. Set up Python environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt

# 3. Set up Node.js dependencies
npm install

# 4. Build CSS assets
npm run build-prod

# 5. Configure environment variables
cp .env.example .env
# Edit .env with your configuration

# 6. Run database migrations
python manage.py migrate

# 7. Create a superuser
python manage.py createsuperuser

# 8. Start the development server
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) to view the app.

## 🛠️ Production Deployment

- Set environment variables for Django, database, and AWS S3.
- Collect static files: `python manage.py collectstatic --noinput`
- Run migrations: `python manage.py migrate`
- Start with Gunicorn: `gunicorn casestudy_project.wsgi:application`

## 🤝 How to Contribute

We welcome contributions from everyone! Here's how you can help:

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR-USERNAME/casestudies.git
cd casestudies
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or for bug fixes
git checkout -b fix/your-bug-description
```

### 3. Set Up Your Environment

Follow the [Quick Start](#quick-start) guide above.

### 4. Make Your Changes

- Write clean, well-documented code.
- Follow the existing code style (PEP8 for Python, semantic HTML, BEM or utility classes for CSS).
- Add or update tests if needed.
- Update documentation as needed.

### 5. Test Your Changes

```bash
python manage.py test
npm run build-prod
```

### 6. Commit & Push

```bash
git add .
git commit -m "feat: add new feature"
git push origin feature/your-feature-name
```

### 7. Open a Pull Request

- Go to the GitHub repo and open a PR.
- Fill out the PR template and describe your changes.

## 📝 Contribution Guidelines

- **Code Style:** PEP8 for Python, semantic HTML, BEM or utility classes for CSS.
- **Commits:** Use [Conventional Commits](https://www.conventionalcommits.org/).
- **PRs:** Small, focused, and well-documented.
- **Tests:** Add/maintain tests for new features and bug fixes.
- **Docs:** Update documentation for any user-facing or developer-facing changes.

## 🐛 Reporting Issues

- Search [existing issues](https://github.com/castudies/casestudies/issues) before opening a new one.
- Use the issue template and provide as much detail as possible (steps to reproduce, expected/actual behavior, screenshots, environment).

## 🌟 Support This Project

You can support us in many ways:

- **🌟 Star this repo** on GitHub
- **☕ Buy me a coffee:** [Ko-fi](https://ko-fi.com/mushfikurahmaan)
- **💰 Donate:** [GitHub Sponsors](https://github.com/sponsors/castudies) | [PayPal](#)
- **📣 Share:** Post about us on LinkedIn, Reddit, Twitter, or your blog
- **📤 Contribute:** Submit your own case study
- **🐛 Report bugs / suggest features:** Open an issue or discussion

See the [Support This Project page](https://www.castudies.com/support/) for more details.

## 🏢 Organization

Maintained by the **CaseStudies Organization**.

🌐 **Website:** [CaseStudies](https://www.castudies.com)  
📧 **Email:** [Mail us](mailto:contact@castudies.com)
## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Django, Tailwind CSS, Gumroad and the open source community
- All contributors and case study authors
