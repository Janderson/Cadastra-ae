from redmine import Redmine
rd = Redmine("http://redmine.sislam.com.br", key="03988ba1a5d559b2525ed55db325ea4696c41ba4")
tree = rd.get("projects.xml")
for node in tree.iter('project'):
  print node.find("name").text
  print node.find("id").text
