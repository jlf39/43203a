from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash
import lxml
from .forms import StockForm
from .charts import *


@app.route("/", methods=['GET', 'POST'])
@app.route("/stocks", methods=['GET', 'POST'])
def stocks():
    apikey = "R6OMMN6KY7H6OUY7"
    form = StockForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            #Get the form data to query the api
            symbol = request.form['symbol']
            chart_type = request.form['chart_type']
            time_series = request.form['time_series']
            start_date = convert_date(request.form['start_date'])
            end_date = convert_date(request.form['end_date'])
            print(time_series)
            if end_date <= start_date:
                #Generate error message as pass to the page
                err = "ERROR: End date cannot be earlier than Start date."
                chart = None
            else:
                #query the api using the form data
                err = None
                 
                #THIS IS WHERE YOU WILL CALL THE METHODS FROM THE CHARTS.PY FILE AND IMPLEMENT YOUR CODE
            
                data=apiRequest(time_series,symbol,apikey)
                timeseries=timeSeriesCheck(time_series)
                data1=(data[timeseries])
                data7=refineData(data1,start_date,end_date,time_series)
                
                
                
                
                #This chart variable is what is passed to the stock.html page to render the chart returned from the api
                chart = makeGraph(chart_type,data7,start_date,end_date,symbol,time_series)

            return render_template("stock.html", form=form, template="form-template", err = err, chart = chart)
    
    return render_template("stock.html", form=form, template="form-template")
