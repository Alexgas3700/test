# Email Template Variables

This document describes all variables used in the discount offer email template.

## Available Variables

### Customer Information

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `{{FIRST_NAME}}` | Customer's first name | "Иван" | Yes |
| `{{EMAIL}}` | Customer's email address | "ivan@example.com" | Yes |
| `{{COMPANY_NAME}}` | Customer's company name | "ТехСтарт" | Yes |

### Discount Information

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `{{DISCOUNT_CODE}}` | Unique discount code | "NEWBIZ0210-5678" | Yes |
| `{{DISCOUNT_AMOUNT}}` | Discount percentage | "25" or "20" | Yes |
| `{{OFFER_EXPIRES}}` | Expiration date | "February 24, 2026" | Yes |

### URLs

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `{{LANDING_PAGE_URL}}` | Landing page for claiming offer | "https://yourcompany.com/claim-offer" | Yes |
| `{{UNSUBSCRIBE_URL}}` | Unsubscribe page URL | "https://yourcompany.com/unsubscribe" | Yes |
| `{{PRIVACY_URL}}` | Privacy policy page URL | "https://yourcompany.com/privacy" | Yes |

## Variable Mapping in n8n

These variables are automatically populated by the n8n workflow in the "Prepare Email Data" node:

```javascript
// Customer data from database
first_name: {{ $json.first_name || 'Entrepreneur' }}
email: {{ $json.email }}
company_name: {{ $json.company_name || 'your business' }}

// Generated discount data
discount_code: {{ 'NEWBIZ' + $now.format('MMDD') + '-' + $json.id.toString().slice(-4).toUpperCase() }}
discount_amount: {{ $json.industry === 'tech' ? '25' : '20' }}
offer_expires: {{ $now.plus(14, 'days').format('MMMM dd, yyyy') }}

// URLs from environment variables
landing_page_url: {{ $env.LANDING_PAGE_URL || 'https://yourcompany.com/claim-offer' }}
unsubscribe_url: {{ $env.UNSUBSCRIBE_URL || 'https://yourcompany.com/unsubscribe' }}
privacy_url: {{ $env.PRIVACY_URL || 'https://yourcompany.com/privacy' }}
```

## Customization Guide

### Changing Discount Logic

To modify how discounts are calculated, edit the `discount_amount` assignment in the "Prepare Email Data" node:

```javascript
// Current logic: 25% for tech, 20% for others
discount_amount: {{ $json.industry === 'tech' ? '25' : '20' }}

// Example: Tiered by company size
discount_amount: {{ $json.company_size > 50 ? '30' : $json.company_size > 10 ? '25' : '20' }}

// Example: By region
discount_amount: {{ ['moscow', 'saint_petersburg'].includes($json.region) ? '25' : '20' }}

// Example: Fixed discount
discount_amount: '20'
```

### Changing Discount Code Format

To modify the discount code format, edit the `discount_code` assignment:

```javascript
// Current format: NEWBIZ0210-5678
'NEWBIZ' + $now.format('MMDD') + '-' + $json.id.toString().slice(-4).toUpperCase()

// Example: Include company name
$json.company_name.toUpperCase().slice(0, 6) + '-' + $now.format('YYYY')

// Example: Random code
'PROMO-' + Math.random().toString(36).substring(2, 8).toUpperCase()

// Example: Sequential with date
'ENT' + $now.format('YYYYMMDD') + '-' + $json.id
```

### Changing Offer Duration

To modify how long the offer is valid, edit the `offer_expires` assignment:

```javascript
// Current: 14 days
$now.plus(14, 'days').format('MMMM dd, yyyy')

// Example: 7 days
$now.plus(7, 'days').format('MMMM dd, yyyy')

// Example: 30 days
$now.plus(30, 'days').format('MMMM dd, yyyy')

// Example: End of current month
$now.endOf('month').format('MMMM dd, yyyy')

// Example: Specific date
'December 31, 2026'
```

## Template Customization

### Changing Colors

The template uses a purple gradient color scheme. To change colors, modify these CSS variables:

```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Change to blue gradient */
background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);

/* Change to green gradient */
background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);

/* Change to orange gradient */
background: linear-gradient(135deg, #f46b45 0%, #eea849 100%);
```

### Adding Your Logo

To add a company logo, insert this code in the header section:

```html
<div class="header">
  <img src="https://yourcompany.com/logo.png" alt="Company Logo" style="max-width: 200px; margin-bottom: 20px;">
  <span class="emoji">🚀</span>
  <h1>Специальное предложение для предпринимателей!</h1>
</div>
```

### Changing Language

To translate the template to another language, replace all Russian text with your target language. Make sure to update:

1. All heading text
2. All body paragraphs
3. Button text
4. Footer text
5. Date format in the `offer_expires` variable

### Adding More Benefits

To add more benefit items, copy this HTML structure:

```html
<div class="benefit-item">Your new benefit text here</div>
```

### Customizing the CTA Button

To change the call-to-action button:

```html
<!-- Current -->
<a href="{{LANDING_PAGE_URL}}?code={{DISCOUNT_CODE}}" class="cta-button">
  Получить скидку сейчас
</a>

<!-- With icon -->
<a href="{{LANDING_PAGE_URL}}?code={{DISCOUNT_CODE}}" class="cta-button">
  🎁 Получить скидку сейчас
</a>

<!-- Different text -->
<a href="{{LANDING_PAGE_URL}}?code={{DISCOUNT_CODE}}" class="cta-button">
  Активировать промокод
</a>
```

## Testing Variables

Before sending to real customers, test the template with sample data:

```json
{
  "FIRST_NAME": "Тест",
  "EMAIL": "test@example.com",
  "COMPANY_NAME": "Тестовая Компания",
  "DISCOUNT_CODE": "TEST0210-1234",
  "DISCOUNT_AMOUNT": "25",
  "OFFER_EXPIRES": "February 24, 2026",
  "LANDING_PAGE_URL": "https://yourcompany.com/claim-offer",
  "UNSUBSCRIBE_URL": "https://yourcompany.com/unsubscribe",
  "PRIVACY_URL": "https://yourcompany.com/privacy"
}
```

## Best Practices

1. **Always test emails** before sending to customers
2. **Use fallback values** for optional variables (e.g., `{{ $json.first_name || 'Entrepreneur' }}`)
3. **Keep subject lines under 50 characters** for better open rates
4. **Use clear CTAs** with action-oriented text
5. **Include unsubscribe link** in every email (legal requirement)
6. **Test on multiple email clients** (Gmail, Outlook, Apple Mail, etc.)
7. **Use alt text for images** for accessibility
8. **Keep file size under 100KB** for faster loading
9. **Use responsive design** for mobile devices
10. **Personalize when possible** using customer data

## Troubleshooting

### Variables not replacing

**Problem**: Variables show as `{{VARIABLE_NAME}}` in sent emails

**Solution**: 
- Check that variables are correctly mapped in the "Prepare Email Data" node
- Ensure variable names match exactly (case-sensitive)
- Verify that the email template uses the correct variable syntax

### Formatting issues

**Problem**: Email looks broken in certain email clients

**Solution**:
- Use inline CSS instead of external stylesheets
- Test with Email on Acid or Litmus
- Use table-based layouts for better compatibility
- Avoid using JavaScript in emails

### Images not loading

**Problem**: Images don't appear in the email

**Solution**:
- Use absolute URLs (https://) for all images
- Host images on a reliable CDN
- Include alt text for accessibility
- Check that images are publicly accessible

## Support

For questions about template customization:
- Check the n8n documentation
- Visit the n8n community forum
- Review HTML email best practices
