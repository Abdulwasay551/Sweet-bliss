# Sweet Bliss 🍫

**Premium FMCG Distribution Management System**

A modern, SEO-optimized content management system built with Wagtail CMS for Sweet Bliss - a leading FMCG importer and distributor in Pakistan specializing in premium confectionery and beverage brands.

[![Django](https://img.shields.io/badge/Django-5.2.5-green.svg)](https://djangoproject.com)
[![Wagtail](https://img.shields.io/badge/Wagtail-7.1.1-blue.svg)](https://wagtail.org)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Compatible-blue.svg)](https://postgresql.org)

## 📋 Quick Links

- [🚀 Quick Start](#-quick-start) - Get the project running locally
- [📚 Documentation](#-documentation) - Development guides and API docs
- [🎛️ Admin Access](#️-admin-access) - Content management system
- [🚀 Deployment](#-deployment) - Production deployment guide
- [🤝 Contributing](#-contributing) - How to contribute to the project

## 🚀 About Sweet Bliss

Sweet Bliss is a premium FMCG importer and distributor connecting global confectionery and beverage brands with local markets across Pakistan. We specialize in bringing internationally recognized brands like Nestlé, Mars Wrigley, Ferrero, Pringles, KitKat, Nutella, and many more to Pakistani consumers.

### 🎯 Business Focus
- **FMCG Importing**: Direct relationships with global manufacturers
- **Distribution Network**: Reliable delivery to retailers, supermarkets, and wholesalers
- **Quality Assurance**: Authenticity and freshness guaranteed
- **Strategic Partnerships**: Building lasting business relationships

## 🛠️ Technology Stack

### Backend
- **Django 5.2.5** - Python web framework
- **Wagtail CMS 7.1.1** - Advanced content management system
- **PostgreSQL** - Production database
- **Django REST Framework** - API development
- **Wagtail API** - Headless CMS capabilities

### Frontend & Styling
- **HTML5/CSS3** - Modern responsive design
- **Wagtail StreamFields** - Flexible content blocks
- **Bootstrap-compatible** - Responsive components

### SEO & Analytics
- **Custom SEO Mixin** - Advanced SEO optimization
- **Google Analytics Integration** - Traffic tracking
- **Meta Tags & Open Graph** - Social media optimization
- **Structured Data (Schema.org)** - Rich snippets
- **XML Sitemaps** - Search engine indexing

### Deployment & Infrastructure
- **Gunicorn** - WSGI HTTP Server
- **WhiteNoise** - Static file serving
- **PostgreSQL** - Production database
- **Environment Variables** - Configuration management

## 📁 Project Structure

```
Sweet-bliss/
├── business/                 # Main business app
│   ├── models.py            # Business models (Products, Partners, etc.)
│   ├── views.py             # Business views and API endpoints
│   ├── admin.py             # Django admin configuration
│   ├── urls.py              # URL routing
│   └── management/
│       └── commands/
│           └── setup_sweetbliss.py  # Initial data setup
├── seo/                     # SEO optimization app
│   ├── models.py            # SEO models and mixins
│   └── admin.py             # SEO admin interface
├── setting/                 # Project settings
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── templates/               # HTML templates
│   ├── base/                # Base templates
│   ├── business/            # Business page templates
│   ├── includes/            # Reusable components
│   └── blocks/              # Wagtail block templates
├── static/                  # Static assets (CSS, JS, images)
├── staticfiles/             # Collected static files (production)
├── requirements.txt         # Python dependencies
├── manage.py                # Django management script
├── build.sh                 # Deployment build script
└── README.md                # This file
```

## 🚦 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL (for production) or SQLite (for development)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Abdulwasay551/Sweet-bliss.git
cd Sweet-bliss
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
# Development settings
DEBUG=True

# Database configuration (for development - uses SQLite by default)
# For production, set these PostgreSQL variables:
# DATABASE_URL=postgresql://user:password@localhost:5432/sweetbliss_db
# user=your_db_user
# password=your_db_password
# host=localhost
# port=5432
# dbname=sweetbliss_db

# Security (generate a new secret key for production)
SECRET_KEY=your-secret-key-here

# SEO & Analytics (optional)
GOOGLE_ANALYTICS_ID=your-ga-id
FACEBOOK_PIXEL_ID=your-pixel-id
```

### 5. Database Setup
```bash
# Run database migrations
python manage.py migrate

# Create a superuser account
python manage.py createsuperuser

# Set up initial Sweet Bliss data (optional)
python manage.py setup_sweetbliss
```

### 6. Collect Static Files (Production)
```bash
python manage.py collectstatic --noinput
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The application will be available at:
- **Frontend**: http://localhost:8000/
- **Wagtail Admin**: http://localhost:8000/admin/
- **Django Admin**: http://localhost:8000/django-admin/

## 🎛️ Admin Access

### Wagtail CMS Admin
Access the content management system at `/admin/`:
- Manage pages, products, and content
- SEO optimization tools
- Image and document management
- User permissions and workflows

### Django Admin
Access the Django admin at `/django-admin/`:
- User management
- Direct model access
- System administration

## 📊 Key Features

### 🏢 Business Management
- **Product Catalog**: Comprehensive FMCG product management
- **Partner Management**: Track business partners and suppliers
- **Brand Portfolio**: Organize products by global brands
- **Team Profiles**: Leadership team presentation

### 🎨 Content Management
- **Flexible Page Builder**: Wagtail StreamFields for dynamic content
- **Rich Text Editing**: Advanced WYSIWYG editor
- **Image Management**: Optimized image handling and delivery
- **Menu Management**: Dynamic navigation system

### 🔍 SEO Optimization
- **Advanced SEO Controls**: Title, meta descriptions, keywords
- **Social Media Integration**: Open Graph and Twitter Cards
- **Structured Data**: Schema.org markup
- **XML Sitemaps**: Automatic sitemap generation
- **Analytics Integration**: Google Analytics and Facebook Pixel

### 📱 Responsive Design
- **Mobile-First**: Optimized for all device sizes
- **Fast Loading**: Optimized assets and caching
- **Accessibility**: WCAG compliance features

### 🔐 Security Features
- **User Authentication**: Secure admin access
- **Permission System**: Role-based access control
- **CSRF Protection**: Built-in security measures
- **Environment Variables**: Secure configuration

## 🚀 Deployment

### Using the Build Script
```bash
chmod +x build.sh
./build.sh
```

### Manual Deployment Steps
```bash
# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate

# Start the application
gunicorn setting.wsgi:application
```

### Environment Variables (Production)
```env
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 🗄️ Database Models

### Business Models
- **HomePage**: Main landing page with hero sections
- **AboutPage**: Company information and team
- **ProductsPage**: Product catalog and filtering
- **ContactPage**: Contact information and forms
- **ServicesPage**: Service offerings
- **PortfolioPage**: Product portfolio showcase
- **PartnershipsPage**: Partnership opportunities

### Content Models
- **Product**: Individual product entries
- **Brand**: Product brands and manufacturers
- **Partner**: Business partners and suppliers
- **ProductCategory**: Product categorization
- **TeamMember**: Team member profiles

### SEO Models
- **SEOMixin**: Advanced SEO fields for all pages
- **GlobalSEOSettings**: Site-wide SEO configuration
- **RedirectRule**: Custom URL redirects

## 📚 Documentation

- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Detailed development setup and workflow guide
- **[API.md](API.md)** - Complete API documentation and examples
- **[doc.md](doc.md)** - Business requirements and content specifications

## 🤝 Contributing

We welcome contributions to improve the Sweet Bliss platform:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**: Follow the existing code style
4. **Run tests**: Ensure all tests pass
5. **Commit your changes**: `git commit -m "Add your feature"`
6. **Push to the branch**: `git push origin feature/your-feature-name`
7. **Submit a pull request**

### Development Guidelines
- Follow Django and Wagtail best practices
- Write descriptive commit messages
- Update documentation for new features
- Test your changes thoroughly
- See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed development workflow

## 📞 Support & Contact

### Sweet Bliss Business Contact
- **Email**: azan@sweetbliss.pk
- **Phone**: +92-315-7680420
- **Address**: 05-231, Ravi Park, Minar-e-Pakistan, Lahore, Punjab, Pakistan

### Technical Support
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check this README and code comments
- **Community**: Contribute to discussions and improvements

## 📄 License

This project is proprietary software owned by Sweet Bliss. All rights reserved.

## 🏷️ Version History

- **v1.0.0** - Initial release with core CMS functionality
- **Latest** - Enhanced SEO features and business management tools

---

**Built with ❤️ for Sweet Bliss - Bringing Sweet Moments Closer to You**

*Premium FMCG Distribution | Global Brands | Pakistani Markets*
