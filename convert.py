
import requests
import xml.etree.ElementTree as ET
import json

# URL XML feedu
url = "https://www.krytnamobil.cz/products.xml"

# Stažení XML feedu
response = requests.get(url)
response.encoding = "utf-8"
root = ET.fromstring(response.text)

# Převod XML na JSON strukturu
products = []
for item in root.findall(".//SHOPITEM"):
    product = {
        "name": item.findtext("PRODUCT"),
        "price_vat": item.findtext("PRICE_VAT"),
        "item_id": item.findtext("ITEM_ID"),
        "manufacturer": item.findtext("MANUFACTURER"),
        "description": item.findtext("DESCRIPTION"),
        "stock": item.findtext("STOCK_QUANTITY"),
    }
    products.append(product)

# Uložení jako JSON
with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print("products.json byl úspěšně vytvořen.")
