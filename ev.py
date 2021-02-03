import csv
import requests
import datetime
import sys
from bs4 import BeautifulSoup
from os import path
from time import sleep

OUTFILE = ''


def go_scrape(url, card_name):
    my_date_time = datetime.datetime.now()
    headers = {'User-Agent': "Chrome/54.0.2840.90"}
    response = requests.get(url, headers=headers)
    html = response.content

    soup = BeautifulSoup(html, "lxml")
    table = soup.find('div', attrs={'class': 'table-responsive'})
    card_name = card_name

    for row in table.findAll('tr')[1:2]:
        list_of_cells = []
        for cell in row.findAll("td"):
            text = cell.text.replace('&nbsp;', '')
            list_of_cells.append(text)
        list_of_cells.append(card_name)
        list_of_cells.append(my_date_time)
        return list_of_cells


def run():
    global OUTFILE
    print("trying")
    try:
        while True:
            if not path.exists("mining.csv"):
                print("Creating File")
                OUTFILE = open("mining.csv", "w")
                writer = csv.writer(OUTFILE)
                writer.writerow(["Algorithm", "HashRate", "EPM ETH", "EPM BTC", "EPM USD", "Card", "Date"])
            else:
                print("Opening File")
                OUTFILE = open("mining.csv", "a")
                writer = csv.writer(OUTFILE)
            # for each in range(1, 10):

            print("Scraping")
            writer.writerow(go_scrape('https://www.betterhash.net/NVIDIA-GeForce-RTX-2060-SUPER-mining-profitability'
                                      '-557.html', "RTX-2060 Super"))
            # writer.writerow(go_scrape('https://www.betterhash.net/NVIDIA-GeForce-RTX-2070-SUPER-mining-profitability'
            #                           '-639211.html', "RTX-2070 Super"))
            # writer.writerow(go_scrape('https://www.betterhash.net/NVIDIA-GeForce-RTX-3090-mining-profitability-47133091'
            #                           '.html', "RTX-3090"))
            # print("Closing")
            # outfile.close()
            sleep(360)

    except KeyboardInterrupt:
        OUTFILE.close()
        print("Keyboard Interrupt")
        sys.exit(0)

    except Exception as e:
        print("Error")
        print(e)
        OUTFILE.close()
        sys.exit()

    finally:
        print("Closing")
        OUTFILE.close()


if __name__ == '__main__':
    run()
