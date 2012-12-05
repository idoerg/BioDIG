import MySQLdb
from optparse import OptionParser
import sys


opts = OptionParser()
opts.add_option("-f","--file",action="store",type = "string", dest="filename", help="Exact location of the file")
opts.add_option("--outfile", action = "store", type = "string", dest="outfile", help="The file to write formatted gff to. By default this is <inFileName>.colored")
opts.add_option("--accession", action="store", type="string", dest="accession", help="GO Accession")

(options, args) = opts.parse_args()

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

try:
    # Query descendants of biological process, molecular function and cellular component
    connDesc = MySQLdb.connect(host="localhost", user="oberliat", passwd="password", db="MyGO")
    curDesc = connDesc.cursor()
except MySQLdb.Error, e:
    sys.stderr.write("Error connecting to local Gene Ontology Database")
    sys.exit(1)

try:
    curDesc.execute("SELECT DISTINCT descendant.acc FROM term INNER JOIN graph_path ON (term.id=graph_path.term1_id) INNER JOIN term AS descendant ON (descendant.id=graph_path.term2_id) WHERE term.name='biological_process' AND distance = 1; ")
    
    bioProcessList = list(curDesc.fetchall())
except MySQLdb.Error, e:
    sys.stderr.write("Could not find the biological processes in the local Gene Ontology")
    sys.exit(1)

try:
    curDesc.execute("SELECT DISTINCT descendant.acc FROM term INNER JOIN graph_path ON (term.id=graph_path.term1_id) INNER JOIN term AS descendant ON (descendant.id=graph_path.term2_id) WHERE term.name='molecular_function' AND distance = 1; ")
    
    molecFunctionList = list(curDesc.fetchall())
except MySQLdb.Error, e:
    sys.stderr.write("Could not find the molecular functions in the local Gene Ontology")
    sys.exit(1)
try:    
    curDesc.execute("SELECT DISTINCT descendant.acc FROM term INNER JOIN graph_path ON (term.id=graph_path.term1_id) INNER JOIN term AS descendant ON (descendant.id=graph_path.term2_id) WHERE term.name='cellular_component' AND distance = 1; ")

    celCompList = list(curDesc.fetchall())
except MySQLdb.Error, e:
    sys.stderr.write("Could not find the cellular components in the local Gene Ontology")
    sys.exit(1)

totalLen = len(bioProcessList) + len(molecFunctionList) + len(celCompList)
 
#print "Length: " + str(totalLen)

colors = ['bisque', 'darkred', 'darkgoldenrod', 'deepskyblue', 'indianred', 'lightblue', 'lightseagreen', 'magenta', 'mediumspringgreen', 'navy', 'palegreen', 'powderblue', 'seagreen', 'black', 'darkgray', 'gold', 'indigo', 'purple', 'blue', 'darkgreen', 'mediumvioletred', 'palevioletred', 'red', 'tan', 'yellow', 'blueviolet', 'khaki', 'olivedrab', 'rosybrown', 'silver', 'teal', 'yellowgreen', 'aqua', 'brown', 'crimson', 'lightgreen', 'mediumorchid', 'orange', 'thistle', 'lime', 'orangered', 'saddlebrown', 'tomato', 'fuchsia', 'deeppink', 'gainsboro', 'hotpink']

gap = 16777215/totalLen

bioProcessList.extend(molecFunctionList)
bioProcessList.extend(celCompList)

colorHash = dict()
j = 0
i = 0

for ontol in bioProcessList:
    colorHash[ontol[0]] = i
    j += 1
    i += gap
'''
try:  
    delimitedFile = open('/var/www/mycoplasma_site/mycoplasma_home/static/python_scripts/color_distribution.txt', 'w')
except IOError:
    sys.stderr.write("Could not create a color distribution file")
    sys.exit(1)

for key in colorHash.keys():
    delimitedFile.write(key)
    count = 0
    color = colorHash[key]
    delimitedFile.write('\t' + hex(color) + "\n")
    count += 1

delimitedFile.close()
'''
try:
    gffFile = open(options.filename,'r')
except IOError:
    sys.stderr.write("Could not open the specified file: " + options.filename)
    sys.exit(1)

outFilename = options.filename + ".colored"

if (options.outfile != None):
    outFilename = options.outfile
            
outfile = open(outFilename,'w')

for line in gffFile:
    # Splits the delimited entry into pieces
    splitLine = line.strip().split()
    
    # finds the entries that refer to genes
    if (len(splitLine) > 2 and splitLine[2] == 'gene'):
        # in GFF format there are allowable options
        # Splits the options
        gffOpts = splitLine[len(splitLine)-1].split(";")
        
        # traverses the options to find the name
        for option in gffOpts:
            optionName = option.split("=")
            #finds the name of the gene
            if (optionName[0] == 'Name'):
                geneName = optionName[1]
                break;
        # connects to MySQL database
        try:   
            connMySQL = MySQLdb.connect(host="localhost", user = "oberliat",passwd = "password",db = "MyGO")
            curMySQL = connMySQL.cursor()
        except MySQLdb.Error, e:
            sys.stderr.write("Error connecting to local Gene Ontology Database")
            sys.exit(1)
        # used for holding all ancestors possibly for this gene
        tmpList = list()
        if (hashOntology.has_key(geneName) and hashOntology[geneName][0].strip() != "None"):
            #print "Name: " + geneName
            #print "ontology: "
            # Each gene is associated with multiple GO:XXXXXXX accessions
            # Finds the ancestors from the DAG asscoiated with each accession
            for ontol in hashOntology[geneName]:  
                # SQL statement to find the distance from the current node on the DAG to whichever top tier nodes
                # (molecular function, biological process, cellular component) it is a descendant of
                curMySQL.execute("SELECT DISTINCT graph_path.distance FROM term INNER JOIN graph_path ON (term.id = graph_path.term2_id) INNER JOIN term AS ancestor ON (ancestor.id = graph_path.term1_id) WHERE term.acc = '" + ontol + "' AND ancestor.name = ancestor.term_type;")
                ancestorDistList = list(curMySQL.fetchall())
                
                # 100 used as arbitrary high value (need infinity)
                minDistance = 100
                # uses only the shortest distance to the selected top tier node
                for distance in ancestorDistList:
                    if distance[0] < minDistance:
                        minDistance = distance[0]
                #print "Min distance: " + str(minDistance)
                #print "\t" + ontol
                
                # finds the ancestor information for every node at the correct distance to be both a
                # descendant of the top tier node and an ancestor of the current node 
                curMySQL.execute("SELECT DISTINCT ancestor.name, ancestor.acc, ancestor.term_type FROM term INNER JOIN graph_path ON (term.id = graph_path.term2_id) INNER JOIN term AS ancestor ON (ancestor.id = graph_path.term1_id) WHERE term.acc = '" + ontol + "' AND graph_path.distance = " + str(minDistance-1) + ";")
                ancestorsAway = list(curMySQL.fetchall())
                #print "Ancestor away: " + str(ancestorsAway)
                        
                # uses the colorHash table to find whether the
                # nodes returned from the last query are actually
                # immediate descendants of the top tier nodes
                for ancestor in ancestorsAway:
                    if (colorHash.has_key(ancestor[1])):
                        tmpList.append(ancestor)
                
            #print "Ancestor: " + str(tmpList) + "\n"
            
            # Go through the list of ancestor candidates searching for molecular function first
            # then biological process then cellular component (will also hold out for a better molecular function
            # than 'binding' or 'structural molecule activity' because those are not particularly helpful)
            currentChosenAncestor = None
            for ancestorCandidate in tmpList:
                if (currentChosenAncestor != None):
                    if (ancestorCandidate[2] == "molecular_function"):
                        if (currentChosenAncestor[0] == "binding" or currentChosenAncestor[0] == "structural molecule activity"):
                            currentChosenAncestor = ancestorCandidate
                    elif (ancestorCandidate[2] == "biological_process"):
                        if (currentChosenAncestor[2] == "cellular_component"):
                            currentChosenAncestor = ancestorCandidate   
                else: 
                    currentChosenAncestor = ancestorCandidate
                    
            #print currentChosenAncestor
            
            color = colorHash[currentChosenAncestor[1]]
            
            
            outfile.write(line.strip("\n") + ";color=" + hex(color) + "\n")
        
        else:
            outfile.write(line.strip("\n") + ";color=Unknown\n")
    else:
        if (line.strip() != "##gff-version 3"):
            line_split = line.split()
            if (line[0] != "#" and len(line_split) > 0 and line_split[0] == options.accession):
                outfile.write(line.strip("\n") + ";color=Unknown\n")
        else:
            outfile.write(line)            
            
    
