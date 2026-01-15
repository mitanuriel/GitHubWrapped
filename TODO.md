# GitHub Team Wrapped - TODO List

## Setup Tasks

- [ ] **Install dependencies**
  ```bash
  pip install -r requirements.txt
  ```

- [ ] **Create GitHub Personal Access Token**
  - Go to: https://github.com/settings/tokens
  - Create classic token with permissions: `read:org`, `read:project`, `read:user`, `repo`
  - Save token securely

- [ ] **Configure settings in `config.py`**
  - [ ] Add your GitHub token to `GITHUB_TOKEN`
  - [ ] Update `TEAM_MEMBERS` list with team member usernames
  - [ ] Update `ORG_NAME` with your organization name
  - [ ] Adjust `SINCE_DATE` for your desired time period (default: 2025-01-01)

## Running the Project

- [ ] **Test API connection**
  - Run a small test to ensure your token works
  - Check that you have access to the organization

- [ ] **Run data collection**
  ```bash
  python data_collection.py
  ```
  - Note: This can take a while depending on org size
  - Optional: Comment out commit stats collection for faster execution

- [ ] **Run analytics**
  ```bash
  python analytics.py
  ```

- [ ] **Or run complete workflow**
  ```bash
  python main.py
  ```

## Optional Enhancements

- [ ] Add visualization with matplotlib/seaborn
- [ ] Create HTML/PDF report generation
- [ ] Add support for multiple organizations
- [ ] Implement caching to avoid re-fetching data
- [ ] Add unit tests
- [ ] Create command-line interface with argparse
- [ ] Add progress indicators for long-running operations
- [ ] Implement incremental updates (only fetch new data)
- [ ] Add email notification when complete
- [ ] Create shareable wrapped cards/images

## Troubleshooting

- [ ] Check API rate limits if errors occur
- [ ] Verify token permissions if getting 403/401 errors
- [ ] Ensure team member usernames are correct
- [ ] Check organization name spelling
- [ ] Verify date format in SINCE_DATE

## Notes

- **API Rate Limits**: GitHub API has rate limits. The script includes delays to handle this.
- **Performance**: For large organizations, consider running during off-hours.
- **Data Privacy**: Keep your token secure. Never commit `config.py` with your real token.
