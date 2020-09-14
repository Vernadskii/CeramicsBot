from mega import Mega
mega = Mega()
from passwords import email, password
m = mega.login(email, password)
#folder = m.find('Ceramics', exclude_deleted=True)
'''public_exported_web_link = m.export('Ceramics')
print(public_exported_web_link)'''
def list_of_links_vase():
    vase =[]
    globalt = m.get_files()
    for file in globalt:
        if 'vase' in (globalt[file])[1]['a']['n'] or\
                'Vase' in (globalt[file])[1]['a']['n'] or\
                'VASE' in (globalt[file])[1]['a']['n']:
            print(m.export((globalt[file])[1]['a']['n']))
           # list.append(m.get_link(file))

#print(list_of_links_vase())



##########
cerobject = m.find('Ceramics')
print(cerobject)



"""print(folder)
for file in folder:
    if 'PNG' in (folder[file])['a']['n'] or 'JPEG' in (folder[file])['a']['n'] or 'GIF' in (folder[file])['a']['n'] :
        print('yes')"""

        #print(m.export(file[1][5][2][1]))
