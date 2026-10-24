### Problem Statement: Web Scraping for Blockchain Transaction Information

Objective:
The goal is to develop a Python script that extracts transaction details from a block explorer website for a specified cryptocurrency. The extracted data should include transaction ID, timestamp, sender address, recipient address, and amount transferred.

Background:
Block explorers are online tools that allow users to search and view details of blockchain transactions. Each transaction on a blockchain network, such as Bitcoin or Ethereum, contains important information that can be accessed via these explorers. For this problem, you'll choose a block explorer for a specific cryptocurrency and create a script to scrape transaction data.

Requirements:

1. Target Website:
Choose a block explorer website for a popular cryptocurrency (e.g., Bitcoin, Ethereum). Examples of block explorers include:
- [Blockchain.com](https://www.blockchain.com/explorer)
- [Etherscan.io](https://etherscan.io/)
- [Blockcypher.com](https://live.blockcypher.com/)

2. Data to Extract:
For each transaction, extract the following information:
- Transaction ID
- Timestamp
- Sender Address
- Recipient Address
- Amount Transferred

3. Pagination Handling:
Block explorers typically list transactions with pagination. Your script should handle pagination to extract multiple pages of transaction data.

4. Error Handling:
Implement error handling to manage situations where the webpage structure changes or the requested data is unavailable.

5. Output Format:
Save the extracted data into a CSV file with the following columns:
- transaction_id
- timestamp
- sender_address
- recipient_address
- amount_transferred

6. Documentation:
Provide a README file with instructions on how to run the script, including any dependencies that need to be installed.

Bonus Points:
- Implement a function to convert the timestamp to a readable format (e.g., "YYYY-MM-DD HH:MM:SS").
- Include additional data points if available, such as transaction fees or confirmations.
- Write unit tests to validate the extraction functions.

The extracted data will be saved in transactions.csv.

By following this problem statement, you will create a robust web scraping script capable of extracting detailed transaction information from a block explorer website.


# Block Explorer Scraper

## Requirements
- Python 3.x
- playwright
- beautifulsoup4
- pandas

## Installation
```bash
pip install playwright beautifulsoup4 pandas