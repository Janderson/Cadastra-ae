#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from datetime import datetime
from pyPgSQL import PgSQL
from decimal import Decimal
from datetime import datetime
from timer import RepeatTimer
from time import sleep
from threading import Thread, Timer, Event

try:
    import pygtk
    pygtk.require("2.0")
except:
    print "Cannot Load pyGTK, please install"
    
try:
    import gtk
    import gtk.glade
except:
    print "Cannot Load GTK, please install"
    sys.exit(1)

# Inicializacao do gtk thread
gtk.gdk.threads_enter()

class FractionSetter(Thread):
	stopthread = Event()
	def __init__(self, wnd):
	    Thread.__init__(self)
	    self.wnd = wnd
	def run(self):
		while not self.stopthread.isSet():
			gtk.gdk.threads_enter()
			self.wnd.showmsg("Opa ")
			gtk.gdk.threads_leave()
			sleep(2)
			
	def stop(self):
		self.stopthread.set()


class userconfig():
	def __init__(self):
		self.user_id=0 # Nao esta ativo
		self.project_id=0 # Nao esta ativo
class dbconnect():
	def __init__(self):
		self.date_time_timestamp='Mon Jun 14 15:29:21 -0300 2010'
		self.date_time = "2010-06-16 10:47:24"
		self.banco_ip="192.168.1.246"
		self.banco_nome="rdmine"
		self.banco_usuario="postgres"
		self.banco_senha="123456"
		self.user_id=6 # Usuario Esse que vale
		self.project_id=1
		self.bdcon = PgSQL.connect(host=self.banco_ip, database=self.banco_nome, user=self.banco_usuario, password=self.banco_senha)

	def set_user_id(self, user_id):
	      self.user_id=user_id
	      
	def getuserlogado(self):
		cur = self.bdcon.cursor()
		cur.execute('select firstname from users where id= ' + str(self.user_id))
		return str(cur.fetchall()[0][0])
		
	  
	def load_time_stamp(self):
	  self.date_time_timestamp = datetime.now().strftime("%a %b %d %X -0300 %Y")
	  self.date_time = datetime.now().strftime("%F %X")
	      
	def get_tickets_for_user(self):
		print('Carregando informacoes')
		cur = self.bdcon.cursor()
		cur.execute(' select subject,issues.id from issues INNER JOIN projects ON issues.project_id = projects.id INNER JOIN users ON issues.assigned_to_id = users.id where project_id='+str(self.project_id)+' and assigned_to_id='+str(self.user_id)+' and not status_id =5 order by issues.id;')
		regras = cur.fetchall()
		return regras

	def insert_time(self,  ticket, time):
		print "tenando inserir ", ticket, time
		cur = self.bdcon.cursor()
		self.load_time_stamp()
		daten = datetime.now()
		cur.execute("insert into time_entries (project_id, user_id, issue_id, hours,comments,activity_id,spent_on,tyear,tmonth,tweek, created_on, updated_on) values("+str(self.project_id)+","+str(self.user_id)+", "+str(ticket)+", "+str(time)+", 'inserido pelo cadastra ae',9,'" + daten.strftime("%F") + "', '"+daten.strftime("%Y")+"','"+daten.strftime("%m")+"','"+daten.strftime("%d")+"', '"+str(self.date_time)+"', '"+str(self.date_time)+"');")
		self.bdcon.commit()
		
	def fechar_ticket(self, ticket_id):
		print "fechando ticket", ticket_id
		cur = self.bdcon.cursor()
		# Coloca um assentamento
		self.load_time_stamp()
		cur.execute("insert into journals (journalized_id, journalized_type, user_id, notes, created_on) values ("+str(ticket_id)+", 'Issue', "+str(self.user_id)+", 'Fechado pelo cadastra ai tche', '"+str(self.date_time)+"')")
		self.bdcon.commit()
		# Altera  o status do ticket
		print 
		cur.execute("update issues set status_id=5 where id="+str(ticket_id))
		self.bdcon.commit()
	  
class logintela(object):
	def __init__(self, dbcon, userconf):

		# Abrindo a conexao com banco de dados
		self.dbcon = dbcon
		self.userconf = userconf

		#Setando a variavel com o arquivo glade
		self.arquivoglade = "projetos.glade"
		
		#Extraindo conteúdo XML do arquivo
		
	def load_window(self):
		self.xml = gtk.glade.XML(self.arquivoglade)
		self.MainWindow = self.xml.get_widget('frmLogin')



class adduser(object):
	def __init__(self, dbcon, userconf):

		# Abrindo a conexao com banco de dados
		self.dbcon = dbcon
		self.userconf = userconf

		#Setando a variavel com o arquivo glade
		self.arquivoglade = "projetos.glade"
		#Extraindo conteúdo XML do arquivo
		self.tarefa_iniciada= False
		self.temporario_tempo_tarefa=0
		self.nr_ticket=0
		
		# Status Icon
		self.staticon = gtk.StatusIcon()
		self.staticon.set_from_stock(gtk.STOCK_ABOUT)
		self.staticon.set_blinking(False)
		self.staticon.set_visible(True)
		self.staticon.connect("activate", self.clique_botao_direito)
		self.staticon.connect("popup_menu", self.clique_botao_esquerdo)
		#
		#Componentes
		#
	
		#Janela Principal
		self.load_window()
		self.showmsg("Bem vindo " + self.dbcon.getuserlogado()+"" )

	def teste(self):
	  print "teste chamado"

	def terminate(self):
	    print "fechando a aplicação"
		
	def load_window(self):
		self.xml = gtk.glade.XML(self.arquivoglade)
		self.MainWindow = self.xml.get_widget('frmOpenTicket')

		#Botoes
		self.btnIniciar = self.xml.get_widget('btnIniciar')
		self.btnParar = self.xml.get_widget('btnParar')
		self.btnClose = self.xml.get_widget('btncloseTicket')
		self.menuClose = self.xml.get_widget('memClose')
		

		# Barra de Status
		self.statusbar = self.xml.get_widget('statusbar1')

		#Entrada do nome do usuário
		self.combobox = self.xml.get_widget('combobox1')
		for i in self.dbcon.get_tickets_for_user():
			strcomb= '#'+str(i[1]) +': '+str(i[0])+''
			self.combobox.append_text(strcomb)
		if len(self.dbcon.get_tickets_for_user())==0:
		    self.combobox.append_text("Nenhum ticket aberto para voce nesse projeto")
		    self.btnIniciar.set_sensitive(False)
		    self.btnParar.set_sensitive(False)
		    self.btnClose.set_sensitive(False)
		else:
		    self.btnIniciar.set_sensitive(True)
		    self.btnParar.set_sensitive(True)
		    self.btnClose.set_sensitive(True)
		  
		self.btnIniciar.connect('clicked', self.on_btnIniciar_clicked)
		self.btnParar.connect('clicked', self.on_btnParar_clicked)
		self.btnClose.connect('clicked', self.on_btnFechar_clicked)
		self.menuClose.connect('activate-item', self.terminate)
		
		self.MainWindow.show()
	    
	def showmsg(self, msg):
		#print msg
		context_id = self.statusbar.get_context_id("")
		self.statusbar.pop(context_id)
		self.statusbar.push(context_id, msg)
		self.staticon.set_tooltip(msg)

	def reload_combo(self):
	  model = self.combobox.get_model()
	  active = self.combobox.get_active()
	  print active
	  while not active < 0:
	    self.combobox.remove_text(active)
	    active = self.combobox.get_active()
	    print active
        
	def get_combo_ticket(self):
	  if not self.combobox.get_active_text()==None:
	      ticket= self.combobox.get_active_text().split(":")[0].replace('#','')
	      if not ticket.strip()=='':
		self.nr_ticket=ticket
		return True
	      else:
		return None
	  else:
	    return None
	

	def buscar_tickets_atribuidos(self):
		print ""

	def on_btnIniciar_clicked(self, widget):
	    self.iniciar_tarefa()
	    
	def iniciar_tarefa(self):
		if self.tarefa_iniciada:
			self.showmsg("tarefa do ticket #{" + str(self.nr_ticket) + "} ja iniciada") 
		elif not self.get_combo_ticket()==None:
				self.tarefa_iniciada=True
				self.temporario_tempo_tarefa=datetime.now()
				self.showmsg("Tarefa relacionada ao ticket #{" + str(self.nr_ticket) + "} iniciada")
				self.staticon.set_from_stock(gtk.STOCK_MEDIA_PLAY)
				self.staticon.set_blinking(True)
				fs.start()

				  
		else:
			self.showmsg("Nenhum ticket selecionado")

	def on_btnFechar_clicked(self, widget):
	  
	  if not self.get_combo_ticket()==None:
	    print "Numero de ticket:", self.nr_ticket
	    self.dbcon.fechar_ticket(self.nr_ticket)
	    self.reload_combo()
	    self.showmsg("Ticket #{" + str(self.nr_ticket) + "} fechado com sucesso " )
	    
	  else:
	    self.showmsg("Nenhum ticket selecionado")

	def on_btnParar_clicked(self, widget):
	  self.parar_tarefa()
	
	def parar_tarefa(self):
		if self.tarefa_iniciada:
			self.tarefa_iniciada=False
			tempo = datetime.now() - self.temporario_tempo_tarefa

			hours = tempo.seconds/3600.0

			d = Decimal(str(hours))
			tempofinal= float(d.quantize(Decimal('0.001')))
			self.dbcon.insert_time(self.nr_ticket, tempofinal)
			self.showmsg("parando tarefa relacionada ao ticket #{" + str(self.nr_ticket) + "} tempo total: "+ str(tempofinal))
			self.staticon.set_from_stock(gtk.STOCK_MEDIA_STOP)
			self.staticon.set_blinking(False)
			self.showmsg("tarefa parada relacionada ao ticket #{" + str(self.nr_ticket) + "} tempo total: "+ str(tempofinal))
#

		else:
			self.showmsg("Nenhuma tarefa iniciada, nada fazer")

	def clique_botao_direito(self, widget):
	    print "botao esquerdo"
	    if self.tarefa_iniciada:
	      self.parar_tarefa()
	    else:
	      self.iniciar_tarefa()

	def clique_botao_esquerdo(self, button, widget, data=None):
	    print "botao direito"
	    self.load_window()


if __name__ == "__main__":
	dbcon = dbconnect()
	userconf = userconfig()
	w = adduser(dbcon, userconf)
	gtk.main()
	#fs.stop()
