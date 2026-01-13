# Climate Data Analyzer 

A climate analysis tool that fetches historical temperature data from NOAA's API, visualizes trends, and gives AI-powered insights using a local LLM.

## Features

- Fetch multi-year temperature data from 10 major U.S. cities
- Generate time-series visualizations of temperature trends
- AI-powered climate analysis using Ollama (local LLM)
- Statistical analysis including seasonal averages and variability
- User-friendly command-line interface

## Tech Stack

- Python 3.x
- pandas - Data manipulation and analysis
- matplotlib - Data visualization
- requests - API integration
- Ollama - Local LLM for climate insights (Llama 3.2)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/climate-data-analyzer.git
cd climate-data-analyzer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Ollama and download the model:
   - Download Ollama from [ollama.com](https://ollama.com)
   - Run: `ollama pull llama3.2`

5. Get a NOAA API token:
   - Visit [NOAA's Climate Data Online](https://www.ncdc.noaa.gov/cdo-web/token)
   - Request a free API token (sent instantly to your email)

6. Create a `.env` file in the project root:
```
NOAA_API_TOKEN=your_token_here
```

## Usage

Run the program:
```bash
python start_here.py
```

Follow the prompts

## Example Output
```
Climate Data Analysis
============================================================
Enter city name: Chicago
Enter start year: 2020
Enter end year: 2023

Fetching data for station GHCND:USW00094846 from 2020 to 2023
  Getting 2020... ✓ (365 records)
  Getting 2021... ✓ (365 records)
  Getting 2022... ✓ (365 records)
  Getting 2023... ✓ (365 records)

Plot saved as Chicago_2020-2023.png

AI CLIMATE ANALYSIS
============================================================
[AI provides detailed climate classification and insights]
```

## Supported Cities

- New York
- Los Angeles
- Chicago
- Houston
- Phoenix
- Philadelphia
- Miami
- Seattle
- Boston
- Denver

## Project Structure
```
climate-data-analyzer/
├── start.py          # Main program
├── README.md              # Documentation
├── requirements.txt       # Python dependencies
├── .env                   # API tokens (not here)
├── .gitignore            # Git ignore rules
└── venv/                 # Virtual environment (not here)
```

## Future Enhancements

- [ ] Add more cities and weather stations
- [ ] Include precipitation and humidity data
- [ ] Export analysis to PDF reports
- [ ] Web interface using Streamlit
- [ ] Compare cities 
- [ ] Climate change trend detection

## License

MIT License - feel free to use this project for learning or personal use.

## Author

Ichiro Bai - [GitHub](https://github.com/ichib31) | [LinkedIn](https://www.linkedin.com/in/ichiro-bai-324190338/)

## Acknowledgments

- Climate data provided by [NOAA](https://www.ncdc.noaa.gov/cdo-web/)
- AI analysis powered by [Ollama](https://ollama.com)