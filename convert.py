import requests
import xml.etree.ElementTree as ET
import json # JSON už nebudeme přímo generovat, ale necháme import pro případné ladění

# URL XML feedu
url = "https://www.krytnamobil.cz/products.xml"

# Stažení XML feedu
try:
    response = requests.get(url)
    response.raise_for_status() # Vyvolá chybu pro špatné HTTP odpovědi (4xx nebo 5xx)
    response.encoding = "utf-8"
    root = ET.fromstring(response.text)
except requests.exceptions.RequestException as e:
    print(f"Chyba při stahování XML feedu: {e}")
    exit()
except ET.ParseError as e:
    print(f"Chyba při parsování XML feedu: {e}")
    exit()

# Vytvoření kořenového elementu pro Shoptet XML
shoptet_products = ET.Element("products")

# Převod XML na Shoptet XML strukturu
for item in root.findall(".//SHOPITEM"): #
    # Získání dat z původního feedu
    product_name = item.findtext("PRODUCT")
    price_vat = item.findtext("PRICE_VAT")
    item_id = item.findtext("ITEM_ID")
    manufacturer = item.findtext("MANUFACTURER")
    description = item.findtext("DESCRIPTION")
    stock_quantity = item.findtext("STOCK_QUANTITY")
    
    # Získání URL obrázků (předpoklad, že jsou v IMGURL elementech)
    images_urls = [img.text for img in item.findall("IMGURL")]
    
    # Získání kategorie (předpoklad, že je v CATEGORYTEXT elementu)
    category_text = item.findtext("CATEGORYTEXT")

    # Vytvoření <product> elementu pro Shoptet
    product_element = ET.SubElement(shoptet_products, "product")

    # Přidání povinných elementů
    ET.SubElement(product_element, "code").text = item_id if item_id else ""
    ET.SubElement(product_element, "name").text = product_name if product_name else ""
    ET.SubElement(product_element, "price_vat").text = price_vat if price_vat else ""
    
    # Cena bez DPH (pokud ji nemáte, je potřeba ji dopočítat nebo nastavit placeholder)
    price_without_vat = None # Zde můžete doplnit logiku pro výpočet ceny bez DPH
    ET.SubElement(product_element, "price").text = str(price_without_vat) if price_without_vat is not None else ""

    ET.SubElement(product_element, "stock").text = stock_quantity if stock_quantity else "0"
    ET.SubElement(product_element, "stock_type").text = "available" if int(stock_quantity or 0) > 0 else "unavailable" # Logika pro stock_type

    # Přidání volitelných elementů
    if manufacturer:
        ET.SubElement(product_element, "manufacturer").text = manufacturer
    if description:
        ET.SubElement(product_element, "description").text = description.strip()
    
    if category_text:
        ET.SubElement(product_element, "category").text = category_text

    # Obrázky
    if images_urls:
        images_element = ET.SubElement(product_element, "images")
        for img_url in images_urls:
            if img_url:
                ET.SubElement(images_element, "image").text = img_url

# Vytvoření XML stromu a uložení do souboru
tree = ET.ElementTree(shoptet_products)
# Zajištění hezkého formátování XML
ET.indent(tree, space="  ", level=0)

with open("shoptet_products.xml", "wb") as f: # Ukládáme jako binární soubor (wb) pro správné kódování
    tree.write(f, encoding="utf-8", xml_declaration=True)

print("shoptet_products.xml byl úspěšně vytvořen.")
