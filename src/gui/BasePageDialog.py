# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Sat Feb 12 19:19:32 2011

import os

import wx

import core.system
import core.factory
from core.search import TagsList

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class BasePageDialog(wx.Dialog):
	def __init__(self, parentPage = None, *args, **kwds):
		"""
		parentPage -- родительская страница (используется, если страницу нужно создавать, а не изменять)
		currentPage -- страница, которую надо изменить (используется, если страницу нужно изменять, а не создавать)
		"""
		# begin wxGlade: BasePageDialog.__init__
		kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME
		wx.Dialog.__init__(self, *args, **kwds)
		self.label_1 = wx.StaticText(self, -1, _("Title"))
		self.titleTextCtrl = wx.TextCtrl(self, -1, "")
		self.label_2 = wx.StaticText(self, -1, _("Tags (comma separated)"))
		self.tagsTextCtrl = wx.TextCtrl(self, -1, "")
		self.label_3 = wx.StaticText(self, -1, _("Page type"))
		self.comboType = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN|wx.CB_READONLY)
		self.iconsList = wx.ListCtrl(self, -1, style=wx.LC_ICON|wx.LC_AUTOARRANGE|wx.LC_SINGLE_SEL|wx.FULL_REPAINT_ON_RESIZE)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

		self.parentPage = parentPage

		self.imagesDir = core.system.getImagesDir()
		self.iconspath = os.path.join (self.imagesDir, "iconset")
		self.defaultIcon = os.path.join (self.imagesDir, "page.png")

		self._fillComboType()

		self.icons = wx.ImageList (16, 16)
		self.iconsList.AssignImageList (self.icons, wx.IMAGE_LIST_NORMAL)

		# Словарь, с помощью которого можно найти путь к файлу по элементу списка
		# Ключ - элемент списка, значение - путь к файлу
		self.iconsDict = {}
		self.makeIconsList()

		if parentPage.parent != None:
			tags = TagsList.getTagsString (parentPage.tags)
			self.tagsTextCtrl.SetValue (tags)


	def testPageTitle (self, title):
		"""
		Возвращает True, если возможно создать страницу с таким заголовком
		"""
		if ("/" in title or 
			"\\" in title or
			title.startswith ("__") or
			len (title.strip()) == 0):
			return False

		return True
	

	def makeIconsList (self):
		self.iconsList.ClearAll()
		self.icons.RemoveAll()
		self.iconsDict = {}

		# Иконка по умолчанию
		self.icons.Add (wx.Bitmap (self.defaultIcon) )
		firstItem = self.iconsList.InsertImageStringItem (0, u"page.png", 0)
		self.iconsDict[firstItem] = self.defaultIcon
		self.iconsDict[-1] = self.defaultIcon

		files = [fname for fname in os.listdir (self.iconspath)]
		files.sort()

		index = 1
		for fname in files:
			fullpath = os.path.join (self.iconspath, fname)

			if wx.Image.CanRead (fullpath):
				bitmap = wx.Bitmap (fullpath)

				# Считаем, что, если если уж CanRead вернул True, то Bitmap должен создаться без проблем
				assert bitmap.IsOk()

				self.icons.Add (bitmap)
				item = self.iconsList.InsertImageStringItem (index, fname, index)
				self.iconsDict[item] = fullpath

				index += 1
		
		self.iconsList.SetItemState (firstItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)


	def __set_properties(self):
		# begin wxGlade: BasePageDialog.__set_properties
		self.SetTitle(_("Create Page"))
		self.SetSize((500, 350))
		self.titleTextCtrl.SetMinSize((350,-1))
		self.tagsTextCtrl.SetMinSize((250, -1))
		self.iconsList.SetMinSize((500, 200))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: BasePageDialog.__do_layout
		grid_sizer_1 = wx.FlexGridSizer(5, 1, 0, 0)
		grid_sizer_4 = wx.FlexGridSizer(1, 2, 0, 0)
		grid_sizer_3 = wx.FlexGridSizer(1, 2, 0, 0)
		grid_sizer_2 = wx.FlexGridSizer(1, 2, 0, 0)
		grid_sizer_2.Add(self.label_1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
		grid_sizer_2.Add(self.titleTextCtrl, 0, wx.ALL|wx.EXPAND, 4)
		grid_sizer_2.AddGrowableCol(1)
		grid_sizer_1.Add(grid_sizer_2, 1, wx.EXPAND, 0)
		grid_sizer_3.Add(self.label_2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
		grid_sizer_3.Add(self.tagsTextCtrl, 0, wx.ALL|wx.EXPAND, 4)
		grid_sizer_3.AddGrowableCol(1)
		grid_sizer_1.Add(grid_sizer_3, 1, wx.EXPAND, 0)
		grid_sizer_4.Add(self.label_3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
		grid_sizer_4.Add(self.comboType, 0, wx.ALL|wx.EXPAND, 4)
		grid_sizer_4.AddGrowableCol(1)
		grid_sizer_1.Add(grid_sizer_4, 1, wx.EXPAND, 0)
		grid_sizer_1.Add(self.iconsList, 1, wx.ALL|wx.EXPAND, 2)
		self.SetSizer(grid_sizer_1)
		grid_sizer_1.AddGrowableRow(3)
		grid_sizer_1.AddGrowableCol(0)
		self.Layout()
		# end wxGlade
	
		self._createOkCancelButtons (grid_sizer_1)
		self.titleTextCtrl.SetFocus()
	

	def _createOkCancelButtons (self, sizer):
		# Создание кнопок Ok/Cancel
		buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)
		sizer.AddSpacer(0)
		sizer.Add (buttonsSizer, 1, wx.ALIGN_RIGHT | wx.ALL, border = 2)
		self.Bind (wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)

		sizer.Fit(self)
		self.Layout()

	
	def _fillComboType (self):
		self.comboType.Clear()
		for factory in core.factory.FactorySelector.factories:
			self.comboType.Append (factory.title, factory)

		if not self.comboType.IsEmpty():
			self.comboType.SetSelection (0)


	@property
	def selectedFactory (self):
		index = self.comboType.GetSelection()
		return self.comboType.GetClientData (index)

	@property
	def pageTitle (self):
		return self.titleTextCtrl.GetValue()

	@property
	def tags (self):
		tagsString = self.tagsTextCtrl.GetValue()
		tags = TagsList.parseTagsList (tagsString)
		return tags

	@property
	def icon (self):
		item = self.iconsList.GetNextItem (-1, state = wx.LIST_STATE_SELECTED)
		return self.iconsDict[item]
		# end wxGlade

# end of class BasePageDialog


