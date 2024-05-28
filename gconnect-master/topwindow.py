################################################################################
#
# (C) 2021-2022, Tiago Gasiba
#                tiago.gasiba@gmail.com
#
################################################################################
from multiprocessing import Process, Value, Queue
from mainwindow import *
from fgconnect import *

class mainApp( mainWindow ):
  def __init__(self, parent):
    mainWindow.__init__(self,parent)
    self.flag1  = None
    self.flag2  = None
    self.myEvtQ = Queue(maxsize=1)
    self.AIEvtQ = Queue(maxsize=1)
    self.fgBMP.SetBitmap( wx.Bitmap.FromRGBA(15, 15, red=255, alpha=255) )
    self.lnmBMP.SetBitmap( wx.Bitmap.FromRGBA(15, 15, red=255, alpha=255) )
    
  def onClose(self,event):
    if self.flag1!=None:
      self.flag1.value = 1
      self.p0.kill()
      self.p1.kill()
      self.flag1 = None
    if self.flag2!=None:
      self.flag2.value = 1
      self.p2.kill()
      self.flag2 = None
    mainWindow.onClose(self,event)

  def evtStart1(self,event):
    if self.flag1==None:
      self.flag1 = Value("i",0)
      pCfg = { "IP_ADDR"    : self.fgIPAddr.GetValue(),
               "UDP_PORT"   : int(self.fgPortNr.GetValue()),
               "sleepTime"  : 1/10.0,
               "xmlCfgFile" : "littlenavmap.xml",
             }
      self.p1 = Process( target=processReadFromFlightGear, args=(self.flag1, self.myEvtQ, pCfg) )
      self.p1.start()
      pCfg = { "IP_ADDR"    : self.fgIPAddr.GetValue(),
               "UDP_PORT"   : 5400,
               "sleepTime"  : 1/2.0,
             }
      self.p0 = Process( target=processReadAIFromFlightGear, args=(self.flag1, self.AIEvtQ, pCfg) )
      self.p0.start()
      self.fgBMP.SetBitmap( wx.Bitmap.FromRGBA(15, 15, green=200, alpha=255) )

  def evtStop1(self,event):
    if self.flag1!=None:
      self.flag1.value = 1
      self.p0.join()
      self.p1.join()
      self.flag1 = None
      self.fgBMP.SetBitmap( wx.Bitmap.FromRGBA(15, 15, red=255, alpha=255) )

  def evtStart2(self,event):
    if self.flag2==None:
      self.flag2 = Value("i",0)
      pCfg = { "IP_ADDR"    : self.lnmIPAddr.GetValue(),
               "UDP_PORT"   : int(self.lnmPortNr.GetValue()),
               "sleepTime"  : 1/10.0,
             }
      self.p2 = Process( target=processWriteToLittleNavMap, args=(self.flag2, self.myEvtQ, self.AIEvtQ, pCfg) )
      self.p2.start()
      self.lnmBMP.SetBitmap( wx.Bitmap.FromRGBA(15, 15, green=200, alpha=255) )

  def evtStop2(self,event):
    if self.flag2!=None:
      self.flag2.value = 1
      self.p2.join()
      self.flag2 = None
      self.lnmBMP.SetBitmap( wx.Bitmap.FromRGBA(15, 15, red=255, alpha=255) )

