from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests

# global variables
CURRENT_BALANCE_APLUS = 0.00
CURRENT_BALANCE_A = 0.00
CURRENT_BALANCE_B = 0.00
CURRENT_BALANCE_C = 0.00
CURRENT_BALANCE_D = 0.00
todayDate = datetime.today()
format = "%a %b %d %Y"
fullDate = todayDate.strftime(format)
diffDate = 1

# puts all values of rows into a list of strings
def findRowValues(row_string):
    rowValues = []
    starting = -1
    while row_string.find(' ', starting +1) != -1:
        ending = row_string.find(' ', starting + 1)
        rowValues.append(row_string[(starting +1 ):ending])
        starting = ending
    rowValues.append(row_string[starting + 1:])
    return rowValues

# scrapes the website for the data rows
def scrapeWebsite():
    url_balance = requests.get('https://www.oxy.edu/student-life/campus-dining/meal-plans/check-your-balance').text
    url_soup = BeautifulSoup(url_balance, 'lxml')
    balance_table = url_soup.find('table')
    rows = balance_table.find_all('tr')

    firstRow = rows[2].text.strip().replace('\n', ' ').replace(',', '')
    secondRow= rows[3].text.strip().replace('\n', ' ').replace(',', '')
    lastRow = rows[-1].text.strip().replace('\n', ' ').replace(',', '')

    firstRowValues = findRowValues(firstRow)
    secondRowValues = findRowValues(secondRow)
    lastRowValues = findRowValues(lastRow)

    return firstRowValues, secondRowValues, lastRowValues

#calculate meal plan difference
def calculateBalance(differenceDate, firstRowValues, secondRowValues, lastRowValues):
    totalWeeks = (int)(lastRowValues[0])
    totalDays = totalWeeks * 7

    startingBalanceAPlus = (float)(firstRowValues[2])
    startingBalanceA = (float)(firstRowValues[3])
    startingBalanceB = (float)(firstRowValues[4])
    startingBalanceC = (float)(firstRowValues[5])
    startingBalanceD = (float)(firstRowValues[6])

    weeklyUpdateAPlus = startingBalanceAPlus - (float)(secondRowValues[2])
    weeklyUpdateA = startingBalanceA - (float)(secondRowValues[3])
    weeklyUpdateB = startingBalanceB - (float)(secondRowValues[4])
    weeklyUpdateC = startingBalanceC - (float)(secondRowValues[5])
    weeklyUpdateD = startingBalanceD - (float)(secondRowValues[6])

    dailyUpdateAPlus = weeklyUpdateAPlus / 7
    dailyUpdateA = weeklyUpdateA / 7
    dailyUpdateB = weeklyUpdateB / 7
    dailyUpdateC = weeklyUpdateC / 7
    dailyupdateD = weeklyUpdateD / 7

    if differenceDate.days > totalDays or differenceDate.days < 0:
        currentBalanceAPlus = 1000.12
        currentBalanceA = 0.00
        currentBalanceB = 0.00
        currentBalanceC = 0.00
        currentBalanceD = 0.00
    else:
        currentBalanceAPlus = startingBalanceAPlus - (dailyUpdateAPlus * differenceDate.days)
        currentBalanceA = startingBalanceA - (dailyUpdateA * differenceDate.days)
        currentBalanceB = startingBalanceB - (dailyUpdateB * differenceDate.days)
        currentBalanceC = startingBalanceC - (dailyUpdateC * differenceDate.days)
        currentBalanceD = startingBalanceD - (dailyupdateD * differenceDate.days)

    roundedBalanceAPlus = round(currentBalanceAPlus, 2)
    roundedBalanceA = round(currentBalanceA, 2)
    roundedBalanceB = round(currentBalanceB, 2)
    roundedBalanceC = round(currentBalanceC, 2)
    roundedBalanceD = round(currentBalanceD, 2)

    return roundedBalanceAPlus, roundedBalanceA, roundedBalanceB, roundedBalanceC, roundedBalanceD

def main():
    global CURRENT_BALANCE_APLUS, CURRENT_BALANCE_A, CURRENT_BALANCE_B, CURRENT_BALANCE_C, CURRENT_BALANCE_D

    currentYear = todayDate.year

    firstRowValues, secondRowValues, lastRowValues = scrapeWebsite()

    date = firstRowValues[1].replace('/', ' ')
    startingMonth = (int) (findRowValues(date)[0])
    startingDay = (int) (findRowValues(date)[1])

    startingDate = datetime(currentYear, startingMonth, startingDay)
    differenceDate = todayDate - startingDate

    global diffDate
    diffDate = differenceDate

    CURRENT_BALANCE_APLUS, CURRENT_BALANCE_A, CURRENT_BALANCE_B, CURRENT_BALANCE_C, CURRENT_BALANCE_D = calculateBalance(differenceDate, firstRowValues, secondRowValues, lastRowValues)

from flask import Flask, render_template
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def hello():
    return render_template('index.html', CURRENT_BALANCE_APLUS = CURRENT_BALANCE_APLUS, CURRENT_BALANCE_A = CURRENT_BALANCE_A, CURRENT_BALANCE_B = CURRENT_BALANCE_B, CURRENT_BALANCE_C = CURRENT_BALANCE_C, CURRENT_BALANCE_D = CURRENT_BALANCE_D, todayDate = fullDate, diffDate = diffDate)

if __name__ == "__main__":
    main()
    app.run()

