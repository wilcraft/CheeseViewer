import csv
import requests
import threading
import time
from bs4 import BeautifulSoup

threads = []
sem = threading.Semaphore(value=10)
mutex = threading.Lock()
inp = open('Text_Files/cheese_details.csv', newline='', errors='ignore')
out = open('Text_files/cheese_details_new.csv', mode='w', newline='', errors='ignore')
reader = csv.reader(inp)
writer = csv.writer(out)


def parse_cheese(row, writer):
    while True:
        sem.acquire()
        url = row[0]
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        div_img = soup.find('div', class_='cheese-image-border')
        if div_img is None:
            sem.release()
            time.sleep(0.25)
            return
        image_link = div_img.find('img')['src']
        if 'icon-cheese-default' not in image_link:
            mutex.acquire()
            writer.writerow(row)
            out.flush()
            print('Wrote row ' + row[0])
            mutex.release()
        sem.release()
        time.sleep(0.25)
        return


first_row = True
for row in reader:
    if first_row:
        writer.writerow(row)
        first_row = False
        continue
    thread = threading.Thread(target=parse_cheese, args=(row, writer))
    threads.append(thread)
    thread.start()

# for t in threads:
#     t.start()
for t in threads:
    t.join()

inp.close()
out.close()
