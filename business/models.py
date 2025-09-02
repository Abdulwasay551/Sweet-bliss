from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import (
    FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
)
from wagtail.images.models import Image
from wagtail.images import get_image_model_string
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from django.core.validators import RegexValidator
from django.utils.functional import cached_property
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from seo.models import SEOMixin


# Custom blocks for flexible content
class HeroBlock(blocks.StructBlock):
    """Hero section block"""
    title = blocks.CharBlock(max_length=100, help_text="Main hero title")
    subtitle = blocks.TextBlock(help_text="Hero subtitle")
    description = blocks.TextBlock(help_text="Hero description")
    background_image = ImageChooserBlock(help_text="Hero background image")
    cta_text = blocks.CharBlock(max_length=50, help_text="Call to action button text")
    cta_link = blocks.PageChooserBlock(help_text="Call to action link")
    
    class Meta:
        template = "blocks/hero_block.html"
        icon = "image"
        label = "Hero Section"


class ProductBlock(blocks.StructBlock):
    """Product showcase block"""
    title = blocks.CharBlock(max_length=100, help_text="Product title")
    description = blocks.TextBlock(help_text="Product description")
    image = ImageChooserBlock(help_text="Product image")
    brand_logo = ImageChooserBlock(help_text="Brand logo")
    category = blocks.CharBlock(max_length=50, help_text="Product category")
    features = blocks.ListBlock(blocks.CharBlock(max_length=100), help_text="Product features")
    
    class Meta:
        template = "blocks/product_block.html"
        icon = "pick"
        label = "Product Showcase"


class TeamMemberBlock(blocks.StructBlock):
    """Team member block"""
    name = blocks.CharBlock(max_length=100, help_text="Team member name")
    position = blocks.CharBlock(max_length=100, help_text="Job position")
    bio = blocks.TextBlock(help_text="Short biography")
    photo = ImageChooserBlock(required=False, help_text="Team member photo")
    
    class Meta:
        template = "blocks/team_member_block.html"
        icon = "user"
        label = "Team Member"


class FeatureBlock(blocks.StructBlock):
    """Feature/Service block"""
    title = blocks.CharBlock(max_length=100, help_text="Feature title")
    description = blocks.TextBlock(help_text="Feature description")
    icon = blocks.CharBlock(max_length=50, help_text="Icon class or emoji")
    
    class Meta:
        template = "blocks/feature_block.html"
        icon = "cogs"
        label = "Feature/Service"


class ContactBlock(blocks.StructBlock):
    """Contact information block"""
    title = blocks.CharBlock(max_length=100, help_text="Contact section title")
    description = blocks.TextBlock(help_text="Contact description")
    phone = blocks.CharBlock(max_length=20, help_text="Phone number")
    email = blocks.EmailBlock(help_text="Email address")
    address = blocks.TextBlock(help_text="Physical address")
    
    class Meta:
        template = "blocks/contact_block.html"
        icon = "mail"
        label = "Contact Information"


@register_snippet
class ProductCategory(models.Model):
    """Product categories for organization"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or emoji")
    
    class Meta:
        verbose_name_plural = "Product Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('icon'),
    ]


@register_snippet
class Brand(models.Model):
    """Brand information"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    logo = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.CASCADE,
        related_name='+',
        null=True,
        blank=True
    )
    website_url = models.URLField(blank=True)
    country_of_origin = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('logo'),
        FieldPanel('website_url'),
        FieldPanel('country_of_origin'),
    ]


@register_snippet
class Product(index.Indexed, models.Model):
    """Individual products"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.CASCADE,
        related_name='+',
        null=True,
        blank=True
    )
    
    # Product specifications
    specifications = models.JSONField(default=dict, blank=True)
    
    # SEO fields
    slug = models.SlugField(max_length=255, unique=True)
    
    # Status
    is_featured = models.BooleanField(default=False, help_text="Display on homepage")
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    search_fields = [
        index.SearchField('name', partial_match=True, boost=10),
        index.SearchField('description'),
        index.FilterField('category'),
        index.FilterField('brand'),
        index.FilterField('is_featured'),
        index.FilterField('is_active'),
    ]
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.brand.name} - {self.name}"
    
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
        FieldPanel('category'),
        FieldPanel('brand'),
        FieldPanel('image'),
        FieldPanel('specifications'),
        MultiFieldPanel([
            FieldPanel('is_featured'),
            FieldPanel('is_active'),
        ], heading="Status"),
    ]


class TeamMember(models.Model):
    """Team member information"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.CASCADE,
        related_name='+',
        null=True,
        blank=True
    )
    
    # Contact information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Social links
    linkedin_url = models.URLField(blank=True)
    
    # Display order
    order = models.PositiveIntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.position}"


# Wagtail Page Models
class HomePage(SEOMixin, Page):
    """Homepage with dynamic content blocks"""
    
    # Hero section
    hero_title = models.CharField(max_length=200, default="Sweet Bliss")
    hero_subtitle = models.CharField(max_length=300, default="Bringing Sweet Moments Closer to You")
    hero_description = models.TextField(
        default="At Sweet Bliss, we carefully source the finest confectionery brands from around the world, delivering premium FMCG products that create joy, flavor, and unforgettable experiences for customers across Pakistan."
    )
    hero_background = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
        blank=True,
        help_text="Hero background image"
    )
    
    # Content sections using StreamField
    content_sections = StreamField([
        ('hero', HeroBlock()),
        ('products', ProductBlock()),
        ('features', FeatureBlock()),
        ('team_members', TeamMemberBlock()),
        ('contact', ContactBlock()),
    ], blank=True, use_json_field=True)
    
    # Featured content
    featured_products = models.ManyToManyField(
        Product,
        blank=True,
        help_text="Products to feature on homepage"
    )
    
    search_fields = Page.search_fields + [
        index.SearchField('hero_title', boost=10),
        index.SearchField('hero_subtitle'),
        index.SearchField('hero_description'),
        index.SearchField('content_sections'),
    ]
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_description'),
            FieldPanel('hero_background'),
        ], heading="Hero Section"),
        
        FieldPanel('content_sections'),
        FieldPanel('featured_products'),
    ]
    
    promote_panels = Page.promote_panels + SEOMixin.seo_panels
    
    class Meta:
        verbose_name = "Home Page"
    
    def get_context(self, request):
        context = super().get_context(request)
        
        # Add featured products to context
        context['featured_products'] = Product.objects.filter(
            is_featured=True,
            is_active=True
        ).select_related('brand', 'category')[:6]
        
        # Add team members
        context['team_members'] = TeamMember.objects.filter(
            is_active=True
        )[:3]
        
        return context


class AboutPage(SEOMixin, Page):
    """About us page"""
    
    introduction = RichTextField(
        blank=True,
        features=['h2', 'h3', 'bold', 'italic', 'link', 'ol', 'ul']
    )
    
    mission_title = models.CharField(max_length=100, default="Our Mission")
    mission_content = RichTextField(
        blank=True,
        features=['bold', 'italic', 'link', 'ol', 'ul']
    )
    
    vision_title = models.CharField(max_length=100, default="Our Vision")
    vision_content = RichTextField(
        blank=True,
        features=['bold', 'italic', 'link', 'ol', 'ul']
    )
    
    values_title = models.CharField(max_length=100, default="What We Do")
    values_content = RichTextField(
        blank=True,
        features=['bold', 'italic', 'link', 'ol', 'ul']
    )
    
    company_image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
        blank=True,
        help_text="Company image or office photo"
    )
    
    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('mission_content'),
        index.SearchField('vision_content'),
        index.SearchField('values_content'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        FieldPanel('company_image'),
        
        MultiFieldPanel([
            FieldPanel('mission_title'),
            FieldPanel('mission_content'),
        ], heading="Mission"),
        
        MultiFieldPanel([
            FieldPanel('vision_title'),
            FieldPanel('vision_content'),
        ], heading="Vision"),
        
        MultiFieldPanel([
            FieldPanel('values_title'),
            FieldPanel('values_content'),
        ], heading="What We Do"),
        
        InlinePanel('about_features', label="Features/Services"),
    ]
    
    promote_panels = Page.promote_panels + SEOMixin.seo_panels
    
    def get_context(self, request):
        context = super().get_context(request)
        
        # Add team members
        context['team_members'] = TeamMember.objects.filter(is_active=True)
        
        # Add global brands
        context['brands'] = Brand.objects.all()[:9]
        
        return context


class AboutPageFeature(Orderable):
    """Features for about page"""
    page = ParentalKey(AboutPage, on_delete=models.CASCADE, related_name='about_features')
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or emoji")
    
    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('icon'),
    ]


class ProductsPage(SEOMixin, Page):
    """Products listing page"""
    
    introduction = RichTextField(
        blank=True,
        features=['h2', 'h3', 'bold', 'italic', 'link']
    )
    
    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
    ]
    
    promote_panels = Page.promote_panels + SEOMixin.seo_panels
    
    def get_context(self, request):
        context = super().get_context(request)
        
        # Get all categories
        context['categories'] = ProductCategory.objects.all()
        
        # Get products by category
        category_slug = request.GET.get('category')
        if category_slug:
            try:
                category = ProductCategory.objects.get(name__iexact=category_slug)
                products = Product.objects.filter(
                    category=category,
                    is_active=True
                ).select_related('brand', 'category')
                context['selected_category'] = category
            except ProductCategory.DoesNotExist:
                products = Product.objects.filter(
                    is_active=True
                ).select_related('brand', 'category')
        else:
            products = Product.objects.filter(
                is_active=True
            ).select_related('brand', 'category')
        
        context['products'] = products
        context['brands'] = Brand.objects.all()
        
        return context


class ContactPage(SEOMixin, Page):
    """Contact page"""
    
    introduction = RichTextField(
        blank=True,
        features=['h2', 'h3', 'bold', 'italic', 'link']
    )
    
    # Contact information
    phone = models.CharField(max_length=20, default="+92-315-7680420")
    email = models.EmailField(default="azan@sweetbliss.pk")
    address = models.TextField(default="Lahore, Punjab, Pakistan")
    
    # Business hours
    business_hours = RichTextField(
        blank=True,
        features=['bold', 'italic']
    )
    
    # Map embed
    map_embed_code = models.TextField(
        blank=True,
        help_text="Google Maps embed code"
    )
    
    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('address'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        
        MultiFieldPanel([
            FieldPanel('phone'),
            FieldPanel('email'),
            FieldPanel('address'),
            FieldPanel('business_hours'),
        ], heading="Contact Information"),
        
        FieldPanel('map_embed_code'),
    ]
    
    promote_panels = Page.promote_panels + SEOMixin.seo_panels


class TeamPage(SEOMixin, Page):
    """Team page"""
    
    introduction = RichTextField(
        blank=True,
        features=['h2', 'h3', 'bold', 'italic', 'link']
    )
    
    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
    ]
    
    promote_panels = Page.promote_panels + SEOMixin.seo_panels
    
    def get_context(self, request):
        context = super().get_context(request)
        
        # Add all team members
        context['team_members'] = TeamMember.objects.filter(is_active=True)
        
        return context


class ServicesPage(SEOMixin, Page):
    """Services page showcasing what Sweet Bliss offers"""
    
    introduction = RichTextField(
        blank=True,
        help_text="Introduction to services",
        features=['h2', 'h3', 'bold', 'italic', 'link', 'ul', 'ol']
    )
    
    importing_services = RichTextField(
        blank=True,
        help_text="Importing services description",
        features=['h2', 'h3', 'bold', 'italic', 'link', 'ul', 'ol']
    )
    
    distribution_services = RichTextField(
        blank=True,
        help_text="Distribution services description",
        features=['h2', 'h3', 'bold', 'italic', 'link', 'ul', 'ol']
    )
    
    partnership_services = RichTextField(
        blank=True,
        help_text="Partnership services description",
        features=['h2', 'h3', 'bold', 'italic', 'link', 'ul', 'ol']
    )
    
    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('importing_services'),
        index.SearchField('distribution_services'),
        index.SearchField('partnership_services'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        MultiFieldPanel([
            FieldPanel('importing_services'),
            FieldPanel('distribution_services'),
            FieldPanel('partnership_services'),
        ], heading="Service Details"),
    ]
    
    promote_panels = Page.promote_panels + SEOMixin.seo_panels


class PortfolioPage(SEOMixin, Page):
    """Portfolio page showcasing product categories and brands"""
    
    introduction = RichTextField(
        blank=True,
        help_text="Portfolio overview introduction",
        features=['h2', 'h3', 'bold', 'italic', 'link', 'ul', 'ol']
    )
    
    quality_commitment = RichTextField(
        blank=True,
        help_text="Quality commitment statement",
        features=['h2', 'h3', 'bold', 'italic', 'link', 'ul', 'ol']
    )
    
    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('quality_commitment'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        FieldPanel('quality_commitment'),
    ]
    
    promote_panels = Page.promote_panels + SEOMixin.seo_panels
    
    def get_context(self, request):
        context = super().get_context(request)
        
        # Add categories and brands
        context['categories'] = ProductCategory.objects.all()
        context['brands'] = Brand.objects.all()
        
        return context


class PartnershipsPage(SEOMixin, Page):
    """Partnerships page for potential business partners"""
    
    introduction = RichTextField(
        blank=True,
        help_text="Partnership opportunities introduction",
        features=['h2', 'h3', 'bold', 'italic', 'link', 'ul', 'ol']
    )
    
    why_partner = RichTextField(
        blank=True,
        help_text="Why partner with Sweet Bliss",
        features=['h2', 'h3', 'bold', 'italic', 'link', 'ul', 'ol']
    )
    
    partnership_benefits = RichTextField(
        blank=True,
        help_text="Partnership benefits and advantages",
        features=['h2', 'h3', 'bold', 'italic', 'link', 'ul', 'ol']
    )
    
    how_to_partner = RichTextField(
        blank=True,
        help_text="How to become a partner",
        features=['h2', 'h3', 'bold', 'italic', 'link', 'ul', 'ol']
    )
    
    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('why_partner'),
        index.SearchField('partnership_benefits'),
        index.SearchField('how_to_partner'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        MultiFieldPanel([
            FieldPanel('why_partner'),
            FieldPanel('partnership_benefits'),
            FieldPanel('how_to_partner'),
        ], heading="Partnership Information"),
    ]
    
    promote_panels = Page.promote_panels + SEOMixin.seo_panels
