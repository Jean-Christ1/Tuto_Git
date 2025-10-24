# GitHub Repository Setup

This guide will help you push this project to a new GitHub repository.

## Prerequisites

- GitHub account
- Git installed locally
- Command line access

## Step 1: Create GitHub Repository

### Option A: Using GitHub Website

1. Go to https://github.com/new
2. Fill in repository details:
   - **Repository name:** `natural-language-to-sql-accelerator`
   - **Description:** "A modern web platform for querying databases using natural language and visualizing results through interactive dashboards"
   - **Visibility:** Public or Private (your choice)
   - **Do NOT initialize with:**
     - ❌ README
     - ❌ .gitignore
     - ❌ License
   (We already have these files)
3. Click "Create repository"

### Option B: Using GitHub CLI

```bash
gh repo create natural-language-to-sql-accelerator \
  --description "A modern web platform for querying databases using natural language" \
  --public
```

## Step 2: Add Remote and Push

After creating the repository on GitHub, you'll see commands like these:

```bash
cd /home/user/natural-language-to-sql-accelerator

# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/natural-language-to-sql-accelerator.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 3: Verify

Visit your repository URL:
```
https://github.com/YOUR_USERNAME/natural-language-to-sql-accelerator
```

You should see all files and folders uploaded.

## Step 4: Add Repository Details

On GitHub, add:

### Topics/Tags
Click "Add topics" and add:
- `natural-language-processing`
- `sql`
- `fastapi`
- `react`
- `langchain`
- `dashboard`
- `data-visualization`
- `python`
- `javascript`
- `machine-learning`

### About Section
```
A modern, full-stack web platform that enables users to query databases
using natural language and visualize results through interactive dashboards
and charts.
```

### Website (if deployed)
Add your deployment URL when ready.

## Step 5: Set Up GitHub Pages (Optional)

If you want to host documentation:

1. Go to repository Settings
2. Navigate to "Pages"
3. Select branch: `main`
4. Select folder: `/docs` (if you create one)
5. Click Save

## Step 6: Add Secrets for CI/CD (Optional)

If setting up GitHub Actions:

1. Go to Settings → Secrets and variables → Actions
2. Add repository secrets:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`
   - Other deployment credentials

## Alternative: Using SSH

If you prefer SSH over HTTPS:

```bash
# Add remote with SSH
git remote add origin git@github.com:YOUR_USERNAME/natural-language-to-sql-accelerator.git

# Push
git push -u origin main
```

## Troubleshooting

### Authentication Failed

**Problem:** Git asking for username/password repeatedly

**Solution 1 - Use Personal Access Token:**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`
4. Use token as password when pushing

**Solution 2 - Use SSH:**
1. Generate SSH key: `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. Add to GitHub: Settings → SSH and GPG keys
3. Use SSH remote URL

### Large Files Warning

**Problem:** Warning about large files (chinook.db)

**Solution:** The database is only ~1MB, should be fine. If you get errors:

```bash
# Add to .gitattributes
echo "*.db filter=lfs diff=lfs merge=lfs -text" >> .gitattributes
git add .gitattributes
git commit -m "Add LFS tracking for database files"
```

Or use Git LFS:
```bash
git lfs install
git lfs track "*.db"
git add .gitattributes
git commit -m "Track database files with LFS"
git push origin main
```

### Remote Already Exists

**Problem:** "fatal: remote origin already exists"

**Solution:**
```bash
# Remove existing remote
git remote remove origin

# Add correct remote
git remote add origin https://github.com/YOUR_USERNAME/natural-language-to-sql-accelerator.git

# Push
git push -u origin main
```

## Collaborators

To add collaborators:

1. Go to repository Settings
2. Navigate to "Collaborators"
3. Click "Add people"
4. Enter GitHub username or email

## Branch Protection (Recommended for Teams)

1. Go to Settings → Branches
2. Add rule for `main` branch:
   - ✅ Require pull request reviews
   - ✅ Require status checks to pass
   - ✅ Require conversation resolution

## Next Steps After Pushing

1. ✅ Verify all files are uploaded
2. ✅ Check README displays correctly
3. ✅ Add topics/tags
4. ✅ Update repository description
5. ✅ Add collaborators (if team project)
6. ✅ Set up GitHub Actions (optional)
7. ✅ Configure branch protection (optional)
8. ✅ Add project to your profile (pin it)

## Sharing Your Project

After pushing, share your repository:

**URL Format:**
```
https://github.com/YOUR_USERNAME/natural-language-to-sql-accelerator
```

**Clone Command for Others:**
```bash
git clone https://github.com/YOUR_USERNAME/natural-language-to-sql-accelerator.git
```

## Badges (Optional but Cool!)

Add these to your README.md for a professional look:

```markdown
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![React](https://img.shields.io/badge/react-18.x-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.104+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Stars](https://img.shields.io/github/stars/YOUR_USERNAME/natural-language-to-sql-accelerator)
![Forks](https://img.shields.io/github/forks/YOUR_USERNAME/natural-language-to-sql-accelerator)
```

## Keeping Your Repository Updated

For future updates:

```bash
# Make changes
git add .
git commit -m "feat: your feature description"
git push origin main
```

## Creating Releases

When ready for v1.0.0:

1. Go to Releases
2. Click "Create a new release"
3. Tag: `v1.0.0`
4. Title: `Version 1.0.0 - Initial Release`
5. Description: Feature list
6. Publish release

## Questions?

- GitHub Docs: https://docs.github.com
- Git Docs: https://git-scm.com/doc
- GitHub Support: https://support.github.com

---

**Ready to share your amazing Natural Language to SQL platform with the world! 🚀**
