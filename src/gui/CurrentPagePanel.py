# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Sat Apr 10 19:07:28 2010

import os.path
import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

from core.controller import Controller
from core.factory import FactorySelector
import core.commands
from core.tree import RootWikiPage
from gui.AttachPanel import AttachPanel
from core.search import TagsList
import core.system


class CurrentPagePanel(wx.Panel):
	def __init__(self, *args, **kwds):
		self.pageView = None

		self.imagesDir = core.system.getImagesDir()
		
		self.grayStarImage = os.path.join (self.imagesDir, "star_gray.png")
		self.goldStarImage = os.path.join (self.imagesDir, "star.png")

		# begin wxGlade: CurrentPagePanel.__init__
		kwds["style"] = wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self.bookmarkBitmap = wx.BitmapButton(self, -1, wx.Bitmap(os.path.join (self.imagesDir, "star_gray.png"), wx.BITMAP_TYPE_ANY))
		self.titleLabel = wx.StaticText(self, -1, "")
		self.tagsLabel = wx.StaticText(self, -1, "[]")
		self.attachPAnel = AttachPanel(self, -1)

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_BUTTON, self.onBookmark, self.bookmarkBitmap)
		# end wxGlade

		self.currentPage = None

		Controller.instance().onPageSelect += self.onPageSelect
		Controller.instance().onPageUpdate += self.onPageUpdate
		Controller.instance().onBookmarksChanged += self.onBookmarksChanged

		self.Bind (wx.EVT_CLOSE, self.onClose)

	
	def onClose (self, event):
		if self.pageView != None:
			self.pageView.removeGui ()
			self.pageView.Close()
		self.Destroy()


	def onPageSelect (self, page):
		"""
		Событие при выборе страницы
		"""
		self.Freeze()
		self.destroyPageView()

		self.currentPage = page
		self.updatePageInfo (page)
		self.updatePageView (page)
		self.Thaw()


	def onPageUpdate (self, page):
		if self.currentPage != None and self.currentPage == page:
			self.updatePageInfo (page)
	

	def updateBookmarkBtn (self):
		imagePath = self.grayStarImage

		if self.currentPage != None and self.currentPage.root.bookmarks.pageMarked (self.currentPage):
			imagePath = self.goldStarImage

		self.bookmarkBitmap.SetBitmapLabel (wx.Bitmap(imagePath, wx.BITMAP_TYPE_ANY))


	def onBookmarksChanged (self, bookmarks):
		self.updateBookmarkBtn()


	def updatePageView (self, page):
		"""
		Обновить вид страницы
		"""
		if page != None:
			factory = FactorySelector.getFactory (page)
			self.pageView = factory.getPageView (page, self)

			assert self.pageView != None

			self.contentSizer.Add (self.pageView, 1, wx.EXPAND, 0)
			self.Layout()

			self.pageView.initGui(wx.GetApp().GetTopWindow() )


	def updatePageInfo (self, page):
		"""
		Обновить информацию о странице
		"""
		if page != None:
			title = "%s" % (page.title)
			self.titleLabel.SetLabel (title)

			tags = "[%s]" % TagsList.getTagsString (page.tags)
			self.tagsLabel.SetLabel (tags)

			self.updateBookmarkBtn()
		else:
			self.titleLabel.SetLabel (u"")
			self.tagsLabel.SetLabel (u"[]")

	
	def __set_properties(self):
		# begin wxGlade: CurrentPagePanel.__set_properties
		self.bookmarkBitmap.SetSize(self.bookmarkBitmap.GetBestSize())
		self.titleLabel.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
		self.tagsLabel.SetFont(wx.Font(12, wx.MODERN, wx.ITALIC, wx.NORMAL, 0, ""))
		self.attachPAnel.SetMinSize((-1, 150))
		# end wxGlade


	def __do_layout(self):
		# begin wxGlade: CurrentPagePanel.__do_layout
		mainSizer = wx.FlexGridSizer(3, 1, 0, 0)
		attachSizer = wx.FlexGridSizer(1, 1, 0, 0)
		contentSizer = wx.FlexGridSizer(1, 1, 0, 0)
		titleSizer = wx.FlexGridSizer(1, 3, 0, 0)
		titleSizer.Add(self.bookmarkBitmap, 0, 0, 0)
		titleSizer.Add(self.titleLabel, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
		titleSizer.Add(self.tagsLabel, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
		mainSizer.Add(titleSizer, 1, wx.EXPAND, 0)
		contentSizer.AddGrowableRow(0)
		contentSizer.AddGrowableCol(0)
		mainSizer.Add(contentSizer, 1, wx.EXPAND, 0)
		attachSizer.Add(self.attachPAnel, 1, wx.EXPAND, 0)
		attachSizer.AddGrowableRow(0)
		attachSizer.AddGrowableCol(0)
		mainSizer.Add(attachSizer, 1, wx.EXPAND, 0)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		mainSizer.AddGrowableRow(1)
		mainSizer.AddGrowableCol(0)
		# end wxGlade

		self.contentSizer = contentSizer

		#if self.pageView != None:
		#	contentSizer.Add (self.pageView, 1, wx.EXPAND, 0)

		#self.Layout()
		#self.GetParent().Layout()


	def destroyPageView (self):
		"""
		Уничтожить текущий контрол
		"""
		if self.pageView != None:
			self.contentSizer.Detach (self.pageView)
			self.pageView.Hide()
			self.pageView.removeGui()
			self.pageView.Close()
			#self.pageView.Destroy()
			self.pageView = None
			#self.__do_layout()

	
	def destroyWithoutSave (self):
		"""
		Уничтожить панель без сохранения изменений.
		Нужно для перезагрузки вики
		"""
		if self.pageView != None:
			self.contentSizer.Detach (self.pageView)
			#self.pageView.Destroy()
			self.pageView.removeGui()
			self.pageView.Hide()
			self.pageView = None
			#self.__do_layout()
	

	def Save (self):
		"""
		Сохранить текущую страницу
		"""
		if self.pageView != None:
			self.pageView.Save()


	def onBookmark(self, event): # wxGlade: CurrentPagePanel.<event_handler>
		if self.currentPage != None:
			if not self.currentPage.root.bookmarks.pageMarked (self.currentPage):
				self.currentPage.root.bookmarks.add (self.currentPage)
			else:
				self.currentPage.root.bookmarks.remove (self.currentPage)


# end of class CurrentPagePanel


