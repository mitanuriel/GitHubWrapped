# GitHub Team Wrapped 

A Python tool to generate a "Spotify Wrapped"-style summary of your team's GitHub activity for the year with an interactive web dashboard.

**🌐 [View Live Demo](https://mitanuriel.github.io/GitHubWrapped/)**

## Features

- 📊 Interactive animated web presentation
- 💪 Pull requests, commits, and code review statistics
- 🎯 Team activity insights and top contributors
- 🎬 Full-screen slides with smooth animations

## Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `pandas` - Data analysis
- `requests` - GitHub API calls
- `tqdm` - Progress bars
- `python-dotenv` - Environment variables

### Configure

1. Create a `.env` file and add your GitHub token:
```
GITHUB_TOKEN=your_github_token_here
```

2. Edit `config.py` to set your team members, organization name, and date range.

## Usage

### Quick Deploy (Recommended)

Update stats and deploy to GitHub Pages in one command:

```bash
python update_and_deploy.py
```

This will automatically:
- Collect fresh data from GitHub API
- Generate updated statistics
- Deploy to your live site at https://mitanuriel.github.io/GitHubWrapped/

**Options:**
- `--skip-collection` - Skip data collection, use existing CSV files
- `--no-push` - Preview changes without deploying

### Manual Workflow

Alternatively, run steps individually:

#### 1. Collect data and view console results:

```bash
python main.py
```

#### 2. Generate and open web dashboard locally:

```bash
python generate_web_stats.py
open web/index.html
```

The web dashboard features animated slides with keyboard navigation (arrow keys/spacebar) and mobile swipe support.

## License

MIT License
