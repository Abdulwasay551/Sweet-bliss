from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from django.core.validators import MinLengthValidator, MaxLengthValidator
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.images.models import Image
from wagtail.images import get_image_model_string
from django.utils.translation import gettext_lazy as _


class SEOMixin(models.Model):
    """
    SEO mixin that can be added to any page or model to provide SEO functionality
    Wagtail already provides seo_title, so we'll extend with additional fields
    """
    # Meta description (Wagtail has search_description, we'll use a more specific one)
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        null=True,
        validators=[MaxLengthValidator(160)],
        help_text="Meta description for search engines (max 160 characters). If empty, search_description will be used.",
        verbose_name="Meta Description"
    )
    
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Keywords separated by commas",
        verbose_name="Meta Keywords"
    )
    
    # Open Graph fields
    og_title = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        help_text="Open Graph title (Facebook, Twitter sharing). If empty, seo_title will be used.",
        verbose_name="OG Title"
    )
    
    og_description = models.TextField(
        max_length=160,
        blank=True,
        null=True,
        help_text="Open Graph description (Facebook, Twitter sharing)",
        verbose_name="OG Description"
    )
    
    og_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Image for social media sharing (1200x630px recommended)",
        verbose_name="OG Image"
    )
    
    # Twitter Card fields
    twitter_title = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        help_text="Twitter card title",
        verbose_name="Twitter Title"
    )
    
    twitter_description = models.TextField(
        max_length=160,
        blank=True,
        null=True,
        help_text="Twitter card description",
        verbose_name="Twitter Description"
    )
    
    twitter_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Twitter card image (1200x600px recommended)",
        verbose_name="Twitter Image"
    )
    
    # Schema.org fields
    schema_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=[
            ('Website', 'Website'),
            ('Organization', 'Organization'),
            ('LocalBusiness', 'Local Business'),
            ('Product', 'Product'),
            ('Article', 'Article'),
            ('BlogPosting', 'Blog Posting'),
            ('WebPage', 'Web Page'),
            ('AboutPage', 'About Page'),
            ('ContactPage', 'Contact Page'),
        ],
        default='WebPage',
        help_text="Schema.org type for structured data",
        verbose_name="Schema Type"
    )
    
    # Advanced SEO settings
    robots_index = models.BooleanField(
        default=True,
        help_text="Allow search engines to index this page",
        verbose_name="Index Page"
    )
    
    robots_follow = models.BooleanField(
        default=True,
        help_text="Allow search engines to follow links on this page",
        verbose_name="Follow Links"
    )
    
    canonical_url = models.URLField(
        blank=True,
        null=True,
        help_text="Canonical URL for this page (optional)",
        verbose_name="Canonical URL"
    )
    
    # Analytics
    google_analytics_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Google Analytics tracking ID (e.g., GA_MEASUREMENT_ID)",
        verbose_name="Google Analytics ID"
    )
    
    facebook_pixel_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Facebook Pixel ID",
        verbose_name="Facebook Pixel ID"
    )
    
    class Meta:
        abstract = True
    
    @property
    def effective_seo_title(self):
        """Return SEO title using Wagtail's seo_title field or fallback to page title"""
        if hasattr(self, 'seo_title') and self.seo_title:
            return self.seo_title
        elif hasattr(self, 'title'):
            return self.title
        return "Sweet Bliss"
    
    @property
    def effective_meta_description(self):
        """Return meta description with fallbacks"""
        if self.meta_description:
            return self.meta_description
        elif hasattr(self, 'search_description') and self.search_description:
            return self.search_description
        # Try to generate from content if available
        if hasattr(self, 'body') and self.body:
            # Extract text from RichText field
            return str(self.body)[:160] + "..." if len(str(self.body)) > 160 else str(self.body)
        return "Sweet Bliss - Premium FMCG Distribution | Bringing Global Brands to Pakistan"
    
    @property
    def effective_og_title(self):
        """Return OG title with fallbacks"""
        if self.og_title:
            return self.og_title
        return self.effective_seo_title
    
    @property
    def effective_og_description(self):
        """Return OG description with fallbacks"""
        if self.og_description:
            return self.og_description
        return self.effective_meta_description
    
    @property
    def effective_twitter_title(self):
        """Return Twitter title with fallbacks"""
        if self.twitter_title:
            return self.twitter_title
        return self.effective_seo_title
    
    @property
    def effective_twitter_description(self):
        """Return Twitter description with fallbacks"""
        if self.twitter_description:
            return self.twitter_description
        return self.effective_meta_description
    
    @property
    def robots_tag(self):
        """Generate robots meta tag"""
        parts = []
        if self.robots_index:
            parts.append('index')
        else:
            parts.append('noindex')
        
        if self.robots_follow:
            parts.append('follow')
        else:
            parts.append('nofollow')
        
        return ', '.join(parts)
    
    # Wagtail admin panels
    seo_panels = [
        MultiFieldPanel([
            FieldPanel('meta_description'),
            FieldPanel('meta_keywords'),
        ], heading="Basic SEO"),
        
        MultiFieldPanel([
            FieldPanel('og_title'),
            FieldPanel('og_description'),
            FieldPanel('og_image'),
        ], heading="Open Graph (Facebook/LinkedIn)"),
        
        MultiFieldPanel([
            FieldPanel('twitter_title'),
            FieldPanel('twitter_description'),
            FieldPanel('twitter_image'),
        ], heading="Twitter Card"),
        
        MultiFieldPanel([
            FieldPanel('schema_type'),
            FieldPanel('canonical_url'),
        ], heading="Structured Data"),
        
        MultiFieldPanel([
            FieldPanel('robots_index'),
            FieldPanel('robots_follow'),
        ], heading="Search Engine Settings"),
        
        MultiFieldPanel([
            FieldPanel('google_analytics_id'),
            FieldPanel('facebook_pixel_id'),
        ], heading="Analytics & Tracking"),
    ]


@register_setting
class GlobalSEOSettings(BaseSiteSetting):
    """
    Global SEO settings that can be managed from Wagtail admin
    """
    # Site-wide settings
    site_name = models.CharField(
        max_length=100,
        default="Sweet Bliss",
        help_text="Your website name"
    )
    
    default_meta_description = models.TextField(
        max_length=160,
        default="Sweet Bliss - Premium FMCG Distribution | Bringing Global Brands to Pakistan",
        help_text="Default meta description for pages without custom description"
    )
    
    default_og_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Default image for social media sharing"
    )
    
    # Company information for schema.org
    company_name = models.CharField(
        max_length=100,
        default="Sweet Bliss",
        help_text="Official company name"
    )
    
    company_description = models.TextField(
        default="Premium FMCG Importer and Distributor - Connecting global brands with local markets across Pakistan",
        help_text="Company description for schema markup"
    )
    
    company_logo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Company logo for schema markup"
    )
    
    # Contact information
    phone = models.CharField(
        max_length=20,
        blank=True,
        default="+92-315-7680420",
        help_text="Company phone number"
    )
    
    email = models.EmailField(
        blank=True,
        default="azan@sweetbliss.pk",
        help_text="Company email address"
    )
    
    address = models.TextField(
        blank=True,
        default="Lahore, Punjab, Pakistan",
        help_text="Company address"
    )
    
    # Social media profiles
    facebook_url = models.URLField(blank=True, help_text="Facebook page URL")
    twitter_url = models.URLField(blank=True, help_text="Twitter profile URL")
    instagram_url = models.URLField(blank=True, help_text="Instagram profile URL")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    
    # Analytics
    google_analytics_id = models.CharField(
        max_length=20,
        blank=True,
        help_text="Google Analytics 4 Measurement ID (e.g., G-XXXXXXXXXX)"
    )
    
    google_tag_manager_id = models.CharField(
        max_length=20,
        blank=True,
        help_text="Google Tag Manager ID (e.g., GTM-XXXXXXX)"
    )
    
    facebook_pixel_id = models.CharField(
        max_length=20,
        blank=True,
        help_text="Facebook Pixel ID"
    )
    
    # Search Console
    google_site_verification = models.CharField(
        max_length=100,
        blank=True,
        help_text="Google Search Console verification code"
    )
    
    bing_site_verification = models.CharField(
        max_length=100,
        blank=True,
        help_text="Bing Webmaster Tools verification code"
    )
    
    class Meta:
        verbose_name = "Global SEO Settings"
    
    panels = [
        MultiFieldPanel([
            FieldPanel('site_name'),
            FieldPanel('default_meta_description'),
            FieldPanel('default_og_image'),
        ], heading="Site Information"),
        
        MultiFieldPanel([
            FieldPanel('company_name'),
            FieldPanel('company_description'),
            FieldPanel('company_logo'),
        ], heading="Company Information"),
        
        MultiFieldPanel([
            FieldPanel('phone'),
            FieldPanel('email'),
            FieldPanel('address'),
        ], heading="Contact Information"),
        
        MultiFieldPanel([
            FieldPanel('facebook_url'),
            FieldPanel('twitter_url'),
            FieldPanel('instagram_url'),
            FieldPanel('linkedin_url'),
        ], heading="Social Media"),
        
        MultiFieldPanel([
            FieldPanel('google_analytics_id'),
            FieldPanel('google_tag_manager_id'),
            FieldPanel('facebook_pixel_id'),
        ], heading="Analytics & Tracking"),
        
        MultiFieldPanel([
            FieldPanel('google_site_verification'),
            FieldPanel('bing_site_verification'),
        ], heading="Search Engine Verification"),
    ]


class RedirectRule(models.Model):
    """
    Custom redirect rules for SEO
    """
    old_path = models.CharField(
        max_length=255,
        unique=True,
        help_text="Old URL path (e.g., /old-page/)"
    )
    
    new_path = models.CharField(
        max_length=255,
        help_text="New URL path (e.g., /new-page/)"
    )
    
    redirect_type = models.CharField(
        max_length=3,
        choices=[
            ('301', '301 Permanent'),
            ('302', '302 Temporary'),
        ],
        default='301',
        help_text="Type of redirect"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Is this redirect active?"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Redirect Rule"
        verbose_name_plural = "Redirect Rules"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.old_path} → {self.new_path} ({self.redirect_type})"
    
    panels = [
        FieldPanel('old_path'),
        FieldPanel('new_path'),
        FieldPanel('redirect_type'),
        FieldPanel('is_active'),
    ]
