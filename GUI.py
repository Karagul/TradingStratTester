# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 08:16:26 2018

@author: T58830
"""
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QComboBox, QCheckBox
import sys
import pandas as pd
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from modules import mov_avg, simulator, golden_cross, derivative_strat, mean_reversal, simulator_error_check
from bruteforce import optimizer, mov_average_optim




class Window(QtGui.QMainWindow):

  def __init__(self):
    super(Window, self).__init__()
    self.init_UI()
    
    
  def init_UI(self):
    self.save_folder = ""
    self.box = ""
    self.all_data,self.curr_data = self.readfile()
    self.setFixedSize(1200,950)
    self.dates()
    self.info()
    self.buttons()
    self.sim_list() 
    self.curr_list()
    self.add_plot()    
    self.log_flag = False
    self.setWindowTitle("SIMULATION TOOL")
    self.error = False
    self.error_box()

#    self.radio_buttons()
    
  """UI FUNCTIONS"""
  def paintEvent(self,event):
    lines = QtGui.QPainter(self)
#    pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
#    lines.setPen(pen)
    lines.begin(self)
    lines.drawRect(20,20,230,110)    
    lines.drawRect(250,20,340,110)
    lines.drawRect(620,20,560,110)
    lines.drawRect(10,10,1180,930) 
    lines.drawRect(10,149,1180,701)      
    lines.end()

    
  def info(self): #Create a label where trades stats can be appended
    self.stats_info = QtGui.QLabel(self)
    self.stats_info.setGeometry(20, 860, 300, 80)
    self.stats_info.setText("")
    
    self.brute_lab = QtGui.QLabel(self)
    self.brute_lab.setGeometry(300, 870, 300, 60)
    self.brute_lab.setText("")
  
  def error_box(self):
    self.errb = QCheckBox("Error checking", self)
    self.errb.setGeometry(1080,20,100,90)
    self.errb.setChecked(False)
    self.errb.stateChanged.connect(self.error_truth)    

    
  def dates(self): #Create date input boxes
    self.from_lab = QtGui.QLabel( self)
    self.from_lab.setGeometry( 30, 30, 71, 16 )
    self.from_lab.setText('Date from')
    self.from_edit = QtGui.QLineEdit( self)
    self.from_edit.setGeometry( 30, 50, 61, 20 )
    self.from_edit.setPlaceholderText('20170101')
    self.to_lab = QtGui.QLabel( self )
    self.to_lab.setGeometry( 120, 30, 71, 16 )
    self.to_lab.setText('Date to')
    self.to_edit = QtGui.QLineEdit( self)
    self.to_edit.setGeometry( 120, 50, 61, 20 )
    self.to_edit.setPlaceholderText('20170630')    
    
  def sim_list(self): #Create list of indices
    self.cb = QComboBox(self)
    self.cb.addItems(list(self.all_data.columns))
    self.cb.currentIndexChanged.connect(self.plot_chart)
    self.cb.setGeometry(140,80,100,40)
  
  def curr_list(self): #Create list of currrncies
    self.cl = QComboBox(self)
    self.cl.addItems(list(self.curr_data.columns))
    self.cl.setGeometry(30,80,100,40)

  def buttons(self): #Create all buttons and connect to appropiate functions
  
    #Row 1 starts

    self.a = QtGui.QPushButton('IMPLEMENT STRAT', self)   
    self.a.clicked.connect(self.tester) 
    self.a.setGeometry(260,30,100,40)
  
    self.mov = QtGui.QPushButton('Derivative', self)   
    self.mov.clicked.connect(self.deriv_strat) 
    self.mov.setGeometry(370,30,100,40)
  
    self.mov = QtGui.QPushButton('Moving Average', self)   
    self.mov.clicked.connect(self.moving_average) 
    self.mov.setGeometry(480,30,100,40)
   
    #Row 2 strats

    self.b = QtGui.QPushButton('IMPLEMENT STRAT', self)   
    self.b.clicked.connect(self.tester) 
    self.b.setGeometry(260,80,100,40)    
   
    self.gc = QtGui.QPushButton('Golden Cross', self)   
    self.gc.clicked.connect(self.gd) 
    self.gc.setGeometry(370,80,100,40)
    
    self.mr = QtGui.QPushButton('Mean Reversal', self)   
    self.mr.clicked.connect(self.mean_reversion) 
    self.mr.setGeometry(480,80,100,40)

    #Row 1 funcs

    self.mavg = QtGui.QPushButton('Moving Average\nIndex', self)   
    self.mavg.clicked.connect(self.plot_mov_avg) 
    self.mavg.setGeometry(630,30,100,40)
    
    self.log = QtGui.QPushButton('Scale', self)   
    self.log.clicked.connect(self.log_scale) 
    self.log.setGeometry(740,30,100,40)

    self.repl = QtGui.QPushButton('Reset', self)   
    self.repl.clicked.connect(self.plot_chart) 
    self.repl.setGeometry(850,30,100,40)
    
    self.sf = QtGui.QPushButton('Save Figure', self)   
    self.sf.clicked.connect(self.save_fig) 
    self.sf.setGeometry(960,30,100,40)
    
    #Row 2 funcs

    self.opt = QtGui.QPushButton('Optimal\nMoving Average', self)   
    self.opt.clicked.connect(self.brutefor) 
    self.opt.setGeometry(630,80,100,40)          
    
    self.cur = QtGui.QPushButton('Currency\nPerformance', self)   
    self.cur.clicked.connect(self.currperf) 
    self.cur.setGeometry(740,80,100,40)    
    
    self.plot = QtGui.QPushButton('Plot', self)   
    self.plot.clicked.connect(self.plot_chart_diff_curr) 
    self.plot.setGeometry(850,80,100,40)    
       
    self.sf = QtGui.QPushButton('Save Folder', self)   
    self.sf.clicked.connect(self.set_save_folder) 
    self.sf.setGeometry(960,80,100,40)
    
 
  """PLOTTING FUNCTIONS"""

  def plot_stats(self,ml): #Fetch trade stats and write to UI
    print(ml)
    trades = int(ml[0])
    avg    = int(ml[1])
    maxval = int(ml[2])
    minval = int(ml[3])
    med    = int(ml[4])
    text = "Amount of trades: %.1f \nAverage amount of days between trades: %.1f \nMedian amount of days between trades: %.1f \nLongest period of days between trades: %.1f \nShortest amount of days between trades: %.1f" % (trades,med,avg,maxval,minval)
    print(self.error)
    if self.error:
      errnum = ml[5]
      text2 = "\nAmount of error trades: %d" % errnum
      text = text + text2
      print(text)
    self.stats_info.setText(text)

  def add_plot(self):  #Intialise matplotlib in the UI
    currency = self.cl.currentText()
    index = self.cb.currentText()
    self.figure = Figure() #Create fig
    self.canvas = FigureCanvasQTAgg(self.figure)
    self.canvas.setParent(self)
    self.canvas.setGeometry(11,150,1179,700)
    self.axis = self.figure.add_subplot(111)
    self.axis.set_xlabel("")
    self.axis.legend(loc =2) 
    to_plot = self.all_data[self.cb.currentText()] #Plotting data is first item in list
    
    to_plot = self.reindex(to_plot)    #Plot from 100
    self.first_date = to_plot.index[0] #Set universal variable for currency plotting
    
    text = index + " " + currency
    self.plotter(to_plot, text)  #Plot
    
  def plot_strat(self,to_plot,name): #Plot each individual strategy (E.g movin avg)
    currency = self.cl.currentText()
    to_plot = self.date_cut(to_plot)           
    to_plot = self.to_series(to_plot)
    to_plot = self.reindex(to_plot)
    text = name+ " " +currency
    self.plotter(to_plot, text)  

  def plot_chart(self): #Plot a new base chart and clear everything
    self.cl.setCurrentIndex(0)
    currency = self.cl.currentText()
    column = self.cb.currentText()
    all_curr_data = self.curr_data[currency]
    to_plot = self.all_data[column]
    to_plot = to_plot.dropna()


    to_plot = self.date_cut(to_plot)
    all_curr_data = self.date_cut(all_curr_data)

    to_plot = self.to_series(to_plot)
    all_curr_data = self.to_series(all_curr_data)
    to_plot = to_plot.div(all_curr_data)

    to_plot = self.reindex(to_plot)
    self.first_date = to_plot.index[0]
    
    self.axis.clear()
    text = column+ " " +currency
    self.plotter(to_plot, text)  
    self.stats_info.setText("")
  
  def plot_chart_diff_curr(self): #Plot base chart in a different curenncy
    currency = self.cl.currentText()
    column = self.cb.currentText()
    all_curr_data = self.curr_data[currency]
    to_plot = self.all_data[column]
    to_plot = to_plot.dropna()
    to_plot = self.date_cut(to_plot)
    all_curr_data = self.date_cut(all_curr_data)
    to_plot = self.to_series(to_plot)
    all_curr_data = self.to_series(all_curr_data)
    
    to_plot = to_plot.div(all_curr_data)
    
    to_plot = self.reindex(to_plot)
    
    
    text = column +" "+ currency
    self.plotter(to_plot, text)
    

  def currperf(self):
    currency = self.cl.currentText()    
    curr = self.curr_data[currency]
    to_plot = curr
    to_plot = self.date_cut(to_plot)
    to_plot = to_plot.truncate(before = self.first_date)
    to_plot = self.reindex(to_plot)
    text =  "USD : " + currency
    self.plotter(to_plot, text)
  
  def plot_mov_avg(self):
    currency = self.cl.currentText()
    curr = self.curr_data[currency]
    column = self.cb.currentText()
    number   = self.getint("Enter moving average")
    text = "%s %s %d Moving Average" % (column, currency, number)
    data = self.all_data[column]
    data = data.div(curr)
    data = data.dropna()
    to_plot = data.rolling(window=number).mean()
    
    if self.from_edit.text() != '' and self.from_edit.text() != '':
      to_plot = self.date_cut(to_plot)
    else:
      to_plot = to_plot.truncate(before = self.first_date)
    
    firstval = self.to_series(self.date_cut(self.all_data[column].div(curr))).dropna()[0]    
    print(firstval)
    to_plot = self.to_series(to_plot)
    to_plot = to_plot/firstval*100
    self.plotter(to_plot, text)
    
  def plotter(self,to_plot,text): #Plots to_plot on plot
    self.axis.plot(to_plot,label = text)
    self.axis.legend(loc =2)
    self.canvas.draw()
  
  """Strategies"""

  def mean_reversion(self):
   currency = self.cl.currentText()
   curr = self.curr_data[currency]
   column = self.cb.currentText()
   func = mean_reversal
   nr_stdev = self.getfloat("Number of standard deviations")
   number   = self.getint("Enter moving average")
   text = " " + str(nr_stdev) +" Deviation - Mean Reversion"
   data = self.all_data[column]
   signals,diffs = func(data, number, curr, nr_stdev)
   
   self.simulate(data, number, curr, text, signals, diffs)
  
  def moving_average(self):
    func = mov_avg
    self.strats(func)
  
  def gd(self):    
    func = golden_cross
    text = ":50 GC"
    self.strats(func, text)
      
  def deriv_strat(self):
    func = derivative_strat
    text = ":200 Derivative"
    self.strats(func, text)
    
  def brutefor(self):     #Find the best moving avarge
    lower  = self.getint("Enter lower bound")
    upper  = self.getint("Enter upper bound")
    self.complaint_box("This might take a while...\n")
    currency = self.cl.currentText()
    curr = self.curr_data[currency]
    column = self.cb.currentText()
    data = self.all_data[column]
    data = optimizer(column, currency, data, curr,lower,upper)
    print(data)
    self.bruteplot(data)
  
  def strats(self,func, text = "", number = 200):
    currency = self.cl.currentText()
    curr = self.curr_data[currency]
    column = self.cb.currentText()
    if number == 200:
      number = self.getint("Enter moving average")
    data = self.all_data[column]
    signals,diffs = func(data, number, curr)
    if self.error:
      self.error_checking(data, number, curr, text,signals,diffs)
    else:
      self.simulate(data, number, curr, text,signals,diffs)
        
  def simulate(self,data, number, curr, text,signals,diffs):
    if self.from_edit.text() != '' and self.from_edit.text() != '':
      signals = self.date_cut(signals)
    signals = self.to_series(signals)
    to_plot, masterlist = simulator(data,signals,diffs,curr)
    text = str(number) + text 
    self.plot_strat(to_plot,text)
    self.plot_stats(masterlist)
 
  def error_checking(self,data, number, curr, text,signals,diffs):
    print("ERROR CHECK")
    if self.from_edit.text() != '' and self.from_edit.text() != '':
      signals = self.date_cut(signals)
    signals = self.to_series(signals)
    errnum = self.getint("Enter days for error check")
    to_plot, masterlist, days_between_trades = simulator_error_check(data,signals,diffs,curr,errnum)
    text = str(number) + text 
    self.plot_strat(to_plot,text)
    self.plot_stats(masterlist)
    self.histogram(days_between_trades)

  
  """Underlying UI"""
  def histogram(self, data):
    print('test')
    window = QtGui.QMainWindow(self)
    window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    window.setWindowTitle(self.tr('Histogram'))
    window.setFixedSize(600,600)
    figure = Figure() #Create fig
    canvas = FigureCanvasQTAgg(figure)
    canvas.setParent(window)
    canvas.setGeometry(10,10,580,580)
    ax = figure.add_subplot(111)   
    ax.hist(data, 100)
    canvas.draw()
    window.show()
   
  def bruteplot(self, data):

    window = QtGui.QMainWindow(self)
    window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    window.setWindowTitle(self.tr('Best Moving Average'))
    window.setFixedSize(1000,600)
    figure = Figure() #Create fig
    canvas = FigureCanvasQTAgg(figure)
    canvas.setParent(window)
    canvas.setGeometry(10,10,980,580)
    ax = figure.add_subplot(111)   
    ax.plot(data)
    canvas.draw()
    window.show()
    
  def set_save_folder( self ): 
    self.save_folder = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
    return None
    
  def complaint_box(self,text):   #Create an angry box when users f**** up
    error_dialog = QtGui.QErrorMessage(self)
    error_dialog.setWindowModality(QtCore.Qt.WindowModal)
    error_dialog.showMessage(text)

  def getint(self,text):
    print(text)
    num,ok = QtGui.QInputDialog.getInt(self,"Integer Input",text)	
    if ok:
      print(num)
      return num
      
  def getfloat(self,text):
    print(text)
    num,ok = QtGui.QInputDialog.getDouble(self,"Float Input",text)	
    if ok:
      print(num)
      return num

  def save_fig(self): #Save figure
    if self.save_folder != "":
      self.figure.savefig(self.save_folder +'/test.png')
      self.complaint_box('Figure saved in ' + self.save_folder)
    else:
      self.complaint_box('Choose a folder to save in')  

  def log_scale(self):
    if self.log_flag:           #Change y-scale to linear
      self.axis.set_yscale('linear')
      self.log_flag = False
      self.canvas.draw() 
    else:                       #Change y-scale to log
      self.axis.set_yscale('log')

      self.log_flag = True
      self.canvas.draw()
   
  def error_truth(self):        #Inlcude error stats or not
    self.error = not self.error
      
  """Short data funtions"""
  def reindex(self,data):
    data = self.to_series(data)
    data = data.dropna()
    data = data/data[0]*100
    return data
  
  def to_series(self,data): #If input is pandas DF, return series based on first columns. 
    if isinstance(data, pd.DataFrame): 
      data = data[data.columns[0]]
    return data
        
  def date_cut(self,data): #Cut datframe to specified dates 
    if self.from_edit.text() != '' and self.from_edit.text() != '': #Check input boxes
      if not isinstance(data, pd.DataFrame): #Make sire input actually is a dataframe
        data = data.to_frame()    
      try:
        data.index = data.index.to_datetime()
        from_date = pd.to_datetime(str(self.from_edit.text()), format='%Y%m%d')
        to_date   = pd.to_datetime(str(self.to_edit.text()), format='%Y%m%d')
        data = data.truncate(before = from_date, after = to_date)               #Cut
      except:
        err = sys.exc_info()[0]
        err2 = sys.exc_info()[1]
        print(err, err2)
        self.complaint_box("Invalid date, plotting all \n The index starts " + data.index[0] + " and ends " + data.index[-1] + ".")
    return data
    
  def readfile(self): #Read input data
    data = pd.read_excel("file path to index data")
#    data.index = data.index.to_datetime()
    curr_data = pd.read_excel("file path to currency data")
#    curr_data.index = data.index.to_datetime()
    return data, curr_data    
   
  def tester(self): #Test function for UI elemtents
    print("Something happens")
    
    
    
app = QtGui.QApplication(sys.argv)
GUI = Window()
GUI.show()
sys.exit(app.exec_())


