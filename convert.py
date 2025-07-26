import xml.etree.ElementTree as ET
import json

tree = ET.parse('products.xml')
root = tree.getroot()

items = []
for item in root.findall('SHOP/ITEM'):
    def get(tag):
        el = item.find(tag)
        return el.text.strip() if el is not None and el.text else ""
    items.append({
        "ITEM_ID": get("ITEM_ID"),
        "PRODUCTNAME": get("PRODUCTNAME"),
        "DESCRIPTION": get("DESCRIPTION"),
        "EAN": get("EAN"),
        "PRICE": get("PRICE_VAT"),
        "IMGURL": get("IMGURL"),
        "URL": get("URL")
    })

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)
