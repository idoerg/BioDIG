# BioDIG Biological Database of Images and Genomes

## What is BioDIG?

BioDIG is a collection of software tools to connect image and genomic data. 
While we are experiencing an explosion in both sequence and image data, we need to 
link these two types of data. Examples include: model organism mutations, cell morphology — 
e.g. pathology and cancer and any type of phenotype data that can be imaged, that can be associated 
with one or more genes. Anything from a Blue Whale to a virus, really.

## Can I see an example?

The Mycoplasma Database of Images and Genomes (MyDIG):
http://wan1.mbi.muohio.edu/dome

## Is there an installer?

Not yet. Working on it. You can read the documentation in the trunk

## So How do I install?

Instructions for fresh install of Django Based BioDIG Database.

Prerequisites: (THIS IS THE HARDEST PART)

    Django - Web framework used for website -- https://docs.djangoproject.com/en/1.3/topics/install/
    
    PostgreSQL - database system used for website -- aptitude install postgresql-8.4
      		- for Django make sure that in pg_hba.conf that 
    
    MySQL - database system used with a GO database clone
    
    Apache - Web Server for Django -- aptitude install apache2
    
    mod-wsgi - mod for Apache for Django -- aptitude install libapache2-mod-wsgi
    
    GBrowse - genome browser used -- http://gmod.org/wiki/GBrowse_2.0_Install_HOWTO (WATCH FOR PREREQUISITES)
    
    Chado - database schema used for organism database 
            -- http://gmod.svn.sourceforge.net/viewvc/gmod/schema/trunk/chado/INSTALL.Chado 
            (You may only need the prerequisites with the dump)
    
    SQLite - database used to back GBrowse 
    	-- CPAN DBD::SQLite for adaptor
    	-- aptitude install sqlite3
    	
    Django files - the package (files) in order to create the website
    
    BioPerl - http://www.bioperl.org/wiki/Installing_BioPerl_on_Ubuntu_Server
    
    Pip - aptitude install python-pip
    
    Sorl-thumbnail - pip install sorl-thumbnail
    
    BioPython - aptitude install python-biopython
    
    GFFParser - go to this page: http://biopython.org/wiki/GFF_Parsing
    	and make sure that the link below is still valid
    	-- go to: http://github.com/chapmanb/bcbb/
    	-- download the source here as a zip file
    	-- unzip this file and in the gff directory run:
    		sudo python setup.py install

Instructions:

1. Clone git repository into /var/www/

2. Change the owner of this folder (recursively) to <username>:<username>

3. Change the owner of /etc/gbrowse2 (recursively) to <username>:<username>

4. Replace the GBrowse.conf in /etc/gbrowse2 with the GBrowse.conf in the configuration folder
   Also, move the taxonTemplate.conf file into the /etc/gbrowse2 folder

5. Add Alias to apache2.conf (or httpd.conf) file
    -typically located in /etc/apache2/
    -command: WSGIScriptAlias / /var/www/BioDIG/apache/django.wsgi

6. Create a user for the psql databases with username/passwords given in settings.py and grant
all privileges to this user on the databases

7. Create the same user in MySQL. Clone the GO database at http://www.geneontology.org/GO.downloads.ontology.shtml.
get the database dump for MySQL that is updated daily

8. Once all databases created, in /var/www/BioDIG/ run: python manage.py syncdb

9. Alter the table "organism" in the chado database using the statement: ALTER TABLE organism DROP CONSTRAINT "organism_c1". 
Otherwise, the database will not allow the same species in value in the species column, which we need.

10. Make sure there is a value in chado in the db table: there should be an entry with db_id=41, name=_global. Also make sure
that there is a /var/www/BioDIG/taxon_home/genomeFiles/current folder and a /var/www/BioDIG/taxon_home/genomeFiles/new
folder. 
    a. In order to use our automatic updating you will have to edit the directories to search and the regex to search with in th GenomeUpdater.py script
    b. Then run databaseUpdater/GenomeDB/GenomeUpdater.py
    

*11. Test to see what is working: If GBrowse is not working check your machine's URL for GBrowse then go into 
    /var/www/BioDIG/taxon_home/templates/public/gbrowse.html and replace the iframe src with that URL
 					
 12. Add the cron job for pruning to crontab to run every Saturday at 3:00am (should already be configured in the cron tab sh for pruning)