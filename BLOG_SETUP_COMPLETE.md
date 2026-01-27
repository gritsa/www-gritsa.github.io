# DecapCMS Blog Setup - Quick Start Guide

## ✅ What's Been Completed

### 1. DecapCMS Admin Interface
- **Location:** `/admin/`
- **Files Created:**
  - `admin/index.html` - DecapCMS interface (CDN-based, no npm needed)
  - `admin/config.yml` - Configuration with test-repo backend
  - `admin/README.md` - Detailed documentation

### 2. Blog Infrastructure
- **Directories Created:**
  - `_posts/` - Where blog post markdown files are stored
  - `images/blog/` - Where uploaded images are stored
  - `admin/` - DecapCMS admin interface

### 3. Templates & Layouts
- **Created:**
  - `_layouts/post.html` - Individual blog post template with:
    - Page header with breadcrumbs
    - Post metadata (author, date, tags)
    - Featured image display
    - Content area
    - Post navigation (prev/next)

### 4. Blog Index Page
- **Updated:** `blog/index.html`
  - Replaced hardcoded posts with Jekyll `site.posts` loop
  - Dynamically renders all posts from `_posts/` directory
  - Shows featured images, titles, excerpts
  - Includes "no posts" message when empty

### 5. Sample Content
- **Created:** `_posts/2026-01-27-welcome-to-gritsa-blog.md`
  - Welcome post introducing the blog
  - Covers all three service areas (full-stack, AI agents, data engineering)
  - Shows proper frontmatter structure
  - Example of markdown formatting

### 6. Custom Styling
- **Added:** Custom CSS to `css/custom.css` for:
  - Blog post meta (author, date, tags)
  - Featured image formatting
  - Content typography
  - Post navigation
  - Responsive design

## 🚀 How to Use

### Access the CMS (Test Mode)

1. **Start Jekyll server:**
   ```bash
   cd /Users/abidev/dev/gritsa
   bundle exec jekyll serve
   ```

2. **Visit the admin interface:**
   ```
   http://localhost:4000/admin/
   ```

3. **Create a new blog post:**
   - Click "New Blog Posts"
   - Fill in title, date, author, etc.
   - Upload a featured image (optional)
   - Write content in markdown
   - Click "Publish"

**Note:** In test mode, posts are saved to browser local storage only. To persist them, you need to manually copy the generated markdown to `_posts/` directory.

### View the Blog

1. **Blog index page:**
   ```
   http://localhost:4000/blog/
   ```

2. **Individual posts:**
   ```
   http://localhost:4000/blog/2026/01/27/welcome-to-gritsa-blog/
   ```

## 📝 Creating Blog Posts Manually

If you prefer to create posts without the CMS:

1. **Create a new file** in `_posts/` with format: `YYYY-MM-DD-title.md`
   ```
   _posts/2026-01-27-my-post-title.md
   ```

2. **Add frontmatter:**
   ```yaml
   ---
   layout: post
   title: "Your Post Title"
   date: 2026-01-27 10:00:00 +0530
   author: "Author Name"
   featured_image: "/images/blog/my-image.jpg"
   excerpt: "Short description for previews"
   tags:
     - tag1
     - tag2
   ---
   ```

3. **Write content** in markdown below the frontmatter

4. **Save and refresh** - Jekyll will automatically rebuild

## 🔄 Switching to Production (GitHub OAuth)

When ready to deploy to GitHub Pages:

### Step 1: Create GitHub OAuth App
1. Go to https://github.com/settings/developers
2. Click "OAuth Apps" → "New OAuth App"
3. Fill in:
   - Application name: `Gritsa Blog CMS`
   - Homepage URL: `https://your-username.github.io/gritsa`
   - Callback URL: `https://api.netlify.com/auth/done`
4. Save Client ID and Client Secret

### Step 2: Update admin/config.yml
Replace the backend section:
```yaml
backend:
  name: github
  repo: your-username/gritsa  # Update with your GitHub username
  branch: main
```

### Step 3: Set Up Netlify OAuth (Free)
1. Sign up at https://www.netlify.com
2. Go to Settings → Access control → OAuth
3. Install GitHub provider with your Client ID/Secret

### Step 4: Deploy
1. Commit all changes
2. Push to GitHub
3. Enable GitHub Pages in repo settings
4. Access CMS at: `https://your-username.github.io/gritsa/admin/`

## 📂 File Structure

```
gritsa/
├── admin/
│   ├── index.html          # DecapCMS interface
│   ├── config.yml          # CMS configuration
│   └── README.md           # Detailed docs
├── _posts/
│   └── 2026-01-27-welcome-to-gritsa-blog.md
├── images/
│   └── blog/               # Blog image uploads
├── _layouts/
│   └── post.html           # Blog post template
├── blog/
│   └── index.html          # Blog index (updated with Jekyll loops)
└── css/
    └── custom.css          # Includes blog styling
```

## 🎨 Blog Post Fields

When creating posts via CMS, you'll see these fields:

- **Title** (required) - Post title
- **Publish Date** (required) - When to publish
- **Author** (optional) - Default: "Gritsa Technologies"
- **Featured Image** (optional) - Upload from CMS or use existing
- **Excerpt** (optional) - Short preview text
- **Tags** (optional) - Categories/topics
- **Body** (required) - Main content in markdown

## ✏️ Markdown Tips

The CMS supports full markdown:

```markdown
# Heading 1
## Heading 2
### Heading 3

**Bold text**
*Italic text*

- Bullet list
1. Numbered list

[Link text](https://example.com)

![Image alt text](/images/blog/image.jpg)

> Blockquote

`inline code`

\```
code block
\```
```

## 🔧 Troubleshooting

### CMS doesn't load
- Check Jekyll server is running: `bundle exec jekyll serve`
- Try: `http://localhost:4000/admin/` (not http://127.0.0.1)
- Clear browser cache and reload

### Posts not appearing on blog page
- Make sure filename starts with `YYYY-MM-DD-`
- Check frontmatter has `layout: post`
- Restart Jekyll server: `Ctrl+C` then `bundle exec jekyll serve`

### Images not showing
- Upload images to `images/blog/` directory
- Reference with path: `/images/blog/filename.jpg`
- Check image file extensions match

### Test mode changes not saving
- This is expected - test mode uses browser storage
- Manually copy generated markdown to `_posts/`
- Or switch to GitHub backend for persistent storage

## 📚 Resources

- **DecapCMS Docs:** https://decapcms.org/docs/
- **Jekyll Docs:** https://jekyllrb.com/docs/
- **Markdown Guide:** https://www.markdownguide.org/

## 🎯 Next Steps

1. **Test the CMS:**
   - Start Jekyll server
   - Visit `http://localhost:4000/admin/`
   - Create a test blog post
   - View it at `http://localhost:4000/blog/`

2. **Add More Posts:**
   - Write about vibe coding challenges
   - Share AI agent use cases
   - Document data pipeline patterns

3. **When Ready for Production:**
   - Create GitHub OAuth app
   - Update `admin/config.yml` with GitHub backend
   - Set up Netlify OAuth
   - Deploy to GitHub Pages

---

**You're all set!** The blog system is ready to use in test mode. Create posts via the CMS at `http://localhost:4000/admin/` or manually in the `_posts/` directory.
