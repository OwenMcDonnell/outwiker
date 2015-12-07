# -*- coding: UTF-8 -*-

from threading import Event, Thread

import wx

from outwiker.core.tagslist import TagsList
from outwiker.gui.testeddialog import TestedDialog
from outwiker.gui.tagsselector import TagsSelector
from outwiker.core.commands import MessageBox

UpdateLogEvent, EVT_UPDATE_LOG = wx.lib.newevent.NewEvent()
FinishDownloadEvent, EVT_FINISH_DOWNLOAD = wx.lib.newevent.NewEvent()


class DownloadDialog (TestedDialog):
    def __init__ (self, parent):
        super (DownloadDialog, self).__init__ (parent)
        self._createGui()
        self.urlText.SetFocus()


    def _createGui (self):
        mainSizer = wx.FlexGridSizer (cols=1)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (1)
        mainSizer.AddGrowableRow (2)

        self._addUrlGui (mainSizer)
        self._addTagsList (mainSizer)
        self._addLogGui (mainSizer)
        self._addOkCancel (mainSizer)

        self.SetSizer (mainSizer)
        self.SetTitle (_(u'Download page'))
        self.SetMinSize ((500, 350))
        self.Fit()


    def _addUrlGui (self, mainSizer):
        urlSizer = wx.FlexGridSizer (cols=2)
        urlSizer.AddGrowableCol (1)

        urlLabel = wx.StaticText (self, label = _(u'Link'))
        self.urlText = wx.TextCtrl (self)

        urlSizer.Add (urlLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        urlSizer.Add (self.urlText, 0, wx.ALL | wx.EXPAND, border=2)

        mainSizer.Add (urlSizer, 0, wx.ALL | wx.EXPAND, border=2)


    def _addTagsList (self, mainSizer):
        self.tagsSelector = TagsSelector (self)
        mainSizer.Add (self.tagsSelector, 0, wx.EXPAND, 0)


    def _addLogGui (self, mainSizer):
        self.logText = wx.TextCtrl (self,
                                    style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.logText.SetMinSize ((-1, 100))
        mainSizer.Add (self.logText, 0, wx.EXPAND, 0)


    def _addOkCancel (self, mainSizer):
        buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        mainSizer.Add (buttonsSizer,
                       0,
                       wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL,
                       border = 4)


    def setTagsList (self, tagslist):
        self.tagsSelector.setTagsList (tagslist)



class DownloadDialogController (object):
    def __init__ (self, dialog, application):
        self._dialog = dialog
        self._application = application

        self._runEvent = Event()
        self._thread = None

        self._dialog.Bind (wx.EVT_BUTTON, self._onOk, id=wx.ID_OK)
        self._dialog.Bind (wx.EVT_BUTTON, self._onCancel, id=wx.ID_CANCEL)
        self._dialog.Bind (EVT_UPDATE_LOG, self._onLogUpdate)


    def showDialog (self):
        """
        The method show the dialog and return result of the ShowModal() method
        """
        if self._application.wikiroot is None:
            return

        self._loadState()

        result = self._dialog.ShowModal()
        if result == wx.ID_OK:
            self._saveState()

        return result


    def _loadState (self):
        tagslist = TagsList (self._application.wikiroot)
        self._dialog.setTagsList (tagslist)


    def _saveState (self):
        pass


    def _onLogUpdate (self, event):
        self._dialog.logText.Value += event.text

        count = len (self._dialog.logText.Value)
        self._dialog.logText.SetSelection (count, count)
        self._dialog.logText.SetFocus()


    def _onOk (self, event):
        if len (self._dialog.urlText.Value.strip()) == 0:
            MessageBox (_(u'Enter url for downloading'),
                        _(u"Error"),
                        wx.ICON_ERROR | wx.OK)
            self._dialog.urlText.SetFocus()
            return

        if self._thread is None:
            self._runEvent.clear()
            self._thread = DownloadThread (self._dialog, self._runEvent)
            self._thread.start()
        elif self._thread is not None:
            event.Skip()


    def _onCancel (self, event):
        self._runEvent.set()
        if self._thread is not None:
            self._thread.join()

        event.Skip()



class DownloadThread (Thread):
    def __init__ (self, parentWnd, runEvent, name=None):
        super (DownloadThread, self).__init__ (name=name)
        self._parentWnd = parentWnd
        self._runEvent = runEvent


    def run (self):
        self._updateLog (_(u'Start download\n'))


    def _updateLog (self, text):
        event = UpdateLogEvent (text=text)
        wx.PostEvent (self._parentWnd, event)