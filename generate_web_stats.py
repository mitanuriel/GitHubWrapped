"""
Script to generate stats.json for the web interface
"""
import json
import pandas as pd
from config import TEAM_MEMBERS

def generate_stats_json():
    """Generate stats.json file for the web interface"""
    
    print("Generating stats.json for web interface...")
    
    # Load data
    try:
        repos_df = pd.read_csv("relevant_repos.csv")
        prs_df = pd.read_csv("relevant_prs.csv")
        if not prs_df.empty:
            prs_df["created_at"] = pd.to_datetime(prs_df["created_at"], utc=True)
        comments_df = pd.read_csv("relevant_prs_comments.csv")
        commits_df = pd.read_csv("relevant_prs_commits.csv")
        commits_stats_df = pd.read_csv("commits_stats.csv")
        
        # Load workflow runs (may not exist in older data)
        try:
            workflow_runs_df = pd.read_csv("workflow_runs.csv")
            if not workflow_runs_df.empty:
                workflow_runs_df["created_at"] = pd.to_datetime(workflow_runs_df["created_at"], utc=True)
        except FileNotFoundError:
            workflow_runs_df = pd.DataFrame()
            print("Note: workflow_runs.csv not found. Skipping workflow stats.")
    except FileNotFoundError as e:
        print(f"Error: CSV files not found. Please run data collection first.")
        print(f"Missing file: {e}")
        return
    
    # Calculate stats
    total_prs = len(prs_df)
    total_commits = len(commits_df)
    total_comments = len(comments_df)
    total_additions = int(commits_stats_df["additions"].sum()) if not commits_stats_df.empty else 0
    total_deletions = int(commits_stats_df["deletions"].sum()) if not commits_stats_df.empty else 0
    
    # Workflow stats
    total_workflow_runs = len(workflow_runs_df)
    successful_runs = len(workflow_runs_df[workflow_runs_df["conclusion"] == "success"]) if not workflow_runs_df.empty else 0
    failed_runs = len(workflow_runs_df[workflow_runs_df["conclusion"] == "failure"]) if not workflow_runs_df.empty else 0
    
    # Top contributor
    if not prs_df.empty:
        top_pr_opener = prs_df["user_login"].value_counts().head(1)
        top_contributor = top_pr_opener.index[0]
        top_contributor_prs = int(top_pr_opener.values[0])
    else:
        top_contributor = "N/A"
        top_contributor_prs = 0
    
    # Busiest month
    if not prs_df.empty:
        prs_df["created_month_name"] = prs_df["created_at"].dt.month_name()
        top_month = prs_df["created_month_name"].value_counts()
        busiest_month = top_month.idxmax()
        busiest_month_prs = int(top_month.max())
    else:
        busiest_month = "N/A"
        busiest_month_prs = 0
    
    # Most active repo
    if not prs_df.empty:
        top_repo = prs_df["repo_name"].value_counts().head(1)
        most_active_repo = top_repo.index[0]
        most_active_repo_prs = int(top_repo.values[0])
    else:
        most_active_repo = "N/A"
        most_active_repo_prs = 0
    
    # Prepare data for web interface
    web_stats = {
        "team_size": len(TEAM_MEMBERS),
        "repo_count": len(repos_df),
        "total_prs": total_prs,
        "top_contributor": top_contributor,
        "top_contributor_prs": top_contributor_prs,
        "total_additions": total_additions,
        "total_deletions": total_deletions,
        "total_commits": total_commits,
        "total_comments": total_comments,
        "busiest_month": busiest_month,
        "busiest_month_prs": busiest_month_prs,
        "most_active_repo": most_active_repo,
        "most_active_repo_prs": most_active_repo_prs,
        "total_workflow_runs": total_workflow_runs,
        "successful_workflow_runs": successful_runs,
        "failed_workflow_runs": failed_runs
    }
    
    # Write to JSON file in web directory
    with open('web/stats.json', 'w') as f:
        json.dump(web_stats, f, indent=2)
    
    print("✓ Generated web/stats.json")
    print(f"\nStats Summary:")
    print(f"  Total PRs: {web_stats['total_prs']}")
    print(f"  Top Contributor: {web_stats['top_contributor']} ({web_stats['top_contributor_prs']} PRs)")
    print(f"  Total Commits: {web_stats['total_commits']}")
    print(f"  Total Comments: {web_stats['total_comments']}")
    print(f"  Code Changes: +{web_stats['total_additions']:,} -{web_stats['total_deletions']:,}")
    print(f"  Busiest Month: {web_stats['busiest_month']} ({web_stats['busiest_month_prs']} PRs)")
    print(f"  Most Active Repo: {web_stats['most_active_repo']} ({web_stats['most_active_repo_prs']} PRs)")
    print(f"  Workflow Runs: {web_stats['total_workflow_runs']} total ({web_stats['successful_workflow_runs']} successful, {web_stats['failed_workflow_runs']} failed)")
    
    return web_stats

if __name__ == "__main__":
    generate_stats_json()
