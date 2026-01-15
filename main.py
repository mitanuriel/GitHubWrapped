"""
Main script to run GitHub Team Wrapped
"""
from data_collection import collect_github_data, create_dataframes
from analytics import calculate_aggregations, print_results


def main():
    """Main function to run the complete workflow."""
    print("🎬 Starting GitHub Team Wrapped...")
    print("="*60 + "\n")
    
    # Step 1: Collect data from GitHub API
    print("STEP 1: Collecting data from GitHub API")
    print("-"*60)
    relevant_repos, relevant_prs, relevant_prs_comments, relevant_prs_commits, commits_stats, workflow_runs = collect_github_data()
    
    # Step 2: Create and save dataframes
    print("\nSTEP 2: Creating dataframes")
    print("-"*60)
    repos_df, prs_df, comments_df, commits_df, commits_stats_df, workflow_runs_df = create_dataframes(
        relevant_repos, relevant_prs, relevant_prs_comments, 
        relevant_prs_commits, commits_stats, workflow_runs
    )
    
    # Step 3: Calculate aggregations and display results
    print("\nSTEP 3: Calculating statistics")
    print("-"*60)
    results = calculate_aggregations(repos_df, prs_df, comments_df, commits_df, commits_stats_df)
    print_results(results)
    
    print("\n✨ GitHub Team Wrapped complete! ✨")


if __name__ == "__main__":
    main()
