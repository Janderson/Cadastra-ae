# -*- coding: utf-8 -*-
################## Pygtk Tray application
###############################

#!/usr/bin/env python

import gtk

class StatusIcc:

    # activate callback
    def activate( self, widget, data=None):
        dialog = gtk.MessageDialog(
        parent         = None,
        flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
        type           = gtk.MESSAGE_INFO,
        buttons        = gtk.BUTTONS_YES_NO,
        message_format = "Did you like this Activation example \n by Maxin B. John <maxinbj...@gmail.com>?")
        dialog.set_title('Popup example')
        dialog.connect('response', self.show_hide)
        dialog.show()

   # Show_Hide callback
    def  show_hide(self, widget,response_id, data= None):
        if response_id == gtk.RESPONSE_YES:
                widget.hide()
        else:
                widget.hide()

    # destroyer callback
    def  destroyer(self, widget,response_id, data= None):
        if response_id == gtk.RESPONSE_OK:
                gtk.main_quit()
        else:
                widget.hide()

    # popup callback
    def popup(self, button, widget, data=None):
        dialog = gtk.MessageDialog(
        parent         = None,
        flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
        type           = gtk.MESSAGE_INFO,
        buttons        = gtk.BUTTONS_OK_CANCEL,
        message_format = "Do you want to close this Status Icon program?")
        dialog.set_title('Popup Window')
        dialog.connect('response', self.destroyer)
        dialog.show()

    def __init__(self):
        # create a new Status Icon
        self.staticon = gtk.StatusIcon()
        self.staticon.set_from_stock(gtk.STOCK_ABOUT)
        self.staticon.set_blinking(True)
        self.staticon.connect("activate", self.activate)
        self.staticon.connect("popup_menu", self.popup)
        self.staticon.set_visible(True)

        # invoking the main()
        gtk.main()

if __name__ == "__main__":
    statusicon = StatusIcc() 