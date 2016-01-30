"""
Very simple Flask web site, with one page
displaying a course schedule.

"""

import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify # For AJAX transactions

import json
import logging

# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# Our own module
# import acp_limits
from distance import calc_duration_open
from distance import calc_duration_close

###
# Globals
###
app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/calc")
def index():
  app.logger.debug("Main page entry")
  return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("calc")
    return flask.render_template('page_not_found.html'), 404


###############
#
# AJAX request handlers 
#   These return JSON, rather than rendering pages. 
#
###############
@app.route("/_calc_times")
def calc_times():
  """
  Passes the values passed to it to 
  calc_duration_open and close  
  Expects the number of brevet_distance.
  Also Expects the current distance
  start_time and start date. 
  """
  app.logger.debug("Got a JSON request");
  cont = request.args.get('distance', 0, type=int)
  total_distance = request.args.get('total_dist', 0, type= int)
  start_time = request.args.get('start', 0, type = str)
  start_date = request.args.get('date', 0, type = str)
  
  final_date = start_date + " " + start_time
  
  ##set the date
  date = arrow.get(final_date, 'MM/DD/YYYY HH:mm')
  
  ##Calculate the date and time of distance
  open_time = calc_duration_open(cont, total_distance)
  close_time = calc_duration_close(cont, total_distance)
  
  #need to get date time to 0
  first_o = calc_duration_open(0, total_distance)
  first_c = calc_duration_close(0, total_distance)
  first_date_open = date.replace(hours=first_o[0], minutes=first_o[1]).format("MM/DD/YYYY HH:mm")
  first_date_close = date.replace(hours=first_c[0], minutes=first_c[1]).format("MM/DD/YYYY HH:mm")
  
  #now set the dates with updated times
  start_date_time = date.replace(hours=open_time[0], minutes=open_time[1])
  start_date_close = date.replace(hours=close_time[0], minutes=close_time[1])
  
  #now makestrings
  final_close = start_date_close.format("MM/DD/YYYY HH:mm")
  final_start = start_date_time.format("MM/DD/YYYY HH:mm")
  
  #pass it all back
  rslt = { "closeing": final_close, "start": final_start, 
                  "first_c": first_date_close, "first_o": first_date_open }
  return jsonify(result=rslt)
 
#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try: 
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"

@app.template_filter( 'fmttime' )
def format_arrow_time( time ):
    try: 
        normal = arrow.get( date )
        return normal.format("hh:mm")
    except:
        return "(bad time)"



#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT)

    
