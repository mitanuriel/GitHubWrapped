#!/usr/bin/env python3
"""
Helper script to update and deploy GitHub Team Wrapped to GitHub Pages

This script will:
1. Collect fresh data from GitHub API
2. Generate updated stats.json
3. Copy to docs/ folder for GitHub Pages
4. Commit and push changes to deploy

Usage:
    python update_and_deploy.py
    
Options:
    --skip-collection: Skip data collection, only regenerate stats from existing CSVs
    --no-push: Generate and stage changes but don't push to GitHub
"""

import sys
import os
import subprocess
import shutil
from datetime import datetime

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{'='*60}")
    print(f"📍 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(e.stderr)
        return False

def main():
    skip_collection = '--skip-collection' in sys.argv
    no_push = '--no-push' in sys.argv
    
    print("\n" + "="*60)
    print("🚀 GitHub Team Wrapped - Update & Deploy")
    print("="*60)
    print(f"📅 Running at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Collect data from GitHub (unless skipped)
    if skip_collection:
        print("\n⏭️  Skipping data collection (using existing CSV files)")
    else:
        print("\n📊 Step 1/5: Collecting data from GitHub API...")
        if not run_command("python data_collection.py", "Fetching data from GitHub"):
            print("\n❌ Data collection failed. Exiting.")
            return False
    
    # Step 2: Generate stats.json for web
    print("\n📈 Step 2/5: Generating web statistics...")
    if not run_command("python generate_web_stats.py", "Creating stats.json"):
        print("\n❌ Stats generation failed. Exiting.")
        return False
    
    # Step 3: Copy stats.json to docs folder
    print("\n📁 Step 3/5: Copying stats to docs folder...")
    try:
        shutil.copy('web/stats.json', 'docs/stats.json')
        print("✅ Copied web/stats.json → docs/stats.json")
    except Exception as e:
        print(f"❌ Failed to copy stats: {e}")
        return False
    
    # Step 4: Git add and commit
    print("\n💾 Step 4/5: Committing changes...")
    
    # Check if there are changes
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        print("ℹ️  No changes to commit. Stats are already up to date!")
        return True
    
    # Stage changes
    if not run_command("git add docs/stats.json web/stats.json *.csv", "Staging updated files"):
        print("\n❌ Git add failed. Exiting.")
        return False
    
    # Commit with timestamp
    commit_msg = f"Update stats - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    if not run_command(f'git commit -m "{commit_msg}"', "Creating commit"):
        print("\n❌ Git commit failed. Exiting.")
        return False
    
    # Step 5: Push to GitHub (unless --no-push)
    if no_push:
        print("\n⏸️  Skipping push (--no-push flag set)")
        print("✅ Changes are committed locally. Run 'git push' when ready.")
    else:
        print("\n🚀 Step 5/5: Pushing to GitHub...")
        if not run_command("git push", "Deploying to GitHub Pages"):
            print("\n❌ Git push failed. You may need to push manually.")
            return False
        
        print("\n" + "="*60)
        print("✅ SUCCESS! Your GitHub Team Wrapped has been updated!")
        print("="*60)
        print("\n🌐 Your live site will update in 1-2 minutes:")
        print("   https://mitanuriel.github.io/GitHubWrapped/")
        print("\n💡 Tip: Clear your browser cache if changes don't appear immediately")
    
    return True

if __name__ == "__main__":
    print("\n")
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0)
    
    success = main()
    sys.exit(0 if success else 1)
