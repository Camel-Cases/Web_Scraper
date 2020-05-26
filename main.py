from bs4 import BeautifulSoup
import requests, os, json

# the search query given to this URL should be seperated by %20
URL = "https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off"

def search_and_fetch_html(search_words):
    search_query = search_words.strip().replace(" ", "%20")
    url = URL.format(search_query)
    html_doc = requests.get(url).content
    return html_doc

def search_items(html_doc):
    soup = BeautifulSoup(html_doc, "html.parser")
    # try 1
    # item = _3wU53n <div class>
    # price = _1vC4OE _2rQ-NK <div class>
    # try 2
    # item = _2cLu-l <a class>
    # price = _1vC4OE <div class>
    # try 1
    items = soup.find_all("div", class_="_3wU53n")
    prices = soup.find_all("div", class_="_1vC4OE _2rQ-NK")
    json_list = []
    for item, price in zip(items, prices):
        price = price.text.replace("\u20b9", "") # includes this \u20b9 which should be replaced
        items_dict = {"Name": item.text.strip(), "Price": price.strip()}
        json_list.append(items_dict)
    # try 2
    if len(json_list) == 0:
        items = soup.find_all("a", class_="_2cLu-l")
        prices = soup.find_all("div", class_="_1vC4OE")
        json_list = []
        for item, price in zip(items, prices):
            price = price.text.replace("\u20b9", "")
            items_dict = {"Name": item.text.strip(), "Price": price.strip()}
            json_list.append(items_dict)
    file = open("items.json", "w")
    json.dump(json_list, file, indent=2)
    file.close()
    print("-"*40)
    os.system("cat items.json")
    print("-"*40)
    return json_list

def main():
    search_words = input("Enter item name: ").strip()
    print("Searching on flipkart...")
    html_doc = search_and_fetch_html(search_words)
    search_items(html_doc)

if __name__ == "__main__":
    main()
