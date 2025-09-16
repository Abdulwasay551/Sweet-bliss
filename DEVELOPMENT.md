# Development Guide for Sweet Bliss

## Development Environment Setup

### Local Development
1. **Clone and Setup**:
   ```bash
   git clone https://github.com/Abdulwasay551/Sweet-bliss.git
   cd Sweet-bliss
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Database Setup**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py setup_sweetbliss  # Optional: Load sample data
   ```

3. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

### Key Development URLs
- **Homepage**: http://localhost:8000/
- **Wagtail Admin**: http://localhost:8000/admin/
- **Django Admin**: http://localhost:8000/django-admin/

## Project Architecture

### Apps Structure
- **business/**: Core business logic, models for products, partners, team
- **seo/**: SEO optimization features, meta tags, analytics
- **setting/**: Django project configuration

### Key Models
- **HomePage**: Landing page with dynamic content
- **Product**: FMCG products with categories and brands
- **Partner**: Business partners and suppliers
- **TeamMember**: Company team information
- **SEOMixin**: Advanced SEO capabilities for all pages

### Templates Structure
- **base/**: Base templates for layout
- **business/**: Page-specific templates
- **includes/**: Reusable components (header, footer, navigation)
- **blocks/**: Wagtail StreamField block templates

## Wagtail CMS Features

### Content Management
- **StreamFields**: Flexible content blocks for dynamic pages
- **Rich Text**: Advanced text editing with formatting
- **Image Management**: Automatic resizing and optimization
- **Page Tree**: Hierarchical page organization

### SEO Tools
- **Meta Tags**: Title, description, keywords for each page
- **Open Graph**: Facebook and social media optimization
- **Schema.org**: Structured data for rich snippets
- **Sitemaps**: Automatic XML sitemap generation

## Development Workflow

### Making Changes
1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes following Django/Wagtail best practices
3. Test your changes locally
4. Commit with descriptive messages
5. Push and create a pull request

### Database Changes
```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Static Files
```bash
# Collect static files for production
python manage.py collectstatic --noinput
```

## Common Development Tasks

### Adding New Products
1. Access Wagtail admin at `/admin/`
2. Go to "Snippets" → "Products"
3. Add product with brand, category, and details
4. Mark as "Featured" to show on homepage

### Creating New Pages
1. In Wagtail admin, go to "Pages"
2. Choose page type (About, Contact, etc.)
3. Add content using StreamFields
4. Configure SEO settings
5. Publish when ready

### Managing Team Members
1. Go to "Snippets" → "Team Members"
2. Add member information and photo
3. Set display order
4. Team will appear on About and Team pages

## Environment Variables

### Development (.env file)
```env
DEBUG=True
SECRET_KEY=your-development-key
```

### Production
```env
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/db
SECRET_KEY=your-production-key
ALLOWED_HOSTS=yourdomain.com
GOOGLE_ANALYTICS_ID=GA_MEASUREMENT_ID
```

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure virtual environment is activated
2. **Database Errors**: Run migrations with `python manage.py migrate`
3. **Static Files**: Run `python manage.py collectstatic`
4. **Permission Errors**: Check user permissions in Wagtail admin

### Getting Help
- Check Django/Wagtail documentation
- Review existing code and comments
- Check GitHub issues for similar problems
- Contact the development team

## Performance Tips

### Development
- Use `DEBUG=True` for detailed error messages
- Django Debug Toolbar can be added for profiling
- Use local SQLite database for faster development

### Production
- Set `DEBUG=False`
- Use PostgreSQL database
- Configure proper caching
- Optimize images and static files
- Use CDN for static file delivery

## Security Considerations

### Development
- Use strong passwords for admin accounts
- Keep dependencies updated
- Never commit sensitive data to Git

### Production
- Use environment variables for secrets
- Enable HTTPS with proper certificates
- Regular security updates
- Monitor for suspicious activity
- Backup database regularly

---

Happy coding! 🚀