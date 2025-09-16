# Sweet Bliss API Documentation

## Overview

Sweet Bliss provides a REST API for accessing product, brand, and category information. This API is built using Django REST Framework and can be used for mobile apps, integrations, or headless implementations.

## Base URL

```
Local Development: http://localhost:8000/api/
Production: https://yourdomain.com/api/
```

## Authentication

Currently, the API endpoints are publicly accessible for read operations. For future write operations, authentication will be required.

## Endpoints

### Products

#### GET /api/products/
List all active products with filtering and search capabilities.

**Parameters:**
- `search` (optional): Search products by name or description
- `brand` (optional): Filter by brand ID
- `category` (optional): Filter by category ID
- `is_featured` (optional): Filter featured products (true/false)

**Response:**
```json
{
  "count": 25,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Original",
      "description": "Classic Pringles Original flavor - crispy, stackable potato crisps",
      "brand": "Pringles",
      "category": "Snacks & Crisps",
      "slug": "pringles-original",
      "is_featured": true,
      "image_url": "https://example.com/pringles-original.jpg",
      "specifications": {}
    }
  ]
}
```

#### GET /api/products/{id}/
Get a specific product by ID.

**Response:**
```json
{
  "id": 1,
  "name": "Original",
  "description": "Classic Pringles Original flavor - crispy, stackable potato crisps",
  "brand": "Pringles",
  "category": "Snacks & Crisps",
  "slug": "pringles-original",
  "is_featured": true,
  "image_url": "https://example.com/pringles-original.jpg",
  "specifications": {}
}
```

### Brands

#### GET /api/brands/
List all brands.

**Response:**
```json
{
  "count": 6,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Pringles",
      "description": "Premium stackable potato crisps",
      "logo_url": "https://example.com/pringles-logo.png",
      "country_of_origin": "United States",
      "partner": "Kellanova"
    }
  ]
}
```

#### GET /api/brands/{id}/
Get a specific brand by ID.

### Categories

#### GET /api/categories/
List all product categories.

**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Chocolates & Confectionery",
      "description": "Premium chocolate bars, candies, and sweet treats",
      "icon": "🍫"
    }
  ]
}
```

#### GET /api/categories/{id}/
Get a specific category by ID.

### Search

#### GET /api/search/
Advanced product search with multiple filters.

**Parameters:**
- `q` (required): Search query
- `category` (optional): Category filter
- `brand` (optional): Brand filter
- `limit` (optional): Number of results (default: 10)

**Response:**
```json
{
  "query": "chocolate",
  "count": 5,
  "results": [
    {
      "id": 6,
      "name": "4-Finger Bar",
      "description": "Iconic chocolate wafer bar - have a break, have a KitKat",
      "brand": "KitKat",
      "category": "Chocolates & Confectionery",
      "slug": "kitkat-4finger",
      "is_featured": true
    }
  ]
}
```

### Contact Form

#### POST /api/contact/
Submit a contact form inquiry.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "company": "ABC Retailers",
  "phone": "+92-300-1234567",
  "subject": "Wholesale Inquiry",
  "message": "I'm interested in becoming a distributor for your products.",
  "inquiry_type": "wholesale"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Thank you for your inquiry. We'll get back to you soon!"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request",
  "details": "Missing required field: email"
}
```

### 404 Not Found
```json
{
  "error": "Not found",
  "details": "Product with ID 999 does not exist"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "details": "Please try again later"
}
```

## Rate Limiting

Current rate limits:
- 100 requests per minute per IP address
- Contact form: 5 submissions per hour per IP address

## Examples

### JavaScript (Fetch API)

```javascript
// Get featured products
fetch('/api/products/?is_featured=true')
  .then(response => response.json())
  .then(data => {
    console.log('Featured products:', data.results);
  });

// Search for chocolate products
fetch('/api/search/?q=chocolate&category=1')
  .then(response => response.json())
  .then(data => {
    console.log('Search results:', data.results);
  });

// Submit contact form
fetch('/api/contact/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken')
  },
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.com',
    message: 'Interested in wholesale partnership'
  })
})
.then(response => response.json())
.then(data => {
  console.log('Form submitted:', data);
});
```

### Python (Requests)

```python
import requests

# Get all brands
response = requests.get('http://localhost:8000/api/brands/')
brands = response.json()['results']

# Search products
params = {'q': 'coffee', 'limit': 5}
response = requests.get('http://localhost:8000/api/search/', params=params)
products = response.json()['results']

# Submit contact form
contact_data = {
    'name': 'Jane Smith',
    'email': 'jane@company.com',
    'message': 'Partnership inquiry'
}
response = requests.post('http://localhost:8000/api/contact/', json=contact_data)
result = response.json()
```

### cURL

```bash
# Get featured products
curl "http://localhost:8000/api/products/?is_featured=true"

# Get specific product
curl "http://localhost:8000/api/products/1/"

# Search products
curl "http://localhost:8000/api/search/?q=chocolate&limit=5"

# Submit contact form
curl -X POST "http://localhost:8000/api/contact/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "message": "API test message"
  }'
```

## Pagination

API endpoints that return multiple items are paginated:

```json
{
  "count": 25,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [....]
}
```

Use the `next` and `previous` URLs to navigate through pages.

## Future Enhancements

Planned API improvements:
- Authentication for admin operations
- Webhook support for real-time updates
- GraphQL endpoint for flexible queries
- File upload endpoints for product images
- Bulk operations for product management

## Support

For API support and questions:
- **Technical Issues**: Create a GitHub issue
- **Business Inquiries**: Contact azan@sweetbliss.pk
- **Documentation**: Check the main README.md

---

*API Version: 1.0 | Last Updated: September 2025*