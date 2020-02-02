import pandas as pd
import xml.etree.ElementTree as et

#df = pd.read_excel(open(fname, 'rb'))
#df_abc = df[df["Products"] == "ABC"]

# open table and parse it
fname = 'table.xls'
df = ExcelFile.parse(fname)

# create file structure of yml
yml_catalog = et.Element('yml_catalog')
yml_catalog.set('date', inf.get('date'))
shop = et.Element('shop')

name = et.SubElement(shop, 'name')
yml_catalog.set('name', inf.get('name'))

company = et.SubElement(shop, 'company')
yml_catalog.set('company', comp)

url = et.SubElement(shop, 'url')
yml_catalog.set('url', comp_url)

currencies = et.SubElement(shop, 'currencies')
currency = et.SubElement('')
