# use /bin/bash to run commands instead of /bin/sh
SHELL=/bin/bash
# mails output to the email address specified here
MAILTO=andyoberlin@gmail.com
# setting the path for any dependencies on PATH
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
# run the GenomeDBUpdater script once every other week every Saturday at 3:00am
00 03 * * 6/2 www-data /usr/bin/python /var/www/mycoplasma_site/databaseUpdater/GenomeDBUpdater.py