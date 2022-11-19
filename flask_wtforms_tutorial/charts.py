'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
import requests
from datetime import datetime
from datetime import date
import lxml
import pygal

def apiRequest(function,symbol,apikey):
    if function == "1":
        url= 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+symbol+'&interval=60min&outputsize=full&apikey=('+apikey+')'
        r = requests.get(url)
        data = r.json()
        return data
    if function == "2":
        url= 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+symbol+'&outputsize=full&apikey=('+apikey+')'
        r = requests.get(url)
        data = r.json()
        return data
    if function == "3":
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol='+symbol+'&outputsize=full&apikey=('+apikey+')'
        r = requests.get(url)
        data = r.json()
        return data
    if function == "4":
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='+symbol+'&outputsize=full&apikey=('+apikey+')'
        r = requests.get(url)
        data = r.json()
        return data

def refineData(data,bd,ed,function):
    list1=[]
    format1=""
    if function == "1":
        format1= '%Y-%m-%d %H:%M:%S'
        bd=bd+' 00:00:00'
        ed=ed+' 00:00:00'
    else:
        format1 = '%Y-%m-%d'
    for item in data:
        x = convert_date(str(item))
        x1 = convert_date(str(bd))
        x2 = convert_date(str(ed))
        #print(item)
        if (x < x2 or x == x2) and( x > x1 or x == x1):
            open1=float(data[item]['1. open'])
            high=float(data[item]['2. high'])
            low=float(data[item]['3. low'])
            close=float(data[item]['4. close'])
            volume=float(data[item]['5. volume'])
            date=item
            #print(date)
            temp = midtermstruct(open1,high,low,close,volume,date)
            list1.append(temp)
        else:
            continue
    return list1
def timeSeriesCheck(function):
    timeSeries=''
    if function == "1":
        timeSeries = 'Time Series (60min)'
    if function == "2":
        timeSeries = 'Time Series (Daily)'
    if function == "3":
        timeSeries = 'Weekly Time Series'
    if function == "4":
        timeSeries = 'Monthly Time Series'
    return timeSeries

def makeGraph(choice,data6,lowDate,highDate,symbol,function):
    open2=[]
    high1=[]
    low1=[]
    close1=[]
    volume1=[]
    date1=[]
    if choice == "2":
        chart=pygal.Line(x_label_rotation=45)
    if choice == "1":
        chart=pygal.Bar(x_label_rotation=45)
    for item in data6:
        temp = item.getOpen()
        open2.append(temp)
        temp = item.getHigh()
        high1.append(temp)
        temp = item.getLow()
        low1.append(temp)
        temp=item.getClose()
        close1.append(temp)
        temp=item.getVolume()
        volume1.append(temp)
        temp=item.getDate()
        date1.append(temp)
    chart.title = ''+symbol+' stock data from '+str(lowDate)+' to ' +str(highDate)+''
    temp10=date1
    temp10.reverse()
    if function == "1":
        lowDate = lowDate + ' 00:00:00'
    if choice != "1":
        lowDate = lowDate
    temp10.insert(0,lowDate)
    chart.x_labels = temp10                                                                      
    chart.add('Open',open2)
    chart.add('High',high1)
    chart.add('Low',low1)
    chart.add('Close',close1)
    chart_data = chart.render_data_uri()
    return chart_data
#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()

class midtermstruct:
    def __init__(self,open1,high,low,close,volume,date):
        self.__open1=open1
        self.__high=high
        self.__low=low
        self.__close=close
        self.__volume=volume
        self.__date=date
    def getOpen(self):
        return self.__open1
    def getHigh(self):
        return self.__high
    def getLow(self):
        return self.__low
    def getClose(self):
        return self.__close
    def getVolume(self):
        return self.__volume
    def getDate(self):
        return self.__date

class midtermstructcont:
    def __init__(self,stocksymbol,name):
        self.__stocksymbol=stocksymbol
        self.__name=name
    def getstocksymbol(self):
        return self.__stocksymbol
    def getName(self):
        return self.__name
