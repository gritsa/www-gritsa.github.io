# Gritsa Technologies Website - Jekyll Conversion Guide

## What Was Done

### 1. ✅ Fixed Asset Paths
- Moved all assets from `template/` to root:
  - `css/` - All stylesheets
  - `js/` - All JavaScript files
  - `images/` - All images and graphics  
  - `webfonts/` - Web fonts
- Updated all HTML files to reference assets correctly

### 2. ✅ Created Jekyll Structure
```
├── _config.yml          # Site configuration
├── _includes/           # Reusable components
│   ├── head.html       # HTML head with meta tags, CSS
│   ├── header.html     # Navigation menu (standardized)
│   ├── footer.html     # Footer with contact info
│   └── scripts.html    # JavaScript includes
├── _layouts/            # Page templates
│   ├── default.html    # Base layout
│   └── page.html       # Page with header/breadcrumb
├── _data/              # Data files (empty for now)
├── Gemfile             # Ruby dependencies
└── README.md           # Documentation
```

### 3. ✅ Standardized Navigation
Created a single navigation menu in `_includes/header.html` that will be used across all pages with proper links:
- Home: `/`
- About: `/about/`
- Services: `/services/` (with submenu)
- Projects: `/projects/`
- Blog: `/blog/`
- Contact: `/contact/`

## Next Steps to Complete Jekyll Migration

### Option 1: Quick Fix (Keep Current HTML)
The current site works now with fixed paths. You can use it as-is with the Python server:
```bash
cd /Users/abidev/dev/gritsa
python3 -m http.server 8000
```

### Option 2: Complete Jekyll Migration

#### Step 1: Install Jekyll
```bash
# Install bundler if not installed
gem install bundler

# Install Jekyll and dependencies
cd /Users/abidev/dev/gritsa
bundle install
```

#### Step 2: Convert HTML Pages to Use Layouts

Each page needs Jekyll front matter added at the top. Example for `about/index.html`:

**Before:**
```html
<!DOCTYPE html>
<html lang="zxx">
<head>
...entire HTML...
</body>
</html>
```

**After:**
```html
---
layout: page
title: About Us
description: Learn about Gritsa Technologies
---

<!-- Only the main content section -->
<div class="about-section">
  ...content only...
</div>
```

#### Step 3: Run Jekyll Server
```bash
bundle exec jekyll serve
```

Visit: http://localhost:4000

## Benefits of Jekyll

1. **DRY (Don't Repeat Yourself)**: Header/footer/nav defined once in `_includes/`
2. **Easy Updates**: Change navigation in one place, updates everywhere
3. **Data-Driven**: Store content in YAML files
4. **Blog-Ready**: Built-in blog functionality
5. **GitHub Pages**: Free hosting option

## Current Status

✅ Assets moved and paths fixed
✅ Jekyll structure created  
✅ Navigation standardized
⏳ Pages still need front matter conversion
⏳ Need to extract content from full HTML pages

## Files Ready to Use

- **_config.yml**: Site configuration with Gritsa info
- **_includes/header.html**: Standard navigation menu
- **_includes/footer.html**: Footer with Gritsa contact info
- **_layouts/default.html**: Base page template
- **Gemfile**: Jekyll dependencies

## To Test Current Setup (Without Jekyll)

```bash
cd /Users/abidev/dev/gritsa
python3 -m http.server 8000
```

Then visit:
- http://localhost:8000/ (Home)
- http://localhost:8000/about/ (About)
- http://localhost:8000/services/ (Services)
- http://localhost:8000/contact/ (Contact)

All navigation links should work and all pages should have Gritsa branding!
