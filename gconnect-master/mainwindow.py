# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class mainWindow
###########################################################################

class mainWindow ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"fgConnect", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Flight Gear Connection", wx.DefaultPosition, wx.Size( 460,-1 ), 0 )
		self.m_staticText1.Wrap( -1 )

		self.m_staticText1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

		bSizer6.Add( self.m_staticText1, 0, wx.ALL, 5 )

		self.fgBMP = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 15,15 ), 0 )
		self.fgBMP.SetMinSize( wx.Size( 15,15 ) )
		self.fgBMP.SetMaxSize( wx.Size( 15,15 ) )

		bSizer6.Add( self.fgBMP, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer6, 1, wx.EXPAND, 5 )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Start/Stop", wx.DefaultPosition, wx.Size( 180,-1 ), wx.ALIGN_CENTER_HORIZONTAL )
		self.m_staticText11.Wrap( -1 )

		self.m_staticText11.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer61.Add( self.m_staticText11, 0, wx.ALL, 5 )

		self.m_staticText111 = wx.StaticText( self, wx.ID_ANY, u"IP Address", wx.DefaultPosition, wx.Size( 200,-1 ), wx.ALIGN_CENTER_HORIZONTAL )
		self.m_staticText111.Wrap( -1 )

		self.m_staticText111.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer61.Add( self.m_staticText111, 0, wx.ALL, 5 )

		self.m_staticText1111 = wx.StaticText( self, wx.ID_ANY, u"Port", wx.DefaultPosition, wx.Size( 80,-1 ), wx.ALIGN_CENTER_HORIZONTAL )
		self.m_staticText1111.Wrap( -1 )

		self.m_staticText1111.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer61.Add( self.m_staticText1111, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer61, 1, wx.EXPAND, 5 )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button1 = wx.Button( self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button1, 0, wx.ALL, 5 )

		self.m_button2 = wx.Button( self, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button2, 0, wx.ALL, 5 )

		self.fgIPAddr = wx.TextCtrl( self, wx.ID_ANY, u"127.0.0.1", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		bSizer2.Add( self.fgIPAddr, 0, wx.ALL, 5 )

		self.fgPortNr = wx.TextCtrl( self, wx.ID_ANY, u"7755", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.fgPortNr, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"LittleNavMap Connection", wx.DefaultPosition, wx.Size( 460,-1 ), 0 )
		self.m_staticText2.Wrap( -1 )

		self.m_staticText2.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

		bSizer7.Add( self.m_staticText2, 0, wx.ALL, 5 )

		self.lnmBMP = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 15,15 ), 0 )
		self.lnmBMP.SetMinSize( wx.Size( 15,15 ) )
		self.lnmBMP.SetMaxSize( wx.Size( 15,15 ) )

		bSizer7.Add( self.lnmBMP, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer7, 1, wx.EXPAND, 5 )

		bSizer611 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText112 = wx.StaticText( self, wx.ID_ANY, u"Start/Stop", wx.DefaultPosition, wx.Size( 180,-1 ), wx.ALIGN_CENTER_HORIZONTAL )
		self.m_staticText112.Wrap( -1 )

		self.m_staticText112.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer611.Add( self.m_staticText112, 0, wx.ALL, 5 )

		self.m_staticText1112 = wx.StaticText( self, wx.ID_ANY, u"IP Address", wx.DefaultPosition, wx.Size( 200,-1 ), wx.ALIGN_CENTER_HORIZONTAL )
		self.m_staticText1112.Wrap( -1 )

		self.m_staticText1112.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer611.Add( self.m_staticText1112, 0, wx.ALL, 5 )

		self.m_staticText11111 = wx.StaticText( self, wx.ID_ANY, u"Port", wx.DefaultPosition, wx.Size( 80,-1 ), wx.ALIGN_CENTER_HORIZONTAL )
		self.m_staticText11111.Wrap( -1 )

		self.m_staticText11111.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer611.Add( self.m_staticText11111, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer611, 1, wx.EXPAND, 5 )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button3 = wx.Button( self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_button3, 0, wx.ALL, 5 )

		self.m_button4 = wx.Button( self, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_button4, 0, wx.ALL, 5 )

		self.lnmIPAddr = wx.TextCtrl( self, wx.ID_ANY, u"127.0.0.1", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		bSizer3.Add( self.lnmIPAddr, 0, wx.ALL, 5 )

		self.lnmPortNr = wx.TextCtrl( self, wx.ID_ANY, u"51968", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.lnmPortNr, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer3, 10, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.onClose )
		self.m_button1.Bind( wx.EVT_BUTTON, self.evtStart1 )
		self.m_button2.Bind( wx.EVT_BUTTON, self.evtStop1 )
		self.m_button3.Bind( wx.EVT_BUTTON, self.evtStart2 )
		self.m_button4.Bind( wx.EVT_BUTTON, self.evtStop2 )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def onClose( self, event ):
		event.Skip()

	def evtStart1( self, event ):
		event.Skip()

	def evtStop1( self, event ):
		event.Skip()

	def evtStart2( self, event ):
		event.Skip()

	def evtStop2( self, event ):
		event.Skip()


