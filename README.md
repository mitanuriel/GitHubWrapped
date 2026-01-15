# GitHub Team Wrapped 🎁

A Python tool to generate a "Spotify Wrapped"-style summary of your team's GitHub activity for the year with an interactive web dashboard.

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

### Collect data and view results:

```bash
python main.py
```

### Generate and open web dashboard:

```bash
python generate_web_stats.py
open web/index.html
```

The web dashboard features animated slides with keyboard navigation (arrow keys/spacebar) and mobile swipe support.

## License

MIT License
