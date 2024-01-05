# %%
from bs4 import BeautifulSoup
from selenium import webdriver


def get_table_data(table_data, tables):

    for table in tables:
        table_html = table.get_attribute("outerHTML")
        soup = BeautifulSoup(table_html, "html.parser")
        expression_data = {}

        # Extract expression, description, matches, and non-matches
        expression_data['id'] = len(table_data) + 1 
        details_link = soup.find('a', class_='buttonSmall', href=True)
        if details_link:
            expression_data['details_link'] = "https://regexlib.com/"+details_link['href'].replace('RETester.aspx', 'REDetails.aspx')
        expression_data['expression'] = soup.find('tr', class_='expression').find('div', class_='expressionDiv').text.strip()
        expression_data['description'] = soup.find('tr', class_='description').find('div', class_='overflowFixDiv').text.strip()
        expression_data['matches'] = soup.find('tr', class_='matches').find('div', class_='overflowFixDiv').text.strip()
        expression_data['non_matches'] = soup.find('tr', class_='nonmatches').find('div', class_='overflowFixDiv').text.strip()

        # Append data to the list
        table_data.append(expression_data)

    return table_data

# %%
import requests
from selenium.webdriver.common.by import By

table_data = []


for i in range(1, 43):
    driver = webdriver.Chrome()
    url = "https://regexlib.com/Search.aspx?k=&c=-1&m=-1&ps=100&p="+str(i)

    driver.get(url)

    tables = driver.find_elements(By.CSS_SELECTOR, "table.searchResultsTable")
    table_data = get_table_data( table_data, tables)

    print(len(table_data))
    print(table_data[-1])

    driver.close()


# %%
print(len(table_data))

# %%
import json
with open('./RegexEval_Init.json', 'w') as f:
    json.dump(table_data, f)


