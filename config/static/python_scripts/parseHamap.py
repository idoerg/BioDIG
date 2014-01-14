import sys
import psycopg2

try:
    hamapFile = open('/var/www/mycoplasma_site/mycoplasma_home/static/python_scripts/hamap_families.dat','r')
except IOError:
    sys.stderr.write("Could not find the hamap file for coloring")
    sys.exit(1)

name = ""
hashOntology = dict()

for line in hamapFile:
    if line[:2] == 'GN':
        name = line.strip().split('=')[1].split(';')[0]
    if line[:2] == 'GO':
        ontol = line.strip().split(';')[0].split('   ')[1]
        if name in hashOntology:
                hashOntology[name].append(ontol)
        else:
                hashOntology[name] = [ontol]
            
hamapFile.close()

'''
try:
    delimitedFile = open('/var/www/mycoplasma_site/mycoplasma_home/static/python_scripts/ontologies.txt', 'w')
except IOError:
    sys.stderr.write("Could not find the ontologies.txt")
    sys.exit(1)
#delimitedFile.write('\n'.join([i + '\t' + '\t'.join(hashOntology[i]) for i in hashOntology.keys()]))

for key in hashOntology.keys():
    delimitedFile.write(key)
    count = 0
    numGOTerms = len(hashOntology[key])
    for ontol in hashOntology[key]:
        delimitedFile.write('\t' + ontol)
        count += 1
        if count == numGOTerms:
            delimitedFile.write('\n')
            

delimitedFile.close()
'''


# Goes through keys and retrieves the feature_id
myerr = 0
for key in hashOntology.keys():
        
    conn = psycopg2.connect(database = "chado", user = "mycoplasma", password = "5i72c44u", host = "localhost")
    cur = conn.cursor()
    
    cur.execute("SELECT DISTINCT feature_id FROM feature WHERE name = '" + key + "';")
    feature_ids = cur.fetchall()
    
    cur.close()
    conn.close()
    
    conn2 = psycopg2.connect(database = "chado", user = "mycoplasma", password = "5i72c44u", host = "localhost")
    cur2 = conn2.cursor()
    # go through the GO Terms (i.e. GO:0000001) and finds the corresponding cvterm_id
    for goTerm in hashOntology[key]:              
                
                
        if goTerm[:3] == "GO:":
            cur2.execute("SELECT cvterm_id FROM cvterm WHERE dbxref_id = (SELECT dbxref_id FROM dbxref WHERE accession = '" + goTerm.split(':')[1] + "' AND db_id = 89);")
            
            cvterm = cur2.fetchone()[0]
                        
            #for each cv_term and feature_id insert a value into the table
            for feature in feature_ids:
                cur2.execute("SELECT cvterm_id FROM feature_cvterm WHERE cvterm_id = %s AND feature_id = %s",(cvterm,feature[0]))
                fetched = cur2.fetchall()
                if (len(fetched) == 0):                    
                    cur2.execute("INSERT INTO feature_cvterm(feature_id, cvterm_id, pub_id) VALUES(%s, %s, 1);", (feature[0], cvterm))
                    conn2.commit()
    cur2.close()
    conn2.close()
                                        
                                
                        
                                
                                
                            




        
        
