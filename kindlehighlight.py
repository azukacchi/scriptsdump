import pandas as pd
import re
from bs4 import BeautifulSoup
import os.path


def main():
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    filepath = input('txt file: ')
    html_path = os.path.join(BASE_DIR, filepath)
    

    with open(html_path, encoding='utf-8') as namafile:
        soup = BeautifulSoup(namafile.read(), features="html.parser") 

    judul = re.sub('[!@#$:]', '', soup.find_all('h3')[0].get_text())+'.csv'
    teks = soup.findAll('span', {'id':'highlight'})
    page = soup.findAll('span', {'id':'annotationNoteHeader'})
    note = soup.findAll('span', {'id': 'note'})

    hal = []
    isiteks = []
    isinotes = []
    
    for baris in teks:
        isiteks.append(baris.get_text())

    for baris in page:
        hal.append(re.findall('\d+',baris.get_text())[0])
    
    for baris in note:
        isinotes.append(baris.get_text())

    tabel = {'Highlight':isiteks, 'Page':hal, 'Note':isinotes}
    df = pd.DataFrame(tabel)
    
    csv_path = os.path.join(BASE_DIR, judul)
    df.to_csv(csv_path, index=False)

    print('fin')
    
    return

if __name__ == '__main__':
    main()
