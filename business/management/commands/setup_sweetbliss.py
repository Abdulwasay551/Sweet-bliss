from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from wagtail.models import Page, Site
from business.models import (
    HomePage, AboutPage, ProductsPage, TeamPage, ContactPage,
    ServicesPage, PortfolioPage, PartnershipsPage,
    ProductCategory, Partner, Brand, Product, TeamMember
)
from seo.models import GlobalSEOSettings


class Command(BaseCommand):
    help = 'Set up initial Sweet Bliss website structure with SEO'

    def handle(self, *args, **options):
        self.stdout.write("Setting up Sweet Bliss website structure...")

        # First, let's ensure we have a proper root page structure
        from wagtail.models import Page
        
        # Check if we have the proper root structure
        try:
            root_page = Page.objects.get(depth=1)
        except Page.DoesNotExist:
            self.stdout.write(self.style.ERROR("Root page not found. Please run 'python manage.py migrate' first."))
            return
        except Page.MultipleObjectsReturned:
            # Multiple root pages, let's fix this
            root_pages = Page.objects.filter(depth=1)
            root_page = root_pages.first()
            # Clean up extra root pages
            for page in root_pages[1:]:
                page.delete()
            self.stdout.write("Cleaned up multiple root pages")

        # Check if we already have a homepage
        existing_home = HomePage.objects.first()
        if existing_home:
            self.stdout.write(self.style.SUCCESS("Homepage already exists. Skipping setup."))
            home_page = existing_home
        else:
            # Remove any existing default pages at depth=2
            default_pages = Page.objects.filter(depth=2)
            for page in default_pages:
                try:
                    page.delete()
                    self.stdout.write(f"Removed existing page: {page.title}")
                except Exception as e:
                    self.stdout.write(f"Could not remove {page.title}: {e}")

            # Create HomePage
            home_page = HomePage(
                title="Sweet Bliss - Premium FMCG Distribution",
                slug="home",
                hero_title="Sweet Bliss",
                hero_subtitle="Bringing Sweet Moments Closer to You",
                hero_description="At Sweet Bliss, we carefully source the finest confectionery brands from around the world, delivering premium FMCG products that create joy, flavor, and unforgettable experiences for customers across Pakistan.",
                seo_title="Sweet Bliss - Premium FMCG Distribution | Global Brands Pakistan",
                search_description="Premium FMCG Importer and Distributor in Pakistan. We bring global confectionery and beverage brands to local markets with quality assurance and reliable distribution.",
                meta_description="Sweet Bliss - Premium FMCG Distribution | Bringing Global Brands to Pakistan",
                meta_keywords="Sweet Bliss, FMCG, confectionery, distribution, Pakistan, global brands, Pringles, KitKat, Nestlé",
                schema_type="Website",
                show_in_menus=True,
                live=True
            )
            
            # Add to root page safely
            try:
                root_page.add_child(instance=home_page)
                # Publish the page
                home_page.save_revision().publish()
                self.stdout.write(self.style.SUCCESS("✓ Created HomePage"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to create homepage: {e}"))
                # Try alternative approach - create directly
                try:
                    home_page.path = root_page._get_next_child_path()
                    home_page.depth = root_page.depth + 1
                    home_page.save()
                    home_page.save_revision().publish()
                    self.stdout.write(self.style.SUCCESS("✓ Created HomePage (alternative method)"))
                except Exception as e2:
                    self.stdout.write(self.style.ERROR(f"Failed with alternative method too: {e2}"))
                    return

        # Update site to use new homepage
        try:
            site, created = Site.objects.get_or_create(
                is_default_site=True,
                defaults={
                    'hostname': 'localhost',
                    'port': 8000,
                    'site_name': 'Sweet Bliss',
                    'root_page': home_page
                }
            )
            
            if not created and site.root_page != home_page:
                site.root_page = home_page
                site.site_name = "Sweet Bliss"
                site.save()
                
            self.stdout.write(self.style.SUCCESS("✓ Updated site root page"))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Could not update site root: {e}"))

        # Create About Page
        if not AboutPage.objects.filter(slug='about').exists():
            about_page = AboutPage(
                title="About Sweet Bliss",
                slug="about",
                seo_title="About Sweet Bliss - FMCG Importer & Distributor Pakistan",
                search_description="Learn about Sweet Bliss, a leading FMCG importer and distributor in Pakistan specializing in premium confectionery and beverage brands.",
                meta_description="About Sweet Bliss - FMCG Importer and Distributor connecting global brands with local markets across Pakistan",
                schema_type="AboutPage",
                show_in_menus=True,
                introduction='<p>At Sweet Bliss, we are a leading <strong>FMCG Importer and Distributor</strong> specializing in premium confectionery and beverage products.</p>',
                mission_content='<p>At Sweet Bliss, our mission is to connect retailers and distributors with the world\'s most trusted confectionery and beverage brands. We believe in delivering not only high-quality products but also consistent value that strengthens our partners\' businesses and delights end consumers.</p>',
                vision_content='<p>We aim to become a leading name in global confectionery and beverage imports, recognized for our reliability, product variety, and ability to anticipate evolving market trends. By bridging global brands with local markets, we help our partners stay competitive and grow.</p>',
                values_content='<p>At Sweet Bliss, we specialize in importing and distributing premium FMCG and confectionery products. Our diverse portfolio includes chocolates, candies, gums, snacks, coffee, and beverages — carefully selected to meet the needs of supermarkets, retailers, and wholesalers across Pakistan.</p>'
            )
            home_page.add_child(instance=about_page)
            about_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS("✓ Created About Page"))

        # Create Products Page
        if not ProductsPage.objects.filter(slug='products').exists():
            products_page = ProductsPage(
                title="Products",
                slug="products",
                seo_title="Premium FMCG Products | Sweet Bliss Distribution Portfolio",
                search_description="Explore our premium FMCG product portfolio including global confectionery and beverage brands distributed across Pakistan.",
                meta_description="Premium FMCG Products - Chocolates, Snacks, Beverages, Coffee from global brands distributed by Sweet Bliss",
                schema_type="WebPage",
                show_in_menus=True,
                introduction='<p>Discover our comprehensive portfolio of premium FMCG products from globally recognized brands.</p>'
            )
            home_page.add_child(instance=products_page)
            products_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS("✓ Created Products Page"))

        # Create Team Page
        if not TeamPage.objects.filter(slug='team').exists():
            team_page = TeamPage(
                title="Our Team",
                slug="team",
                seo_title="Leadership Team | Sweet Bliss Management Pakistan",
                search_description="Meet the experienced leadership team behind Sweet Bliss, providing strategic direction for FMCG distribution across Pakistan.",
                meta_description="Meet the Sweet Bliss leadership team - experienced professionals in FMCG distribution and global brand management",
                schema_type="WebPage",
                show_in_menus=True,
                introduction='<p>Meet our experienced leadership team providing strategic direction and operational excellence in FMCG distribution.</p>'
            )
            home_page.add_child(instance=team_page)
            team_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS("✓ Created Team Page"))

        # Create Contact Page
        if not ContactPage.objects.filter(slug='contact').exists():
            contact_page = ContactPage(
                title="Contact Us",
                slug="contact",
                seo_title="Contact Sweet Bliss - FMCG Distribution Partnership Pakistan",
                search_description="Contact Sweet Bliss for wholesale inquiries, product information, and partnership opportunities in Pakistan FMCG distribution.",
                meta_description="Contact Sweet Bliss for FMCG wholesale partnerships - Phone: +92-315-7680420 | Email: azan@sweetbliss.pk | Lahore, Pakistan",
                schema_type="ContactPage",
                show_in_menus=True,
                introduction='<p>Ready to partner with Sweet Bliss? Let\'s build a successful business relationship together.</p>'
            )
            home_page.add_child(instance=contact_page)
            contact_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS("✓ Created Contact Page"))

        # Create Services Page
        if not ServicesPage.objects.filter(slug='services').exists():
            services_page = ServicesPage(
                title="Our Services",
                slug="services",
                seo_title="FMCG Distribution Services | Sweet Bliss Pakistan",
                search_description="Comprehensive FMCG distribution services including importing, wholesale distribution, and partnership opportunities across Pakistan.",
                meta_description="Professional FMCG Services - Importing, Distribution, Partnership | Sweet Bliss Pakistan",
                meta_keywords="FMCG services, importing services, distribution services, wholesale partnerships, Pakistan",
                schema_type="WebPage",
                show_in_menus=True,
                live=True,
                introduction='<p>Sweet Bliss provides comprehensive FMCG distribution services designed to connect global brands with local markets across Pakistan.</p>',
                importing_services='<h3>Premium Import Services</h3><p>We specialize in importing high-quality confectionery and beverage products from trusted global manufacturers, ensuring authenticity and freshness.</p><ul><li>Direct relationships with international suppliers</li><li>Quality assurance and compliance</li><li>Efficient customs clearance</li><li>Temperature-controlled storage</li></ul>',
                distribution_services='<h3>Reliable Distribution Network</h3><p>Our distribution network ensures your products reach retailers, supermarkets, and wholesalers efficiently across Pakistan.</p><ul><li>Strategic warehouse locations</li><li>Cold chain management</li><li>Last-mile delivery solutions</li><li>Inventory management systems</li></ul>',
                partnership_services='<h3>Strategic Business Partnerships</h3><p>We build lasting partnerships with retailers and distributors, providing ongoing support and value-added services.</p><ul><li>Business development support</li><li>Marketing and promotional assistance</li><li>Training and product knowledge</li><li>Flexible payment terms</li></ul>'
            )
            home_page.add_child(instance=services_page)
            services_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS("✓ Created Services Page"))

        # Create Portfolio Page
        if not PortfolioPage.objects.filter(slug='portfolio').exists():
            portfolio_page = PortfolioPage(
                title="Product Portfolio",
                slug="portfolio",
                seo_title="Premium FMCG Product Portfolio | Sweet Bliss Global Brands",
                search_description="Explore our comprehensive portfolio of premium FMCG products featuring global confectionery and beverage brands distributed across Pakistan.",
                meta_description="Premium Product Portfolio - Global Confectionery & Beverage Brands | Sweet Bliss",
                meta_keywords="product portfolio, global brands, confectionery products, beverage brands, FMCG catalogue",
                schema_type="WebPage",
                show_in_menus=True,
                live=True,
                introduction='<p>Discover our carefully curated portfolio of premium FMCG products from globally recognized brands, each selected for quality, market appeal, and consumer satisfaction.</p><p>Our diverse range includes chocolates, candies, snacks, beverages, coffee, and specialty items that meet the evolving demands of Pakistani consumers.</p>',
                quality_commitment='<h3>Our Quality Commitment</h3><p>Every product in our portfolio undergoes rigorous quality checks and is sourced directly from authorized manufacturers. We ensure:</p><ul><li>Authentic products with proper certifications</li><li>Fresh inventory with optimal shelf life</li><li>Proper storage and handling throughout the supply chain</li><li>Compliance with local and international quality standards</li></ul><p>At Sweet Bliss, our goal is not just to supply products — but to deliver solutions that drive sales, build customer loyalty, and strengthen your business.</p>'
            )
            home_page.add_child(instance=portfolio_page)
            portfolio_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS("✓ Created Portfolio Page"))

        # Create Partnerships Page
        if not PartnershipsPage.objects.filter(slug='partnerships').exists():
            partnerships_page = PartnershipsPage(
                title="Business Partnerships",
                slug="partnerships",
                seo_title="FMCG Business Partnerships | Sweet Bliss Distribution Partners",
                search_description="Join Sweet Bliss as a distribution partner. Comprehensive partnership opportunities for retailers, wholesalers, and distributors in Pakistan.",
                meta_description="Business Partnership Opportunities - FMCG Distribution | Sweet Bliss Pakistan",
                meta_keywords="business partnerships, distribution partners, wholesale opportunities, retailer partnerships, FMCG business",
                schema_type="WebPage",
                show_in_menus=True,
                live=True,
                introduction='<p>Partner with Sweet Bliss to unlock new business opportunities in Pakistan\'s growing FMCG market. We believe in building mutually beneficial relationships that drive growth and success.</p>',
                why_partner='<h3>Why Partner with Sweet Bliss?</h3><ul><li><strong>Proven Track Record:</strong> Established relationships with global suppliers and local markets</li><li><strong>Quality Assurance:</strong> Rigorous quality control and authentic products</li><li><strong>Market Knowledge:</strong> Deep understanding of Pakistani consumer preferences</li><li><strong>Operational Excellence:</strong> Efficient logistics and distribution network</li><li><strong>Business Support:</strong> Ongoing marketing, training, and business development assistance</li></ul>',
                partnership_benefits='<h3>Partnership Benefits</h3><ul><li>Access to premium international brands</li><li>Competitive pricing and flexible payment terms</li><li>Marketing and promotional support</li><li>Product training and knowledge sharing</li><li>Dedicated account management</li><li>Territory protection and exclusive opportunities</li><li>Business growth consultation</li></ul>',
                how_to_partner='<h3>How to Become a Partner</h3><p>Getting started with Sweet Bliss is simple:</p><ol><li><strong>Initial Consultation:</strong> Contact our team to discuss your business requirements</li><li><strong>Business Assessment:</strong> We evaluate mutual fit and partnership potential</li><li><strong>Partnership Agreement:</strong> Customized terms based on your market and requirements</li><li><strong>Onboarding:</strong> Product training, system setup, and launch support</li><li><strong>Ongoing Support:</strong> Continuous business development and growth assistance</li></ol><p>Ready to grow your business with Sweet Bliss? <a href="/contact/">Contact us today</a> to explore partnership opportunities.</p>'
            )
            home_page.add_child(instance=partnerships_page)
            partnerships_page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS("✓ Created Partnerships Page"))

        # Create Product Categories
        categories_data = [
            {"name": "Chocolates & Confectionery", "description": "Premium chocolate bars, candies, and sweet treats", "icon": "🍫"},
            {"name": "Snacks & Crisps", "description": "Quality snack foods and crispy treats", "icon": "🍟"},
            {"name": "Beverages & Drinks", "description": "Refreshing drinks and beverage products", "icon": "🥤"},
            {"name": "Coffee & Hot Beverages", "description": "Premium coffee and hot drink products", "icon": "☕"},
            {"name": "Gum & Chewing Products", "description": "Chewing gum and related products", "icon": "🍬"},
        ]

        for cat_data in categories_data:
            category, created = ProductCategory.objects.get_or_create(
                name=cat_data["name"],
                defaults={
                    "description": cat_data["description"],
                    "icon": cat_data["icon"]
                }
            )
            if created:
                self.stdout.write(f"✓ Created category: {category.name}")

        # Create Business Partners (Brands we Import from)
        partners_data = [
            {
                "name": "Nestlé",
                "description": "Global leader in nutrition, health and wellness with over 2000 brands worldwide",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Nestl%C3%A9_logo.svg/400px-Nestl%C3%A9_logo.svg.png",
                "website_url": "https://www.nestle.com",
                "country_of_origin": "Switzerland",
                "order": 1
            },
            {
                "name": "Mars Wrigley",
                "description": "Leading manufacturer of chocolate, chewing gum, mints, and fruity confections",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Mars_Wrigley_logo.svg/400px-Mars_Wrigley_logo.svg.png",
                "website_url": "https://www.mars.com",
                "country_of_origin": "United States",
                "order": 2
            },
            {
                "name": "Ferrero",
                "description": "Italian confectionery company known for premium chocolate products",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Ferrero_SpA_logo.svg/400px-Ferrero_SpA_logo.svg.png",
                "website_url": "https://www.ferrero.com",
                "country_of_origin": "Italy",
                "order": 3
            },
            {
                "name": "Perfetti Van Melle",
                "description": "Global manufacturer of confectionery and gum products",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Perfetti_Van_Melle_logo.svg/400px-Perfetti_Van_Melle_logo.svg.png",
                "website_url": "https://www.perfettivanmelle.com",
                "country_of_origin": "Netherlands",
                "order": 4
            },
            {
                "name": "Mondelez International",
                "description": "Leading snacking company with iconic global brands",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Mondelez_International_logo.svg/400px-Mondelez_International_logo.svg.png",
                "website_url": "https://www.mondelezinternational.com",
                "country_of_origin": "United States",
                "order": 5
            },
            {
                "name": "Kellanova",
                "description": "Global snacking, cereal and noodles company with beloved brands",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Kellanova_logo.svg/400px-Kellanova_logo.svg.png",
                "website_url": "https://www.kellanova.com",
                "country_of_origin": "United States",
                "order": 6
            },
            {
                "name": "JDE Peet's",
                "description": "World's leading pure-play coffee and tea company",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/JDE_Peet%27s_logo.svg/400px-JDE_Peet%27s_logo.svg.png",
                "website_url": "https://www.jdepeets.com",
                "country_of_origin": "Netherlands",
                "order": 7
            },
            {
                "name": "Aujan Coca-Cola Beverages",
                "description": "Leading beverage company in the Middle East and North Africa",
                "logo_url": "https://example.com/aujan-logo.png",
                "website_url": "https://www.aujancoca-cola.com",
                "country_of_origin": "UAE",
                "order": 8
            },
            {
                "name": "Bavaria N.V.",
                "description": "Premium non-alcoholic malt beverage company",
                "logo_url": "https://example.com/bavaria-logo.png",
                "website_url": "https://www.bavaria.com",
                "country_of_origin": "Netherlands",
                "order": 9
            }
        ]

        for partner_data in partners_data:
            partner, created = Partner.objects.get_or_create(
                name=partner_data["name"],
                defaults=partner_data
            )
            if created:
                self.stdout.write(f"✓ Created partner: {partner.name}")

        # Create Brands for specific products
        brands_data = [
            {"name": "Pringles", "description": "Premium stackable potato crisps", "country": "United States", "partner": "Kellanova"},
            {"name": "Jacobs Coffee", "description": "Rich, aromatic coffee blends", "country": "Germany", "partner": "JDE Peet's"},
            {"name": "Rani", "description": "Refreshing fruit juices and beverages", "country": "UAE", "partner": "Aujan Coca-Cola Beverages"},
            {"name": "Barbican", "description": "Premium non-alcoholic malt beverages", "country": "UAE", "partner": "Bavaria N.V."},
            {"name": "KitKat", "description": "Iconic chocolate wafer bars", "country": "United Kingdom", "partner": "Nestlé"},
            {"name": "Nutella", "description": "Premium hazelnut spread", "country": "Italy", "partner": "Ferrero"},
        ]

        for brand_data in brands_data:
            try:
                partner = Partner.objects.get(name=brand_data["partner"])
                brand, created = Brand.objects.get_or_create(
                    name=brand_data["name"],
                    defaults={
                        "description": brand_data["description"],
                        "country_of_origin": brand_data["country"],
                        "partner": partner
                    }
                )
                if created:
                    self.stdout.write(f"✓ Created brand: {brand.name}")
            except Partner.DoesNotExist:
                self.stdout.write(f"⚠ Partner {brand_data['partner']} not found for brand {brand_data['name']}")

        # Create Featured Products
        featured_products_data = [
            {
                "name": "Original",
                "description": "Classic Pringles Original flavor - crispy, stackable potato crisps",
                "brand": "Pringles",
                "category": "Snacks & Crisps",
                "image_url": "https://example.com/pringles-original.jpg",
                "slug": "pringles-original"
            },
            {
                "name": "Gold Instant Coffee",
                "description": "Premium instant coffee with rich, aromatic flavor",
                "brand": "Jacobs Coffee",
                "category": "Coffee & Hot Beverages",
                "image_url": "https://example.com/jacobs-gold.jpg",
                "slug": "jacobs-gold"
            },
            {
                "name": "Float Juice 250ml",
                "description": "Refreshing fruit juice drink with real fruit pieces",
                "brand": "Rani",
                "category": "Beverages & Drinks",
                "image_url": "https://example.com/rani-float.jpg",
                "slug": "rani-float-250ml"
            },
            {
                "name": "Rani Can 240ml",
                "description": "Premium fruit juice in convenient can packaging",
                "brand": "Rani",
                "category": "Beverages & Drinks",
                "image_url": "https://example.com/rani-can.jpg",
                "slug": "rani-can-240ml"
            },
            {
                "name": "Non-Alcoholic Malt Drink",
                "description": "Premium non-alcoholic malt beverage with natural ingredients",
                "brand": "Barbican",
                "category": "Beverages & Drinks",
                "image_url": "https://example.com/barbican-malt.jpg",
                "slug": "barbican-malt"
            },
            {
                "name": "4-Finger Bar",
                "description": "Iconic chocolate wafer bar - have a break, have a KitKat",
                "brand": "KitKat",
                "category": "Chocolates & Confectionery",
                "image_url": "https://example.com/kitkat-4finger.jpg",
                "slug": "kitkat-4finger"
            },
            {
                "name": "Hazelnut Spread 750g",
                "description": "Premium hazelnut spread with cocoa - perfect for breakfast",
                "brand": "Nutella",
                "category": "Chocolates & Confectionery",
                "image_url": "https://example.com/nutella-750g.jpg",
                "slug": "nutella-750g"
            }
        ]

        for product_data in featured_products_data:
            try:
                brand = Brand.objects.get(name=product_data["brand"])
                category = ProductCategory.objects.get(name=product_data["category"])
                
                product, created = Product.objects.get_or_create(
                    slug=product_data["slug"],
                    defaults={
                        "name": product_data["name"],
                        "description": product_data["description"],
                        "brand": brand,
                        "category": category,
                        "image_url": product_data["image_url"],
                        "is_featured": True,
                        "is_active": True
                    }
                )
                if created:
                    self.stdout.write(f"✓ Created featured product: {brand.name} {product.name}")
            except (Brand.DoesNotExist, ProductCategory.DoesNotExist) as e:
                self.stdout.write(f"⚠ Could not create product {product_data['name']}: {e}")

        # Create Team Members
        team_data = [
            {
                "name": "Sheraz Gulzar",
                "position": "Chief Executive Officer (CEO)",
                "bio": "Provides overall vision, strategic leadership, and direction to position Sweet Bliss as a trusted name in global confectionery and FMCG imports. Leading the company towards sustainable growth and market expansion.",
                "order": 1
            },
            {
                "name": "Azan Anwar", 
                "position": "Chief Operating Officer (COO)",
                "bio": "Responsible for operational efficiency, logistics, and supply chain management to ensure seamless distribution across markets. Focuses on process optimization and customer satisfaction.",
                "email": "azan@sweetbliss.pk",
                "order": 2
            },
            {
                "name": "Mowahid Hassan",
                "position": "Chief Operating Officer (COO)", 
                "bio": "Focuses on operational strategy, process improvement, and maintaining the highest standards of reliability and customer satisfaction. Ensures quality control and service excellence.",
                "order": 3
            }
        ]

        for member_data in team_data:
            member, created = TeamMember.objects.get_or_create(
                name=member_data["name"],
                defaults=member_data
            )
            if created:
                self.stdout.write(f"✓ Created team member: {member.name}")

        # Set up Global SEO Settings
        try:
            seo_settings = GlobalSEOSettings.for_site(Site.objects.get(is_default_site=True))
            seo_settings.site_name = "Sweet Bliss"
            seo_settings.company_name = "Sweet Bliss"
            seo_settings.company_description = "Premium FMCG Importer and Distributor - Connecting global brands with local markets across Pakistan"
            seo_settings.default_meta_description = "Sweet Bliss - Premium FMCG Distribution | Bringing Global Brands to Pakistan"
            seo_settings.phone = "+92-315-7680420"
            seo_settings.email = "azan@sweetbliss.pk"
            seo_settings.address = "Lahore, Punjab, Pakistan"
            seo_settings.save()
            self.stdout.write(self.style.SUCCESS("✓ Configured Global SEO Settings"))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Could not set SEO settings: {e}"))

        self.stdout.write(
            self.style.SUCCESS(
                "\n🎉 Sweet Bliss website structure created successfully!"
                "\n\nNext steps:"
                "\n1. Run: python manage.py runserver"
                "\n2. Visit: http://localhost:8000/admin/ (Django admin)"
                "\n3. Visit: http://localhost:8000/admin/ (Wagtail admin)"
                "\n4. Visit: http://localhost:8000/ (Homepage)"
                "\n\nLogin with your superuser credentials to manage content!"
            )
        )
