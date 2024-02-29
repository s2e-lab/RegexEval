import requests
from bs4 import BeautifulSoup

def get_table_data(table_data, html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    tables = soup.find_all('table', class_='searchResultsTable')

    for table in tables:
        expression_data = {}

        # Extract expression, description, matches, and non-matches
        expression_data['id'] = len(table_data) + 1 
        details_link = table.find('a', class_='buttonSmall', href=True)
        if details_link:
            expression_data['details_link'] = "https://regexlib.com/"+details_link['href'].replace('RETester.aspx', 'REDetails.aspx')
        expression_data['expression'] = table.find('tr', class_='expression').find('div', class_='expressionDiv').text.strip()
        expression_data['description'] = table.find('tr', class_='description').find('div', class_='overflowFixDiv').text.strip()
        expression_data['matches'] = table.find('tr', class_='matches').find('div', class_='overflowFixDiv').text.strip()
        expression_data['non_matches'] = table.find('tr', class_='nonmatches').find('div', class_='overflowFixDiv').text.strip()

        # Append data to the list
        table_data.append(expression_data)

    return table_data

table_data = []

for i in range(1, 43):
    url = "https://regexlib.com/Search.aspx?k=&c=-1&m=-1&ps=100&p=" + str(i)
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        table_data = get_table_data(table_data, html_content)
        print(len(table_data))
        print(table_data[-1])
    else:
        print(f"Failed to fetch data for page {i}")

# Save data to JSON file
import json
with open('./test.json', 'w') as f:
    json.dump(table_data, f)
