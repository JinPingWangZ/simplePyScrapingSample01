import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs
import csv
import array as arr
import datetime

csvData =[]
csvTemp =[]
csvTemp.append('Date')
csvTemp.extend(['HomeTeam','AwayTeam','<0-0>','<1-0>','<2-0>','<3-0>','<4-0>','<4-1>','<4-2>','<0-1>','<1-1>','<2-1>','<3-1>','<0-2>','<1-2>','<2-2>','<3-2>','<0-3>','<1-3>','<2-3>','<0-4>','<1-4>','<2-4>','<3-3>','Total','AVG'])
csvData.append(csvTemp)
csvTemp =[]


def convertDate( strDate ):

    day_of_week_list = [ 'Man', 'Tir', 'Tor', 'Ons', 'Fre', 'Lør', 'Søn' ]

    items = strDate.split('.')
    date_today = datetime.date.today()
    print( items )
    if items[0] == "I morgen":
        item = date_today + datetime.timedelta( days = 1 )
        return item
    elif items[0] == "":
        item = date_today
        return item
    elif items[1] != "":
        item = '-'.join( [ str( date_today.year ), str(int(items[1])), str(int(items[2])) ] )
        return item
    else:
        index_today = date_today.weekday()
        index_week = day_of_week_list.index( str(items[0]) )
        item = date_today   + datetime.timedelta( days = (index_week-index_today) )
        return item

try:
    driver = webdriver.Chrome("chromedriver.exe")
    driver.set_page_load_timeout(-1)

    driver.get("https://www.norsk-tipping.no/sport/langoddsen")
    #driver.get("https://localhost/zzz")
    time.sleep(5)

    driver.find_element_by_id("langoddsenGameBoardSearchField").clear()
    driver.find_element_by_id("langoddsenGameBoardSearchField").send_keys("tottenham")
    time.sleep(5)

    html = driver.page_source
    soup = bs(html, 'lxml')
    elements = soup.find_all('ul')

    arr = []
    for e in elements:
        style = e.get('style')
        idstr = e.get('id')

        if style == "" and idstr != None:
            arr.append(idstr)
            print(idstr)
        else:
            style = ""
            continue
    addItems = []
    for indexItems in arr:
        try:
            csvTemp=[]
            dataDay = driver.find_element_by_css_selector(
                "#" + indexItems + "> li.gameData.date.ellipsis > div > span.dayString")
            print(dataDay.text)

            dataTime = driver.find_element_by_css_selector(
                "#" + indexItems + "> li.gameData.date.ellipsis > div > span.dateTime")
            print(dataTime.text)

            csvTemp.append(str(convertDate(dataDay.text)))

            dataHomeT = driver.find_element_by_css_selector("#" + indexItems +">li.gameData.game.gameMatch>span:nth-child(1)>span")
            print(dataHomeT.text)
            csvTemp.extend([dataHomeT.text])
            dataAwayT = driver.find_element_by_css_selector("#" + indexItems +"> li.gameData.game.gameMatch > span:nth-child(3)")
            print(dataAwayT.text)
            csvTemp.extend([dataAwayT.text])
            time.sleep(1)
            driver.find_element_by_css_selector("#" + indexItems + " li:nth-of-type(11)").click()

            time.sleep(1)

            html = driver.page_source
            soup = bs(html, 'lxml')
            title_list = soup.find_all('a', 'special')

            countArray = 0
            total = 0
            avg = 0
            for title in title_list:
                countArray += 1
                print(title.text[3:])
                total += float((title.text[3:]).replace(",","."))
                csvTemp.extend([(title.text[3:]).replace(",",".")])
                if countArray == 22:
                    avg = int(total)/22
                    break  # break here
            print(total)
            print(avg)
            csvTemp.extend([total])
            csvTemp.extend([avg])
            time.sleep(1)
            driver.find_element_by_css_selector("#" + indexItems + " li:nth-of-type(11)").click()
            time.sleep(1)
            csvData.append(csvTemp)
        except NoSuchElementException:
            continue

    print(csvData)
    time.sleep(1)
    download_dir = "example.csv"  # where you want the file to be downloaded to

    with open("new_file.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(csvData)


except NoSuchElementException:
    print(csvData)
    print('No found Element')
    time.sleep(3)
    driver.quit()