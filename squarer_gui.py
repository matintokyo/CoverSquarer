#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.1.0a2 on Tue Jun  4 21:32:42 2024
#

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
import dropable as xw
# end wxGlade


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((600, 200))
        self.SetTitle("Squarer")

        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusWidths([-1])

        self.notebook_1 = wx.Notebook(self, wx.ID_ANY)

        self.single_tab = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.notebook_1.AddPage(self.single_tab, u"単一")

        sizer_6 = wx.BoxSizer(wx.VERTICAL)

        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6.Add(sizer_7, 0, wx.ALL | wx.EXPAND, 5)

        label_copy = wx.StaticText(self.single_tab, wx.ID_ANY, u"対象画像:")
        label_copy.SetMinSize((100, -1))
        sizer_7.Add(label_copy, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.input_file_picker = xw.DropableFilePickerCtrl(self.single_tab, wx.ID_ANY)
        sizer_7.Add(self.input_file_picker, 1, wx.EXPAND, 0)

        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6.Add(sizer_10, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.single_go_button = wx.Button(self.single_tab, wx.ID_ANY, u"実行")
        sizer_10.Add(self.single_go_button, 0, wx.RIGHT, 0)

        self.show_single_file_button = wx.Button(self.single_tab, wx.ID_ANY, u"ファイル表示")
        self.show_single_file_button.Enable(False)
        sizer_10.Add(self.show_single_file_button, 0, wx.LEFT, 4)

        self.batch_tab = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.notebook_1.AddPage(self.batch_tab, u"バッチ")

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_2, 0, wx.ALL | wx.EXPAND, 5)

        label_1 = wx.StaticText(self.batch_tab, wx.ID_ANY, u"対象フォルダ:")
        label_1.SetMinSize((100, -1))
        sizer_2.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.input_dir_picker = xw.DropableDirPickerCtrl(self.batch_tab, wx.ID_ANY)
        sizer_2.Add(self.input_dir_picker, 1, wx.EXPAND, 0)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_3, 0, wx.ALL | wx.EXPAND, 5)

        label_2 = wx.StaticText(self.batch_tab, wx.ID_ANY, u"出力フォルダ:")
        label_2.SetMinSize((100, -1))
        sizer_3.Add(label_2, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.output_dir_picker = xw.DropableDirPickerCtrl(self.batch_tab, wx.ID_ANY)
        sizer_3.Add(self.output_dir_picker, 1, wx.EXPAND, 0)

        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_4, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.go_button = wx.Button(self.batch_tab, wx.ID_ANY, u"実行")
        sizer_4.Add(self.go_button, 0, wx.RIGHT, 0)

        self.show_folder_button = wx.Button(self.batch_tab, wx.ID_ANY, u"フォルダ表示")
        self.show_folder_button.Enable(False)
        sizer_4.Add(self.show_folder_button, 0, wx.LEFT, 4)

        self.batch_tab.SetSizer(sizer_1)

        self.single_tab.SetSizer(sizer_6)

        self.Layout()
        # end wxGlade

# end of class MyFrame

class MyApp(wx.App):
    def OnInit(self):
        self.Squarer = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.Squarer)
        self.Squarer.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()