# DecapCMS Admin Interface

This directory contains the DecapCMS (formerly Netlify CMS) admin interface for managing blog posts.

## Current Setup: Test Mode

The CMS is currently configured in **test mode** for local development. This allows you to:
- Access the CMS locally without authentication
- Create and edit blog posts
- Test the interface and workflows
- Changes are stored in browser's local storage (not committed to Git)

## Accessing the CMS

### Local Development

1. Start Jekyll server:
```bash
cd /Users/abidev/dev/gritsa
bundle exec jekyll serve
```

2. Visit the admin interface:
```
http://localhost:4000/admin/
```

3. You can now:
   - Create new blog posts
   - Edit existing posts
   - Upload images to `/images/blog/`
   - Preview posts before publishing

**Note:** In test mode, changes are only saved locally in your browser. To persist them, you need to manually save the generated markdown files to the `_posts/` directory.

## Switching to Production (GitHub OAuth)

To enable the CMS for production on GitHub Pages:

### Step 1: Create GitHub OAuth App

1. Go to https://github.com/settings/developers
2. Click "OAuth Apps" → "New OAuth App"
3. Fill in:
   - **Application name:** `Gritsa Blog CMS`
   - **Homepage URL:** `https://your-username.github.io/gritsa`
   - **Authorization callback URL:** `https://api.netlify.com/auth/done`
4. Save your **Client ID** and **Client Secret**

### Step 2: Update config.yml

Edit `admin/config.yml` and replace the backend section:

```yaml
backend:
  name: github
  repo: your-username/gritsa  # Update with your GitHub username
  branch: main  # or master
```

### Step 3: Set Up Netlify OAuth (Free)

Even though you're using GitHub Pages for hosting, you'll use Netlify's free OAuth service:

1. Sign up at https://www.netlify.com (free account)
2. Go to Settings → Access control → OAuth
3. Click "Install provider" → Select "GitHub"
4. Enter your GitHub OAuth App's Client ID and Client Secret
5. Save

### Step 4: Deploy to GitHub Pages

1. Commit all changes including the `admin/` directory
2. Push to GitHub
3. Enable GitHub Pages in repository settings
4. Access CMS at: `https://your-username.github.io/gritsa/admin/`

## Blog Post Structure

Posts are created in `_posts/` directory with filename format: `YYYY-MM-DD-title.md`

Each post has frontmatter fields:
- **layout:** post (automatically set)
- **title:** Post title
- **date:** Publication date and time
- **author:** Author name (default: "Gritsa Technologies")
- **featured_image:** Path to featured image (optional)
- **excerpt:** Short description for previews (optional)
- **tags:** Array of tags (optional)
- **body:** Markdown content

## Media Files

Uploaded images are stored in `/images/blog/` and referenced in posts with path `/images/blog/filename.jpg`

## Troubleshooting

### CMS doesn't load
- Make sure Jekyll server is running
- Check browser console for errors
- Try clearing browser cache

### Changes not appearing
- In test mode, changes are browser-only
- Restart Jekyll server to see file-based changes
- Check `_posts/` directory for generated markdown files

### Images not uploading
- Ensure `/images/blog/` directory exists
- Check browser console for errors
- Verify media_folder path in config.yml

## Documentation

- DecapCMS Docs: https://decapcms.org/docs/
- Jekyll Integration: https://decapcms.org/docs/jekyll/
- GitHub Backend: https://decapcms.org/docs/github-backend/
