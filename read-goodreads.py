import pandas as pd
import re
from bs4 import BeautifulSoup
import os.path


def main():
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #filepath = input('txt file: ')
    filepath = 'goodreads.txt'
    html_path = os.path.join(BASE_DIR, filepath)
    

    with open(html_path, encoding='utf-8') as namafile:
        soup = BeautifulSoup(namafile.read(), features="html.parser") 

    judul = soup.findAll('td',{'class':'field title'})
    penulis = soup.findAll('td',{'class':'field author'})
    tanggal = soup.findAll('td',{'class':'field date_read'})

    title = []
    author = []
    date = []

    for baris in judul:
        title.append(baris.find('a').get_text().strip())
    for baris in penulis:
        full = re.split(',',baris.find('a').get_text().strip())
        try: fullname = full[1].strip()+' '+full[0]
        except: fullname = baris.find('a').get_text().strip()
        author.append(fullname)

    for baris in tanggal:
        date.append(baris.find('span').get_text())

    tabel = {'Title':title, 'Author':author, 'Status':'Finished', 'Progress':'', 'Book type':'', 'Highlight':'','Year':date}
    df = pd.DataFrame(tabel)
    date2 = []
    for row in df.Year:
        print(row)
        try: row = datetime.strptime(row, "%b %d, %Y").strftime('%m/%d/%y')
        except:
            try: row = datetime.strptime(row, "%b %Y").strftime('%m/01/%y')
            except: row = '0'
        date2.append(row)
    df['Year'] = date2

    csv_path = os.path.join(BASE_DIR, 'Goodreads.csv')
    if os.path.exists(csv_path):
        os.remove(csv_path)
    df.to_csv(csv_path, index=False)
    
    print('fin')
    
    return

if __name__ == '__main__':
    main()
