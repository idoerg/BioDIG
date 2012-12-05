from BCBio.GFF import GFFExaminer
from BCBio import GFF
from optparse import OptionParser
import psycopg2
import sys
import MySQLdb
'''
    Prepares a GFF File for loading into Chado by getting rid of cvterms 
    that would not be recognized by our database
    
    Andrew Oberlin
    Date: March 21, 2012
    
    Version 0.1
    
    Dependencies:
        1) hamap file is present in either the default directory or a specified directory (if using addColor)
        2) MySQLdb and psycopg2 installed on the server
'''
class GFFRewriter:
    '''
        Initializes the rewriter to read in the file and
        start processing
        
        Place entries for all three parameters to ignore command line input
    '''
    def __init__(self, filename=None, outfile=None, accession=None):
        self.error = False
        self.error_msg = ""
        if (not (filename and accession)):
            opts = OptionParser()
            opts.add_option("-f","--file",action="store",type = "string", dest="filename", help="Exact location of the file")
            opts.add_option("--outfile", action = "store", type = "string", dest="outfile", help="The file to write formatted gff to. By default this is <inFileName>.colored")
            opts.add_option("--accession", action="store", type="string", dest="accession", help="GO Accession")

            (options, args) = opts.parse_args()
        
            self.filename = options.filename
            self.outfile = options.outfile
            self.accession = options.accession

            if (not self.outfile):
                self.outfile = options.filename + '.prepared'
        else:
            self.filename = filename
            self.outfile = outfile
            self.accession = accession
        
    '''
        Locates all the types of records fin this gff file
        and checks to see if each is in the database
        
        If not then the term is inserted into the unknown cv
    '''
    def addUnknownCvTerms(self, dbInfo={'user' : 'oberliat', 'password' : 'password', 'db' : 'chado'}):
        examiner = GFFExaminer()
        file = open(self.filename)
        
        try:
            conn = psycopg2.connect(database=dbInfo['db'], user=dbInfo['user'], password=dbInfo['password'], host='localhost')
            cur = conn.cursor()        
        except Exception, e:
            self.error = True
            self.error_msg = "Unable to connect to the database " + dbInfo['db']
            sys.exit(1)
        
        try:
            gff_stats = examiner.available_limits(file)
            for gff_type_list in gff_stats['gff_type'].keys():
                for gff_type in gff_type_list:
                    cur.execute("SELECT COUNT(*) FROM cvterm WHERE name = '" + gff_type + "' AND cv_id=10;");
                    count = cur.fetchone()[0]
                    if (count == 0):
                        query = 'INSERT INTO dbxref ("db_id", "accession") VALUES(41, %s) RETURNING dbxref_id'
                        cur.execute(query, (gff_type, ))
                        dbxref_id = cur.fetchone()[0]
                        if (dbxref_id):
                            # inserts the term into the sequence controlled vocabulary (id = 10)
                            query = 'INSERT INTO cvterm ("cv_id", "name", "definition", "dbxref_id", "is_obsolete", "is_relationshiptype") VALUES(10, %s, %s, %s, 0, 0)'
                            cur.execute(query, (gff_type, gff_type, dbxref_id))
        except Exception, e:
            self.error = True
            self.error_msg = e.pgerror
            cur.close()
            conn.close()
            file.close()
            sys.exit(1)

        conn.commit()
        cur.close()
        conn.close()

        file.close()


    '''
        Adds color to the gff file based on a hamap
    '''
    def addColor(self, dbInfo={'user' : 'oberliat', 'password' : 'password', 'db' : 'MyGO'}, hamapName=None):
        if (not self.error):
            try:
                if (hamapName):
                    hamapFile = open(hamapName,'r')
                else:
                    hamapFile = open('/var/www/BioDIG/databaseUpdater/GenomeDB/hamap_families.dat', 'r')
            except IOError:
                self.error_msg = "Could not find the hamap file for coloring"
                self.error = True
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
                connDesc = MySQLdb.connect(host='localhost', user=dbInfo['user'], passwd=dbInfo['password'], db=dbInfo['db'])
                curDesc = connDesc.cursor()
            except MySQLdb.Error, e:
                self.error = True
                self.error_msg = "Error connecting to local Gene Ontology Database"
                sys.exit(1)

            try:
                curDesc.execute("SELECT DISTINCT descendant.acc FROM term INNER JOIN graph_path ON (term.id=graph_path.term1_id) INNER JOIN term AS descendant ON (descendant.id=graph_path.term2_id) WHERE term.name='biological_process' AND distance = 1; ")
                
                bioProcessList = list(curDesc.fetchall())
            except MySQLdb.Error, e:
                self.error = True
                self.error_msg = "Could not find the biological processes in the local Gene Ontology"
                sys.exit(1)

            try:
                curDesc.execute("SELECT DISTINCT descendant.acc FROM term INNER JOIN graph_path ON (term.id=graph_path.term1_id) INNER JOIN term AS descendant ON (descendant.id=graph_path.term2_id) WHERE term.name='molecular_function' AND distance = 1; ")
                
                molecFunctionList = list(curDesc.fetchall())
            except MySQLdb.Error, e:
                self.error = True
                self.error_msg = "Could not find the molecular functions in the local Gene Ontology"
                sys.exit(1)
                
            try:    
                curDesc.execute("SELECT DISTINCT descendant.acc FROM term INNER JOIN graph_path ON (term.id=graph_path.term1_id) INNER JOIN term AS descendant ON (descendant.id=graph_path.term2_id) WHERE term.name='cellular_component' AND distance = 1; ")

                celCompList = list(curDesc.fetchall())
            except MySQLdb.Error, e:
                self.error = True
                self.error_msg = "Could not find the cellular components in the local Gene Ontology"
                sys.exit(1)

            totalLen = len(bioProcessList) + len(molecFunctionList) + len(celCompList)

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

            try:
                gffFile = open(self.filename,'r')
            except IOError:
                self.error = True
                self.error_msg = "Could not open the specified file: " + self.filename
                sys.exit(1)

            outFilename = self.filename + ".colored"

            if (self.outfile != None):
                outFilename = self.outfile
                        
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
                        connMySQL = MySQLdb.connect(host='localhost', user=dbInfo['user'], passwd=dbInfo['password'], db=dbInfo['db'])
                        curMySQL = connMySQL.cursor()
                    except MySQLdb.Error, e:
                        self.error = True
                        self.error_msg = "Error connecting to local Gene Ontology Database"
                        curMySQL.close()
                        connMySQL.close()
                        sys.exit(1)
                    # used for holding all ancestors possibly for this gene
                    tmpList = list()
                    if (hashOntology.has_key(geneName) and hashOntology[geneName][0].strip() != "None"):
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
                            
                            # finds the ancestor information for every node at the correct distance to be both a
                            # descendant of the top tier node and an ancestor of the current node 
                            curMySQL.execute("SELECT DISTINCT ancestor.name, ancestor.acc, ancestor.term_type FROM term INNER JOIN graph_path ON (term.id = graph_path.term2_id) INNER JOIN term AS ancestor ON (ancestor.id = graph_path.term1_id) WHERE term.acc = '" + ontol + "' AND graph_path.distance = " + str(minDistance-1) + ";")
                            ancestorsAway = list(curMySQL.fetchall())
                                    
                            # uses the colorHash table to find whether the
                            # nodes returned from the last query are actually
                            # immediate descendants of the top tier nodes
                            for ancestor in ancestorsAway:
                                if (colorHash.has_key(ancestor[1])):
                                    tmpList.append(ancestor)
                        if (len(tmpList) > 0):
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
                            
                            color = colorHash[currentChosenAncestor[1]]
                            
                            
                            outfile.write(line.strip("\n") + ";color=" + hex(color) + "\n")
                        else:
                            outfile.write(line.strip("\n") + ";color=Unknown\n")
                    else:
                        outfile.write(line.strip("\n") + ";color=Unknown\n")
                else:
                    line_split = line.split()
                    if (line[0] != "#" and len(line_split) > 0 and line_split[0] == self.accession):
                            outfile.write(line.strip("\n") + ";color=Unknown\n")
                    else:
                        outfile.write(line)    
                        
    def getError(self):
        return (self.error, self.error_msg)
        
if (__name__ == "__main__"):      
    rewriter = GFFRewriter()
    rewriter.addUnknownCvTerms()   
    rewriter.addColor()  

        
        
        
