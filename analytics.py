"""
Script to perform analytics on collected GitHub data
"""
import pandas as pd
from config import SINCE_DATE


def load_dataframes():
    """Load dataframes from CSV files."""
    repos_df = pd.read_csv("relevant_repos.csv")
    prs_df = pd.read_csv("relevant_prs.csv")
    if not prs_df.empty:
        prs_df["created_at"] = pd.to_datetime(prs_df["created_at"], utc=True)
    comments_df = pd.read_csv("relevant_prs_comments.csv")
    commits_df = pd.read_csv("relevant_prs_commits.csv")
    commits_stats_df = pd.read_csv("commits_stats.csv")
    
    return repos_df, prs_df, comments_df, commits_df, commits_stats_df


def calculate_aggregations(repos_df, prs_df, comments_df, commits_df, commits_stats_df):
    """Calculate all aggregations and statistics."""
    results = {}
    
    # Total repos worked on
    results["total_repos"] = len(repos_df)
    
    # Total PRs open
    results["total_prs"] = len(prs_df)
    
    # New repos created
    if not repos_df.empty:
        new_repos_this_year = repos_df[repos_df["created_at"] > SINCE_DATE]["name"].to_list()
        results["new_repos"] = new_repos_this_year
    else:
        results["new_repos"] = []
    
    # Most active month
    if not prs_df.empty:
        prs_df["created_month_name"] = prs_df["created_at"].dt.month_name()
        top_month = prs_df["created_month_name"].value_counts()
        results["top_month"] = (top_month.idxmax(), top_month.max())
    else:
        results["top_month"] = (None, 0)
    
    # Most active days
    if not prs_df.empty:
        prs_df["created_date"] = prs_df["created_at"].dt.date
        top_3_pr_dates = prs_df["created_date"].value_counts().head(3)
        results["top_3_pr_dates"] = ", ".join([f"{date}: {count}" for date, count in top_3_pr_dates.items()])
    else:
        results["top_3_pr_dates"] = "N/A"
    
    # Top PR openers
    if not prs_df.empty:
        top_5_pr_openers = prs_df["user_login"].value_counts().head(5)
        results["top_5_pr_openers"] = ", ".join([f"{user}: {count}" for user, count in top_5_pr_openers.items()])
    else:
        results["top_5_pr_openers"] = "N/A"
    
    # Top repos with most PRs opened
    if not prs_df.empty:
        top_3_repos = prs_df["repo_name"].value_counts().head(3)
        results["top_3_repos"] = ", ".join([f"{repo_name}: {count} PRs opened" for repo_name, count in top_3_repos.items()])
    else:
        results["top_3_repos"] = "N/A"
    
    # Top 3 commenters
    if not comments_df.empty:
        top_3_commenters = comments_df["user_login"].value_counts().head(3)
        results["top_3_commenters"] = ", ".join([f"{user_login}: {count} comments" for user_login, count in top_3_commenters.items()])
        results["total_comments"] = len(comments_df)
    else:
        results["top_3_commenters"] = "N/A"
        results["total_comments"] = 0
    
    # LGTM counts
    if not comments_df.empty:
        lgtm_counts = comments_df[
            comments_df["body"].str.contains("lgtm", case=False, na=False) | 
            comments_df["body"].str.contains("looks good", case=False, na=False)
        ]
        results["lgtm_count"] = len(lgtm_counts)
    else:
        results["lgtm_count"] = 0
    
    # Total commits
    results["total_commits"] = len(commits_df)
    
    # Additions and deletions
    results["total_additions"] = "?" if commits_stats_df.empty else int(commits_stats_df["additions"].sum())
    results["total_deletions"] = "?" if commits_stats_df.empty else int(commits_stats_df["deletions"].sum())
    
    return results


def print_results(results):
    """Print formatted results."""
    print("\n" + "="*60)
    print("🎉 GITHUB TEAM WRAPPED ��")
    print("="*60 + "\n")
    
    print(f"Total number of repos worked on this year: {results['total_repos']} ✅")
    print(f"Total PRs open this year: {results['total_prs']} 💪")
    
    if results['top_month'][0]:
        print(f"Most active month - {results['top_month'][0]} with {results['top_month'][1]} PRs open 🎯")
    
    if results['new_repos']:
        print(f"{len(results['new_repos'])} new repositories created - {', '.join(results['new_repos'])} 🎉")
    else:
        print("0 new repositories created this year")
    
    print(f"Top 3 days with most PRs opened: {results['top_3_pr_dates']} 📅")
    print(f"Top 5 PR openers: {results['top_5_pr_openers']} 🚀")
    print(f"Most dynamic repositories: {results['top_3_repos']} 📈")
    print(f"{results['total_comments']} comments left! Top commenters: {results['top_3_commenters']} 📢")
    print(f"{results['lgtm_count']} LGTMs given (👍🏻ᴗ_ᴗ)👍🏻")
    print(f"{results['total_commits']} commits created 🔥")
    print(f"Lines of code written: ➕ {results['total_additions']:,}" if isinstance(results['total_additions'], int) else f"Lines of code written: ➕ {results['total_additions']}")
    print(f"Lines of code deleted: ➖ {results['total_deletions']:,}" if isinstance(results['total_deletions'], int) else f"Lines of code deleted: ➖ {results['total_deletions']}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    print("Loading data from CSV files...")
    repos_df, prs_df, comments_df, commits_df, commits_stats_df = load_dataframes()
    
    print("Calculating aggregations...")
    results = calculate_aggregations(repos_df, prs_df, comments_df, commits_df, commits_stats_df)
    
    print_results(results)
