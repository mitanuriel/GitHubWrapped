"""
Script to collect data from GitHub API
"""
import time
import pandas as pd
from tqdm import tqdm
from config import ORG_NAME, TEAM_MEMBERS, SINCE_DATE
from github_api_helpers import (
    fetch_org_repos,
    fetch_prs,
    fetch_comments_url,
    filter_prs_by_date,
    filter_prs_by_collaboarators,
    get_commit_details,
    fetch_workflow_runs,
    fetch_workflows
)


def collect_github_data():
    """Main function to collect all GitHub data."""
    print("Fetching organization repositories...")
    org_repos = fetch_org_repos(ORG_NAME)
    print(f"Found {len(org_repos)} repositories in the organization.")

    print("Identifying repositories with contributions from team members...")
    relevant_repos = []
    relevant_prs = []
    relevant_prs_comments = []
    relevant_prs_commits = []
    commits_stats = []
    workflow_runs = []
    
    t = tqdm(org_repos, leave=True, bar_format="{desc} {n_fmt}/{total_fmt}")

    for repo in t:
        t.set_description("%s" % repo["full_name"])
        t.refresh()
        try:
            prs = fetch_prs(repo["full_name"])
            # Filter out pull requests by SINCE_DATE
            # comment out to get the full repo history
            prs = filter_prs_by_date(prs)

            # Filter out by collaborators
            # comment out to get PRs from all collaborators
            prs = filter_prs_by_collaboarators(prs, TEAM_MEMBERS)

            # Fetch the comments if there are any
            for pr in prs:
                pull_comments = fetch_comments_url(pr["review_comments_url"])
                issue_comments = fetch_comments_url(pr["comments_url"])
                commits = [commit["commit"]
                           for commit in fetch_comments_url(pr["commits_url"])]
                relevant_prs_comments.extend(pull_comments)
                relevant_prs_comments.extend(issue_comments)
                relevant_prs_commits.extend(commits)
            
            # Fetch workflow runs for this repo
            try:
                runs = fetch_workflow_runs(repo["full_name"])
                workflow_runs.extend(runs)
            except Exception as e:
                print(f"\nNote: Could not fetch workflows for {repo['full_name']}: {e}")
            
            if len(prs) > 0:
                time.sleep(30)
                relevant_repos.append(repo)
                relevant_prs.extend(prs)
        except Exception as e:
            print(f"Error processing {repo['full_name']}: {e}")
            # Timeout in case of hitting Github API rate limit
            # t.set_description("%s Exception, sleeping 1 minute" % e)
            # t.refresh()
            # time.sleep(60)

    print("\nCollecting commit statistics (this may take a while)...")
    print("Note: This step can be skipped for optimization.")
    
    # Optional: Collect detailed commit stats
    # Comment out the following block to skip this step
    for commit in tqdm(relevant_prs_commits):
        try:
            repo = commit["url"].split("/")[4] + "/" + commit["url"].split("/")[5]
            sha = commit["url"].split("/")[8]
            stats = get_commit_details(repo, sha)["stats"]
            commits_stats.append({
                "sha": sha, 
                "additions": stats["additions"], 
                "deletions": stats["deletions"]
            })
        except Exception as e:
            print(f"Error collecting stats for commit {sha}: {e}")

    return relevant_repos, relevant_prs, relevant_prs_comments, relevant_prs_commits, commits_stats, workflow_runs


def create_dataframes(relevant_repos, relevant_prs, relevant_prs_comments, 
                      relevant_prs_commits, commits_stats, workflow_runs):
    """Create and save pandas dataframes from collected data."""
    print("\nCreating dataframes...")
    
    # Repos dataframe
    repos_df = pd.DataFrame.from_dict(relevant_repos)
    repos_df.to_csv("relevant_repos.csv", index=False)
    print("✓ Saved relevant_repos.csv")

    # PRs dataframe
    prs_df = pd.DataFrame.from_dict(relevant_prs)
    if not prs_df.empty:
        prs_df["user_login"] = prs_df["user"].apply(lambda d: d.get("login"))
        prs_df["created_at"] = pd.to_datetime(prs_df["created_at"], utc=True)
        prs_df["repo_name"] = prs_df["url"].apply(lambda d: d.split("/")[5])
    prs_df.to_csv("relevant_prs.csv", index=False)
    print("✓ Saved relevant_prs.csv")

    # Comments dataframe
    comments_df = pd.DataFrame.from_dict(relevant_prs_comments)
    if not comments_df.empty:
        comments_df["user_login"] = comments_df["user"].apply(lambda d: d.get("login"))
        comments_df["repo_name"] = comments_df["html_url"].apply(lambda d: d.split("/")[4])
    comments_df.to_csv("relevant_prs_comments.csv", index=False)
    print("✓ Saved relevant_prs_comments.csv")

    # Commits dataframe
    commits_df = pd.DataFrame.from_dict(relevant_prs_commits)
    if not commits_df.empty:
        commits_df["user_login"] = commits_df["committer"].apply(lambda d: d.get("login") if d else None)
        commits_df["repo_name"] = commits_df["url"].apply(lambda d: d.split("/")[5])
    commits_df.to_csv("relevant_prs_commits.csv", index=False)
    print("✓ Saved relevant_prs_commits.csv")

    # Commit stats dataframe
    commits_stats_df = pd.DataFrame.from_dict(commits_stats)
    commits_stats_df.to_csv("commits_stats.csv", index=False)
    print("✓ Saved commits_stats.csv")

    # Workflow runs dataframe
    workflow_runs_df = pd.DataFrame.from_dict(workflow_runs)
    if not workflow_runs_df.empty:
        workflow_runs_df["created_at"] = pd.to_datetime(workflow_runs_df["created_at"], utc=True)
        workflow_runs_df["repo_name"] = workflow_runs_df["repository"].apply(lambda d: d.get("full_name") if d else None)
    workflow_runs_df.to_csv("workflow_runs.csv", index=False)
    print("✓ Saved workflow_runs.csv")

    return repos_df, prs_df, comments_df, commits_df, commits_stats_df, workflow_runs_df


if __name__ == "__main__":
    # Collect data
    relevant_repos, relevant_prs, relevant_prs_comments, relevant_prs_commits, commits_stats, workflow_runs = collect_github_data()
    
    # Create dataframes
    repos_df, prs_df, comments_df, commits_df, commits_stats_df, workflow_runs_df = create_dataframes(
        relevant_repos, relevant_prs, relevant_prs_comments, 
        relevant_prs_commits, commits_stats, workflow_runs
    )
    
    print("\n✅ Data collection complete!")
