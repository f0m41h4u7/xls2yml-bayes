import xlrd  
import xml.dom.minidom  
import os  
import sys

xlsx_dir = r'./'  
xml_dir = r'./xml'  

jumpline=1



def translate_excel_to_xml(xlsx_path, name):  
    data = xlrd.open_workbook(xlsx_path)  
    print "translate " + xlsx_path.encode('utf-8') + " ... "
    if len(data.sheets()) < 1 :
        print "error: " + xlsx_path.encode('utf-8') + "  sheets  empty."
        print ""
        sys.exit(2) 
    table = data.sheets()[0]          

    nrows = table.nrows  
    ncols = table.ncols  

    doc = xml.dom.minidom.Document()  
    root = doc.createElement('root')  
    doc.appendChild(root)  
    for nrow in range(jumpline + 1, nrows):  
        item = doc.createElement('item')  
        for ncol in range(0, ncols):   
            key = "%s" % table.cell(jumpline, ncol).value  
            value = table.cell(nrow, ncol).value  
            if isinstance(value, float):  
                if abs(value % 1) < 0.000001:
                    value = "%d" % value
                else:
                    value = value = str(value)  

            t = table.cell(nrow, ncol).ctype
            if t == 0 :
                continue
            if t != 2 and t != 1:
                column = 'A'
                if ncol > 25 :
                    column = str(ncol)
                else:
                    column = chr(ncol+65)
                print "error: " + "unknown cell type: " + xlsx_path.encode('utf-8') \
                 + " | sheet: " + table.name.encode('utf-8') + " | key: " + key.encode('utf-8') \
                 + " | Position " + str(nrow+1).encode('utf-8')  + " : " + column  + "\n" 
                print "this translate process only support string or number \n"
                print " \n"
                sys.exit(1)  

            k = doc.createElement(key.encode('utf-8'))
            v = doc.createTextNode(value.encode('utf-8'))  
            k.appendChild(v)
            item.appendChild(k)
        root.appendChild(item)  
    xml_name = name.strip().split('.')[0] + '.xml'  
    xml_path = os.path.join(xml_dir, xml_name)  
  
    f = open(xml_path, 'w')  
    f.write(doc.toprettyxml())  
    f.close()  
  

              
  
if __name__ == "__main__":  
    print sys.argv
    if len(sys.argv) < 3:
        print "used example: xlsx2xml.exe ../from_dir/ ../to_dir/"
        sys.exit(3)
    xlsx_dir=sys.argv[1]
    xml_dir=sys.argv[2]
    if os.path.isfile(xlsx_dir):
        _, name=os.path.split(xlsx_dir)
        translate_excel_to_xml(xlsx_dir, name)  
    else:
        for name in os.listdir(xlsx_dir):  
            if name.endswith('.xlsx') and not name.endswith('~', 0, 1):  
                xlsx_path = os.path.join(xlsx_dir, name)  
                translate_excel_to_xml(xlsx_path, name)
