import gobject
import gtk
import appindicator, pynotify
from time import sleep
class principal:
  def notificacao(self, texto):

    pynotify.init("MRS")
    p = pynotify.Notification("Redmine Cliente [Cadastra-Ae]", texto, "server")
    p.show()

  def click(self, evt, t):
      self.ind.set_status (appindicator.STATUS_ATTENTION)
      self.ind.set_attention_icon("indicator-messages-new")
      self.notificacao("Aplicacao Rodando")

  def __init__(self):
    self.ind = appindicator.Indicator("Redmine Cliente", "indicator-messages", appindicator.CATEGORY_COMMUNICATIONS)
    # create a menu
    self.ind.set_status (appindicator.STATUS_ACTIVE)
    self.ind.set_attention_icon("indicator-messages")
    self.ind.set_icon("/tmp/favicon.ico")
    menu = gtk.Menu()


    # create some labels
    for i in range(3):
        buf = "Test-undermenu - %d" % i
        menu_items = gtk.MenuItem(buf)
        menu.append(menu_items)
        menu_items.show()
        menu_items.connect("activate", self.click, buf)

    exit_item = gtk.ImageMenuItem(stock_id=gtk.STOCK_QUIT)
    exit_item.connect("activate", quit, None)
    exit_item.set_always_show_image(True)
    exit_item.show()
    menu.append(exit_item)
    self.ind.set_menu(menu)
    gtk.main()


if __name__ == "__main__":
  a = principal()
