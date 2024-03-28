# FACEIT Map Ban Analyzer

FACEIT Map Ban Analyzer is a Python tool that is intricately designed for e-sports teams who compete on the FACEIT platform playing Counter-Strike 2. The application makes use of detailed match and player statistics from the FACEIT API to give strategic map ban suggestions which are intended to results in better winning chances of the team after analyzing historical performance data.

## Features

- Retrieves comprehensive match details and player stats directly from the FACEIT API.

- Employs weighted win rate calculations for maps based on individual player performances and team dynamics.

- Outputs strategic map ban recommendations to undermine the opposing team's advantages.

## Getting Started

Here, we have included instructions that will guide you on how to install and run FACEIT Map Ban Analyzer in your personal computer.

### Prerequisites

- Python 3.6 or newer

- `requests` library for making API calls

- `python-dotenv` for managing sensitive environment variables securely
  
### Installation
1. Clone the repository to your local machine:
git clone https://github.com/rhnguyenms/faceitmapban.git

2. Change to the project directory:
cd faceitmapban

3. Install necessary Python packages:
pip install -r requirements.txt

### Configuration

1. Create a `.env` file in the root directory of the project.
2. Add your FACEIT API key to the `.env` file as follows:
FACEIT_API_KEY=<Your_FACEIT_API_Key>

Replace `<Your_FACEIT_API_Key>` with your actual API key.

### Usage

Execute the script via the command line, and input the desired match ID when prompted:
python mapban.py





