# 🕷️ Web Scraping GitHub Topics

This project scrapes data from [GitHub Topics](https://github.com/topics) using Python and BeautifulSoup. It collects topic-wise information about top repositories and saves the data in CSV files for further analysis or exploration.

---

##  Features

- Scrapes all topics from the GitHub Topics page.
- For each topic, extracts:
  - Topic title
  - Topic description
  - Topic URL
- For each topic's page, extracts:
  - Top 25 repositories
  - Repository name
  - Owner's username
  - Star count
  - Repository URL
- Saves each topic’s data into a separate CSV file.

---

## Tools Used

- **Python**
- **Requests** – for sending HTTP requests  
- **BeautifulSoup** – for parsing HTML  
- **Pandas** – for saving data in CSV format  

---

##  Output Format

  Each CSV file (named after the topic) contains:


STEPS TO RUN THE SCRIPT:
1. Clone the repo:
   git clone https://github.com/yourusername/WebScraping-For-Github.git
   cd WebScraping-For-Github
   
2.Install required libraries:
  pip install -r requirements.txt
  
3.Run the script:
  python scrape_github_topics.py


