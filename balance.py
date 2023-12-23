from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests

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


date = firstRowValues[1].replace('/', ' ')
startingMonth = (int) (findRowValues(date)[0])
startingDay = (int) (findRowValues(date)[1])


todayDate = datetime.today()
currentYear = todayDate.year
startingDate = datetime(currentYear, startingMonth, startingDay)
differenceDate = todayDate - startingDate


# magic numbers
TOTAL_WEEKS = (int)(lastRowValues[0])
TOTAL_DAYS = TOTAL_WEEKS * 7
STARTING_BALANCE_APLUS = (float)(firstRowValues[2])
STARTING_BALANCE_A = (float)(firstRowValues[3])
STARTING_BALANCE_B = (float)(firstRowValues[4])
STARTING_BALANCE_C = (float)(firstRowValues[5])
STARTING_BALANCE_D = (float)(firstRowValues[6])
WEEKLYUPDATE_APLUS = STARTING_BALANCE_APLUS - (float)(secondRowValues[2])
WEEKLYUPDATE_A = STARTING_BALANCE_A - (float)(secondRowValues[3])
WEEKLYUPDATE_B = STARTING_BALANCE_B - (float)(secondRowValues[4])
WEEKLYUPDATE_C = STARTING_BALANCE_C - (float)(secondRowValues[5])
WEEKLYUPDATE_D = STARTING_BALANCE_D - (float)(secondRowValues[6])
DAILYUPDATE_APLUS = WEEKLYUPDATE_APLUS / 7
DAILYUPDATE_A = WEEKLYUPDATE_A / 7
DAILYUPDATE_B = WEEKLYUPDATE_B / 7
DAILYUPDATE_C = WEEKLYUPDATE_C / 7
DAILYUPDATE_D = WEEKLYUPDATE_D / 7
CURRENT_BALANCE_APLUS = 0.00
CURRENT_BALANCE_A = 0.00
CURRENT_BALANCE_B = 0.00
CURRENT_BALANCE_C = 0.00
CURRENT_BALANCE_D = 0.00

#calculate meal plan difference
def calculateBalance():
   global CURRENT_BALANCE_A
   global CURRENT_BALANCE_APLUS
   global CURRENT_BALANCE_B
   global CURRENT_BALANCE_C
   global CURRENT_BALANCE_D
   global differenceDate
   if differenceDate.days > TOTAL_DAYS:
       print("ZEROS")
       CURRENT_BALANCE_APLUS = 0.00
       CURRENT_BALANCE_A = 0.00
       CURRENT_BALANCE_B = 0.00
       CURRENT_BALANCE_C = 0.00
       CURRENT_BALANCE_D = 0.00
   else:
       print("NEW BALANCE")
       global STARTING_BALANCE_A
       global STARTING_BALANCE_APLUS
       global STARTING_BALANCE_B
       global STARTING_BALANCE_C
       global STARTING_BALANCE_D
       global DAILYUPDATE_A
       global DAILYUPDATE_APLUS
       global DAILYUPDATE_D
       global DAILYUPDATE_B
       global DAILYUPDATE_C
       CURRENT_BALANCE_APLUS = STARTING_BALANCE_APLUS - (DAILYUPDATE_APLUS * differenceDate.days)
       CURRENT_BALANCE_A = STARTING_BALANCE_A - (DAILYUPDATE_A * differenceDate.days)
       CURRENT_BALANCE_B = STARTING_BALANCE_B - (DAILYUPDATE_B * differenceDate.days)
       CURRENT_BALANCE_C = STARTING_BALANCE_C - (DAILYUPDATE_C * differenceDate.days)
       CURRENT_BALANCE_D = STARTING_BALANCE_D - (DAILYUPDATE_D * differenceDate.days)

# calculate balance
calculateBalance()
print(differenceDate.days)
print(TOTAL_DAYS)
print(CURRENT_BALANCE_APLUS)
print(CURRENT_BALANCE_A)
print(CURRENT_BALANCE_B)
print(CURRENT_BALANCE_C)
print(CURRENT_BALANCE_D)






from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html', CURRENT_BALANCE_APLUS = CURRENT_BALANCE_APLUS, todayDate = todayDate)

if __name__ == '__main__':
    app.run()

