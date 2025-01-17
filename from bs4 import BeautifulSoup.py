from bs4 import BeautifulSoup
import requests
from groq import Groq
import os 

from urllib.parse import urljoin

item = input('Please enter product name')
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

# Send GET request to Amazon
url = f"https://www.flipkart.com/search?q={item}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off"
response = requests.get(url, headers=headers)

# Print raw HTML for debugging (this can be very large)
  # Print the first 1000 characters of the raw HTML

soup = BeautifulSoup(response.content, 'html.parser')

    # Try to find the product elements
apple_links = soup.find('a', string=lambda text: text and  item in text.lower() if text else False)
if apple_links==None:
  apple_links = soup.find('div', string=lambda text: text and  item in text.lower() if text else False)
# Print the links that contain 'apple'
  # The links are in the 'href' attribute of the <a> tag

 # Print the text inside the link (product name)
 # This is the name of the product on Amazon

print(apple_links.text)
link=apple_links.get('href', None)
base="https://www.flipkart.com/"
hello = urljoin(base,link)
print(hello)
 # Extract the product price
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"tell me about {hello}",
        }
    ],
    model="llama-3.3-70b-versatile",
)

print(chat_completion.choices[0].message.content)

