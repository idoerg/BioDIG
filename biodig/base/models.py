#### -----------------------###
#       Image Database        #
#### -----------------------###

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

class Picture(models.Model):
    description = models.TextField(blank=True, null=True)
    #imageName = models.ImageField(upload_to="pictures/")
    #thumbnail = models.ImageField(upload_to="thumbnails/")
    imageName = models.CharField(max_length=256)
    thumbnail = models.CharField(max_length=256)
    publication = models.CharField(max_length=50, blank=True, null=True)
    altText = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User)
    uploadDate = models.DateTimeField(auto_now_add=True)
    isPrivate = models.BooleanField(default=True)
    
    class Meta:
        db_table = u'picture'
        app_label = u'base'

    
    def readPermissions(self, user):       
        # if the image is public then anyone can read it
        if not self.isPrivate:
            return True
        
        exists = user and user.is_authenticated()
        # user exists and is an admin so they get read permissions 
        # no matter what
        if exists and user.is_staff:
            return True
        
        # check to see if user exists, if so do they have permissions?
        if exists:
            return self.user == user
        
        return False
    
    def writePermissions(self, user):        
        exists = user and user.is_authenticated()
        # user exists and is an admin so they get write permissions 
        # no matter what
        if exists and user.is_staff:
            return True
        
        # check to see if user exists, if not then they do not 
        # have write permissions
        if exists:
            # if the image is public then anyone can write to it
            if not self.isPrivate:
                return True
            # check user permissions on a private image
            return self.user == user
        
        return False
    
    def __unicode__(self):
        return str(self.imageName)

class RecentlyViewedPicture(models.Model):
    picture = models.ForeignKey(Picture)
    user = models.ForeignKey(User)
    lastDateViewed = models.DateTimeField()
    def save(self, *args, **kwargs):
        self.lastDateViewed = datetime.now()
        super(RecentlyViewedPicture, self).save(*args, **kwargs)
    class Meta:
        unique_together = ("picture", "user")
        db_table = u'recentlyviewedpicture'
        app_label = u'base'

    
    def __unicode__(self):
        return (self.picture.imageName.name) + " viewed by " + self.user.username

class TagGroup(models.Model):
    name = models.TextField()
    picture = models.ForeignKey(Picture)
    dateCreated = models.DateTimeField(auto_now_add=True, editable=False)
    lastModified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    isPrivate = models.BooleanField(default=True)
    class Meta:
        db_table = u'taggroup'
        unique_together = ('name', 'picture',)
        app_label = u'base'

        
    def readPermissions(self, user):
        # if the tag group is public then anyone can read it
        if not self.isPrivate:
            return True
        
        exists = user and user.is_authenticated()
        # user exists and is an admin so they get read permissions 
        # no matter what
        if exists and user.is_staff:
            return True
        
        # need read permissions on the picture to have read permissions
        # on one of its tag groups
        if not self.picture.readPermissions(user):
            return False
        
        # check to see if user exists, if so do they have permissions?
        if exists:
            return self.user == user
        
        return False
    
    def writePermissions(self, user):
        exists = user and user.is_authenticated()
        # user exists and is an admin so they get write permissions 
        # no matter what
        if exists and user.is_staff:
            return True
        
        # need write permissions on the picture to have write permissions
        # on one of its tag groups
        if not self.picture.writePermissions(user):
            return False
        
        # check to see if user exists, if not then they do not 
        # have write permissions
        if exists:
            # if the image is public then anyone can write to it
            if not self.isPrivate:
                return True
            # check user permissions on a private image
            return self.user == user
        
        return False
    
    def __unicode__(self):
        return self.name

class TagColor(models.Model):
    red = models.IntegerField()
    green = models.IntegerField()
    blue = models.IntegerField()
    class Meta:
        db_table = u'tagcolor'
        app_label = u'base'

    def __unicode__(self):
        return 'R: ' + str(self.red) + ', G: ' + str(self.green) + ', B: ' + str(self.blue)

class Tag(models.Model):
    name = models.TextField()
    color = models.ForeignKey(TagColor)
    group = models.ForeignKey(TagGroup)
    dateCreated = models.DateTimeField(auto_now_add=True, editable=False)
    lastModified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    isPrivate = models.BooleanField(default=True)
    class Meta:
        db_table = u'tag'
        app_label = u'base'

        
    def readPermissions(self, user):
        # if the tag group is public then anyone can read it
        if not self.isPrivate:
            return True
        
        exists = user and user.is_authenticated()
        # user exists and is an admin so they get read permissions 
        # no matter what
        if exists and user.is_staff:
            return True
        
        # need read permissions on the tag group to have read permissions
        # on one of its tags
        if not self.group.readPermissions(user):
            return False
        
        # check to see if user exists, if so do they have permissions?
        if exists:
            return self.user == user
        
        return False
    
    def writePermissions(self, user):
        exists = user and user.is_authenticated()
        # user exists and is an admin so they get write permissions 
        # no matter what
        if exists and user.is_staff:
            return True
        
        # need write permissions on the picture to have write permissions
        # on one of its tag groups
        if not self.group.writePermissions(user):
            return False
        
        # check to see if user exists, if not then they do not 
        # have write permissions
        if exists:
            # if the image is public then anyone can write to it
            if not self.isPrivate:
                return True
            # check user permissions on a private image
            return self.user == user
        
        return False
        
    def __unicode__(self):
        return self.name
    
class TagPoint(models.Model):
    tag = models.ForeignKey(Tag)
    pointX = models.FloatField()
    pointY = models.FloatField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'tagpoint'
        app_label = u'base'

    def __unicode__(self):
        return "(" + str(self.pointX) + "," + str(self.pointY) + ") " + self.tag.name
        
class BlastUpload(models.Model):
    fasta_file = models.FileField(upload_to="fasta_files/")
    name = models.TextField()
    class Meta:
        db_table = u'blastupload'
        app_label = u'base'

    def __unicode__(self):
        return self.name

class GenomeUpload(models.Model):
    genbank_file = models.FileField(upload_to="genbank_files/")
    name = models.TextField()
    class Meta:
        db_table = u'genomeupload'
        app_label = u'base'

    def __unicode__(self):
        return self.name
        
class Landmark(models.Model):
    name = models.CharField(max_length=10)
    organism_id = models.IntegerField()
    class Meta:
        db_table = u'landmark'
        app_label = u'base'

    def __unicode__(self):
        return self.name

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

class Tableinfo(models.Model):
    tableinfo_id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=30)
    primary_key_column = models.CharField(max_length=30)
    is_view = models.IntegerField()
    view_on_table_id = models.IntegerField()
    superclass_table_id = models.IntegerField()
    is_updateable = models.IntegerField()
    modification_date = models.DateField()
    class Meta:
        db_table = u'tableinfo'
        app_label = u'base'


class Db(models.Model):
    db_id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    urlprefix = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    class Meta:
        db_table = u'db'
        app_label = u'base'


class Dbxref(models.Model):
    dbxref_id = models.IntegerField(primary_key=True)
    db = models.ForeignKey(Db)
    accession = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    description = models.TextField()
    class Meta:
        db_table = u'dbxref'
        app_label = u'base'


class DbDbxrefCount(models.Model):
    name = models.CharField(max_length=255)
    num_dbxrefs = models.BigIntegerField()
    class Meta:
        db_table = u'db_dbxref_count'
        app_label = u'base'


class Cv(models.Model):
    cv_id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    definition = models.TextField()
    class Meta:
        db_table = u'cv'

        app_label = u'base'

        
class Cvterm(models.Model):
    cvterm_id = models.IntegerField(primary_key=True)
    cv = models.ForeignKey(Cv)
    name = models.CharField(max_length=1024)
    definition = models.TextField()
    dbxref = models.ForeignKey(Dbxref)
    is_obsolete = models.IntegerField()
    is_relationshiptype = models.IntegerField()
    class Meta:
        db_table = u'cvterm'

        app_label = u'base'


class CvtermRelationship(models.Model):
    cvterm_relationship_id = models.IntegerField(primary_key=True)
    type = models.ForeignKey(Cvterm, related_name = "cvtermrelationship_type_set")
    subject = models.ForeignKey(Cvterm, related_name = "cvtermrelationship_subject_set")
    object = models.ForeignKey(Cvterm, related_name = "cvtermrelationship_object_set")
    class Meta:
        db_table = u'cvterm_relationship'
        app_label = u'base'


class Project(models.Model):
    project_id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    class Meta:
        db_table = u'project'
        app_label = u'base'


class Cvtermpath(models.Model):
    cvtermpath_id = models.IntegerField(primary_key=True)
    type = models.ForeignKey(Cvterm, related_name = "cvtermpath_type_set")
    subject = models.ForeignKey(Cvterm, related_name = "cvtermpath_subject_set")
    object = models.ForeignKey(Cvterm, related_name = "cvtermpath_object_set")
    cv = models.ForeignKey(Cv)
    pathdistance = models.IntegerField()
    class Meta:
        db_table = u'cvtermpath'
        app_label = u'base'


class CvLeaf(models.Model):
    cv_id = models.IntegerField()
    cvterm_id = models.IntegerField()
    class Meta:
        db_table = u'cv_leaf'
        app_label = u'base'


class Dbxrefprop(models.Model):
    dbxrefprop_id = models.IntegerField(primary_key=True)
    dbxref = models.ForeignKey(Dbxref)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'dbxrefprop'
        app_label = u'base'


class Cvtermprop(models.Model):
    cvtermprop_id = models.IntegerField(primary_key=True)
    cvterm = models.ForeignKey(Cvterm, related_name = "cvtermprop_cvterm_set")
    type = models.ForeignKey(Cvterm, related_name = "cvtermprop_type_set")
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'cvtermprop'
        app_label = u'base'


class Cvtermsynonym(models.Model):
    cvtermsynonym_id = models.IntegerField(primary_key=True)
    cvterm = models.ForeignKey(Cvterm, related_name = "cvtermsynonym_cvterm_set")
    synonym = models.CharField(max_length=1024)
    type = models.ForeignKey(Cvterm, related_name = "cvtermsynonym_type_set")
    class Meta:
        db_table = u'cvtermsynonym'
        app_label = u'base'


class CommonAncestorCvterm(models.Model):
    cvterm1_id = models.IntegerField()
    cvterm2_id = models.IntegerField()
    ancestor_cvterm_id = models.IntegerField()
    pathdistance1 = models.IntegerField()
    pathdistance2 = models.IntegerField()
    total_pathdistance = models.IntegerField()
    class Meta:
        db_table = u'common_ancestor_cvterm'
        app_label = u'base'


class CvtermDbxref(models.Model):
    cvterm_dbxref_id = models.IntegerField(primary_key=True)
    cvterm = models.ForeignKey(Cvterm)
    dbxref = models.ForeignKey(Dbxref)
    is_for_definition = models.IntegerField()
    class Meta:
        db_table = u'cvterm_dbxref'
        app_label = u'base'


class CommonDescendantCvterm(models.Model):
    cvterm1_id = models.IntegerField()
    cvterm2_id = models.IntegerField()
    ancestor_cvterm_id = models.IntegerField()
    pathdistance1 = models.IntegerField()
    pathdistance2 = models.IntegerField()
    total_pathdistance = models.IntegerField()
    class Meta:
        db_table = u'common_descendant_cvterm'
        app_label = u'base'


class CvRoot(models.Model):
    cv_id = models.IntegerField()
    root_cvterm_id = models.IntegerField()
    class Meta:
        db_table = u'cv_root'
        app_label = u'base'


class StatsPathsToRoot(models.Model):
    cvterm_id = models.IntegerField()
    total_paths = models.BigIntegerField()
    avg_distance = models.DecimalField(max_digits=1001, decimal_places=1000)
    min_distance = models.IntegerField()
    max_distance = models.IntegerField()
    class Meta:
        db_table = u'stats_paths_to_root'
        app_label = u'base'


class CvCvtermCount(models.Model):
    name = models.CharField(max_length=255)
    num_terms_excl_obs = models.BigIntegerField()
    class Meta:
        db_table = u'cv_cvterm_count'
        app_label = u'base'


class CvCvtermCountWithObs(models.Model):
    name = models.CharField(max_length=255)
    num_terms_incl_obs = models.BigIntegerField()
    class Meta:
        db_table = u'cv_cvterm_count_with_obs'
        app_label = u'base'


class CvLinkCount(models.Model):
    cv_name = models.CharField(max_length=255)
    relation_name = models.CharField(max_length=1024)
    relation_cv_name = models.CharField(max_length=255)
    num_links = models.BigIntegerField()
    class Meta:
        db_table = u'cv_link_count'
        app_label = u'base'


class CvPathCount(models.Model):
    cv_name = models.CharField(max_length=255)
    relation_name = models.CharField(max_length=1024)
    relation_cv_name = models.CharField(max_length=255)
    num_paths = models.BigIntegerField()
    class Meta:
        db_table = u'cv_path_count'
        app_label = u'base'


class Pub(models.Model):
    pub_id = models.IntegerField(primary_key=True)
    title = models.TextField()
    volumetitle = models.TextField()
    volume = models.CharField(max_length=255)
    series_name = models.CharField(max_length=255)
    issue = models.CharField(max_length=255)
    pyear = models.CharField(max_length=255)
    pages = models.CharField(max_length=255)
    miniref = models.CharField(max_length=255)
    uniquename = models.TextField(unique=True)
    type = models.ForeignKey(Cvterm)
    is_obsolete = models.BooleanField()
    publisher = models.CharField(max_length=255)
    pubplace = models.CharField(max_length=255)
    class Meta:
        db_table = u'pub'
        app_label = u'base'


class PubRelationship(models.Model):
    pub_relationship_id = models.IntegerField(primary_key=True)
    subject = models.ForeignKey(Pub, related_name = "pub_relationship_subject_set")
    object = models.ForeignKey(Pub, related_name = "pub_relationship_object_set")
    type = models.ForeignKey(Cvterm)
    class Meta:
        db_table = u'pub_relationship'
        app_label = u'base'


class Pubprop(models.Model):
    pubprop_id = models.IntegerField(primary_key=True)
    pub = models.ForeignKey(Pub)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'pubprop'
        app_label = u'base'


class PubDbxref(models.Model):
    pub_dbxref_id = models.IntegerField(primary_key=True)
    pub = models.ForeignKey(Pub)
    dbxref = models.ForeignKey(Dbxref)
    is_current = models.BooleanField()
    class Meta:
        db_table = u'pub_dbxref'
        app_label = u'base'


class Pubauthor(models.Model):
    pubauthor_id = models.IntegerField(primary_key=True)
    pub = models.ForeignKey(Pub)
    rank = models.IntegerField()
    editor = models.BooleanField()
    surname = models.CharField(max_length=100)
    givennames = models.CharField(max_length=100)
    suffix = models.CharField(max_length=100)
    class Meta:
        db_table = u'pubauthor'
        app_label = u'base'



class Organism(models.Model):
    organism_id = models.IntegerField(primary_key=True)
    abbreviation = models.CharField(max_length=255)
    genus = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255)
    comment = models.TextField()
    class Meta:
        db_table = u'organism'
        app_label = u'base'

    def __unicode__(self):
        return self.common_name
    
class OrganismWithImages(models.Model):
    organism_id = models.IntegerField(primary_key=True)
    abbreviation = models.CharField(max_length=255)
    genus = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255)
    comment = models.TextField()
    class Meta:
        db_table = u'organismwithimages'
        app_label = u'base'
        abstract = True

    def __unicode__(self):
        return self.common_name
    # READ ONLY MODEL
    def save(self, **kwargs):
        raise NotImplementedError
    
class OrganismWithGenome(models.Model):
    organism_id = models.IntegerField(primary_key=True)
    abbreviation = models.CharField(max_length=255)
    genus = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255)
    comment = models.TextField()
    class Meta:
        db_table = u'organismwithgenome'
        app_label = u'base'
        abstract = True

    def __unicode__(self):
        return self.common_name
    # READ ONLY MODEL
    def save(self, **kwargs):
        raise NotImplementedError
    
class OrganismWithTags(models.Model):
    organism_id = models.IntegerField(primary_key=True)
    abbreviation = models.CharField(max_length=255)
    genus = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255)
    comment = models.TextField()
    class Meta:
        db_table = u'organismwithtags'
        app_label = u'base'
        abstract = True

    def __unicode__(self):
        return self.common_name
    # READ ONLY MODEL
    def save(self, **kwargs):
        raise NotImplementedError

class OrganismDbxref(models.Model):
    organism_dbxref_id = models.IntegerField(primary_key=True)
    organism = models.ForeignKey(Organism)
    dbxref = models.ForeignKey(Dbxref)
    class Meta:
        db_table = u'organism_dbxref'
        app_label = u'base'


class Feature(models.Model):
    feature_id = models.IntegerField(primary_key=True)
    dbxref = models.ForeignKey(Dbxref)
    organism = models.ForeignKey(Organism)
    name = models.CharField(max_length=255)
    uniquename = models.TextField()
    residues = models.TextField()
    seqlen = models.IntegerField()
    md5checksum = models.TextField() # This field type is a guess.
    type = models.ForeignKey(Cvterm)
    is_analysis = models.BooleanField()
    is_obsolete = models.BooleanField()
    timeaccessioned = models.DateTimeField()
    timelastmodified = models.DateTimeField()
    class Meta:
        db_table = u'feature'
        app_label = u'base'


class Featureloc(models.Model):
    featureloc_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature, related_name = "featureloc_feature_set")
    srcfeature = models.ForeignKey(Feature, related_name = "featureloc_srcfeature_set")
    fmin = models.IntegerField()
    is_fmin_partial = models.BooleanField()
    fmax = models.IntegerField()
    is_fmax_partial = models.BooleanField()
    strand = models.SmallIntegerField()
    phase = models.IntegerField()
    residue_info = models.TextField()
    locgroup = models.IntegerField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'featureloc'
        app_label = u'base'


class FeaturelocPub(models.Model):
    featureloc_pub_id = models.IntegerField(primary_key=True)
    featureloc = models.ForeignKey(Featureloc)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'featureloc_pub'
        app_label = u'base'


class Organismprop(models.Model):
    organismprop_id = models.IntegerField(primary_key=True)
    organism = models.ForeignKey(Organism)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'organismprop'
        app_label = u'base'


class FeaturePub(models.Model):
    feature_pub_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'feature_pub'
        app_label = u'base'


class FeaturePubprop(models.Model):
    feature_pubprop_id = models.IntegerField(primary_key=True)
    feature_pub = models.ForeignKey(FeaturePub)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'feature_pubprop'
        app_label = u'base'


class Featureprop(models.Model):
    featureprop_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'featureprop'
        app_label = u'base'


class FeatureRelationship(models.Model):
    feature_relationship_id = models.IntegerField(primary_key=True)
    subject = models.ForeignKey(Feature, related_name = "feature_relationship_subject_set")
    object = models.ForeignKey(Feature, related_name = "feature_relationship_object_set")
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'feature_relationship'
        app_label = u'base'


class FeatureRelationshipPub(models.Model):
    feature_relationship_pub_id = models.IntegerField(primary_key=True)
    feature_relationship = models.ForeignKey(FeatureRelationship)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'feature_relationship_pub'
        app_label = u'base'


class FeaturepropPub(models.Model):
    featureprop_pub_id = models.IntegerField(primary_key=True)
    featureprop = models.ForeignKey(Featureprop)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'featureprop_pub'
        app_label = u'base'


class FeatureDbxref(models.Model):
    feature_dbxref_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature)
    dbxref = models.ForeignKey(Dbxref)
    is_current = models.BooleanField()
    class Meta:
        db_table = u'feature_dbxref'
        app_label = u'base'


class FeatureCvterm(models.Model):
    feature_cvterm_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature)
    cvterm = models.ForeignKey(Cvterm)
    pub = models.ForeignKey(Pub)
    is_not = models.BooleanField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'feature_cvterm'
        app_label = u'base'


class FeatureCvtermprop(models.Model):
    feature_cvtermprop_id = models.IntegerField(primary_key=True)
    feature_cvterm = models.ForeignKey(FeatureCvterm)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'feature_cvtermprop'
        app_label = u'base'


class FeatureRelationshipprop(models.Model):
    feature_relationshipprop_id = models.IntegerField(primary_key=True)
    feature_relationship = models.ForeignKey(FeatureRelationship)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'feature_relationshipprop'
        app_label = u'base'


class FeatureRelationshippropPub(models.Model):
    feature_relationshipprop_pub_id = models.IntegerField(primary_key=True)
    feature_relationshipprop = models.ForeignKey(FeatureRelationshipprop)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'feature_relationshipprop_pub'
        app_label = u'base'


class FeatureCvtermPub(models.Model):
    feature_cvterm_pub_id = models.IntegerField(primary_key=True)
    feature_cvterm = models.ForeignKey(FeatureCvterm)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'feature_cvterm_pub'
        app_label = u'base'


class FeatureCvtermDbxref(models.Model):
    feature_cvterm_dbxref_id = models.IntegerField(primary_key=True)
    feature_cvterm = models.ForeignKey(FeatureCvterm)
    dbxref = models.ForeignKey(Dbxref)
    class Meta:
        db_table = u'feature_cvterm_dbxref'
        app_label = u'base'


class Synonym(models.Model):
    synonym_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.ForeignKey(Cvterm)
    synonym_sgml = models.CharField(max_length=255)
    class Meta:
        db_table = u'synonym'
        app_label = u'base'


class FeatureSynonym(models.Model):
    feature_synonym_id = models.IntegerField(primary_key=True)
    synonym = models.ForeignKey(Synonym)
    feature = models.ForeignKey(Feature)
    pub = models.ForeignKey(Pub)
    is_current = models.BooleanField()
    is_internal = models.BooleanField()
    class Meta:
        db_table = u'feature_synonym'
        app_label = u'base'


class TypeFeatureCount(models.Model):
    type = models.CharField(max_length=1024)
    num_features = models.BigIntegerField()
    class Meta:
        db_table = u'type_feature_count'

        app_label = u'base'


class ProteinCodingGene(models.Model):
    feature_id = models.IntegerField()
    dbxref_id = models.IntegerField()
    organism_id = models.IntegerField()
    name = models.CharField(max_length=255)
    uniquename = models.TextField()
    residues = models.TextField()
    seqlen = models.IntegerField()
    md5checksum = models.TextField() # This field type is a guess.
    type_id = models.IntegerField()
    is_analysis = models.BooleanField()
    is_obsolete = models.BooleanField()
    timeaccessioned = models.DateTimeField()
    timelastmodified = models.DateTimeField()
    class Meta:
        db_table = u'protein_coding_gene'
        app_label = u'base'


class IntronCombinedView(models.Model):
    exon1_id = models.IntegerField()
    exon2_id = models.IntegerField()
    fmin = models.IntegerField()
    fmax = models.IntegerField()
    strand = models.SmallIntegerField()
    srcfeature_id = models.IntegerField()
    intron_rank = models.IntegerField()
    transcript_id = models.IntegerField()
    class Meta:
        db_table = u'intron_combined_view'
        app_label = u'base'


class IntronlocView(models.Model):
    exon1_id = models.IntegerField()
    exon2_id = models.IntegerField()
    fmin = models.IntegerField()
    fmax = models.IntegerField()
    strand = models.SmallIntegerField()
    srcfeature_id = models.IntegerField()
    class Meta:
        db_table = u'intronloc_view'
        app_label = u'base'


class Analysis(models.Model):
    analysis_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    program = models.CharField(max_length=255)
    programversion = models.CharField(max_length=255)
    algorithm = models.CharField(max_length=255)
    sourcename = models.CharField(max_length=255)
    sourceversion = models.CharField(max_length=255)
    sourceuri = models.TextField()
    timeexecuted = models.DateTimeField()
    class Meta:
        db_table = u'analysis'
        app_label = u'base'


class Analysisfeature(models.Model):
    analysisfeature_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature)
    analysis = models.ForeignKey(Analysis)
    rawscore = models.FloatField()
    normscore = models.FloatField()
    significance = models.FloatField()
    identity = models.FloatField()
    class Meta:
        db_table = u'analysisfeature'
        app_label = u'base'


class Analysisfeatureprop(models.Model):
    analysisfeatureprop_id = models.IntegerField(primary_key=True)
    analysisfeature = models.ForeignKey(Analysisfeature)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'analysisfeatureprop'
        app_label = u'base'


class Analysisprop(models.Model):
    analysisprop_id = models.IntegerField(primary_key=True)
    analysis = models.ForeignKey(Analysis)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'analysisprop'
        app_label = u'base'


class Phenotype(models.Model):
    phenotype_id = models.IntegerField(primary_key=True)
    uniquename = models.TextField(unique=True)
    observable = models.ForeignKey(Cvterm, related_name = "phenotype_observable_set")
    attr = models.ForeignKey(Cvterm, related_name = "phenotype_attr_set")
    value = models.TextField()
    cvalue = models.ForeignKey(Cvterm, related_name = "phenotype_cvalue_set")
    assay = models.ForeignKey(Cvterm, related_name = "phenotype_assay_set")
    class Meta:
        db_table = u'phenotype'
        app_label = u'base'


class PhenotypeCvterm(models.Model):
    phenotype_cvterm_id = models.IntegerField(primary_key=True)
    phenotype = models.ForeignKey(Phenotype)
    cvterm = models.ForeignKey(Cvterm)
    rank = models.IntegerField()
    class Meta:
        db_table = u'phenotype_cvterm'
        app_label = u'base'


class FeaturePhenotype(models.Model):
    feature_phenotype_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature)
    phenotype = models.ForeignKey(Phenotype)
    class Meta:
        db_table = u'feature_phenotype'
        app_label = u'base'


class Environment(models.Model):
    environment_id = models.IntegerField(primary_key=True)
    uniquename = models.TextField(unique=True)
    description = models.TextField()
    class Meta:
        db_table = u'environment'
        app_label = u'base'


class Genotype(models.Model):
    genotype_id = models.IntegerField(primary_key=True)
    name = models.TextField()
    uniquename = models.TextField(unique=True)
    description = models.CharField(max_length=255)
    class Meta:
        db_table = u'genotype'
        app_label = u'base'


class EnvironmentCvterm(models.Model):
    environment_cvterm_id = models.IntegerField(primary_key=True)
    environment = models.ForeignKey(Environment)
    cvterm = models.ForeignKey(Cvterm)
    class Meta:
        db_table = u'environment_cvterm'
        app_label = u'base'


class FeatureGenotype(models.Model):
    feature_genotype_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature, related_name = "feature_genotype_feature_set")
    genotype = models.ForeignKey(Genotype)
    chromosome = models.ForeignKey(Feature, related_name = "feature_genotype_chromosome_set")
    rank = models.IntegerField()
    cgroup = models.IntegerField()
    cvterm = models.ForeignKey(Cvterm)
    class Meta:
        db_table = u'feature_genotype'
        app_label = u'base'


class Phenstatement(models.Model):
    phenstatement_id = models.IntegerField(primary_key=True)
    genotype = models.ForeignKey(Genotype)
    environment = models.ForeignKey(Environment)
    phenotype = models.ForeignKey(Phenotype)
    type = models.ForeignKey(Cvterm)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'phenstatement'
        app_label = u'base'


class PhenotypeComparison(models.Model):
    phenotype_comparison_id = models.IntegerField(primary_key=True)
    genotype1 = models.ForeignKey(Genotype, related_name = "phenotype_comparison_genotype1_set")
    environment1 = models.ForeignKey(Environment, related_name = "phenotype_comparison_environment1_set")
    genotype2 = models.ForeignKey(Genotype, related_name = "phenotype_comparison_genotype2_set")
    environment2 = models.ForeignKey(Environment, related_name = "phenotype_comparison_environment2_set")
    phenotype1 = models.ForeignKey(Phenotype, related_name = "phenotype_comparison_phenotype1_set")
    phenotype2 = models.ForeignKey(Phenotype, related_name = "phenotype_comparison_phenotype2_set")
    pub = models.ForeignKey(Pub)
    organism = models.ForeignKey(Organism)
    class Meta:
        db_table = u'phenotype_comparison'
        app_label = u'base'


class Phendesc(models.Model):
    phendesc_id = models.IntegerField(primary_key=True)
    genotype = models.ForeignKey(Genotype)
    environment = models.ForeignKey(Environment)
    description = models.TextField()
    type = models.ForeignKey(Cvterm)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'phendesc'
        app_label = u'base'


class PhenotypeComparisonCvterm(models.Model):
    phenotype_comparison_cvterm_id = models.IntegerField(primary_key=True)
    phenotype_comparison = models.ForeignKey(PhenotypeComparison)
    cvterm = models.ForeignKey(Cvterm)
    pub = models.ForeignKey(Pub)
    rank = models.IntegerField()
    class Meta:
        db_table = u'phenotype_comparison_cvterm'
        app_label = u'base'


class Featuremap(models.Model):
    featuremap_id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    unittype = models.ForeignKey(Cvterm)
    class Meta:
        db_table = u'featuremap'
        app_label = u'base'


class Featurerange(models.Model):
    featurerange_id = models.IntegerField(primary_key=True)
    featuremap = models.ForeignKey(Featuremap)
    feature = models.ForeignKey(Feature, related_name = "featurerange_feature_set")
    leftstartf = models.ForeignKey(Feature, related_name = "featurerange_leftstartf_set")
    leftendf = models.ForeignKey(Feature, related_name = "featurerange_leftendf_set")
    rightstartf = models.ForeignKey(Feature, related_name = "featurerange_rightstartf_set")
    rightendf = models.ForeignKey(Feature, related_name = "featurerange_rightendf_set")
    rangestr = models.CharField(max_length=255)
    class Meta:
        db_table = u'featurerange'
        app_label = u'base'


class Featurepos(models.Model):
    featurepos_id = models.IntegerField(primary_key=True)
    featuremap = models.ForeignKey(Featuremap)
    feature = models.ForeignKey(Feature, related_name = "featurepos_feature_set")
    map_feature = models.ForeignKey(Feature, related_name = "featurerange_map_feature_set")
    mappos = models.FloatField()
    class Meta:
        db_table = u'featurepos'
        app_label = u'base'


class Phylotree(models.Model):
    phylotree_id = models.IntegerField(primary_key=True)
    dbxref = models.ForeignKey(Dbxref)
    name = models.CharField(max_length=255)
    type = models.ForeignKey(Cvterm)
    analysis = models.ForeignKey(Analysis)
    comment = models.TextField()
    class Meta:
        db_table = u'phylotree'
        app_label = u'base'


class Phylonode(models.Model):
    phylonode_id = models.IntegerField(primary_key=True)
    phylotree = models.ForeignKey(Phylotree)
    parent_phylonode = models.ForeignKey('self')
    left_idx = models.IntegerField()
    right_idx = models.IntegerField()
    type = models.ForeignKey(Cvterm)
    feature = models.ForeignKey(Feature)
    label = models.CharField(max_length=255)
    distance = models.FloatField()
    class Meta:
        db_table = u'phylonode'
        app_label = u'base'


class PhylonodeDbxref(models.Model):
    phylonode_dbxref_id = models.IntegerField(primary_key=True)
    phylonode = models.ForeignKey(Phylonode)
    dbxref = models.ForeignKey(Dbxref)
    class Meta:
        db_table = u'phylonode_dbxref'
        app_label = u'base'


class FeaturemapPub(models.Model):
    featuremap_pub_id = models.IntegerField(primary_key=True)
    featuremap = models.ForeignKey(Featuremap)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'featuremap_pub'
        app_label = u'base'


class PhylotreePub(models.Model):
    phylotree_pub_id = models.IntegerField(primary_key=True)
    phylotree = models.ForeignKey(Phylotree)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'phylotree_pub'
        app_label = u'base'


class PhylonodePub(models.Model):
    phylonode_pub_id = models.IntegerField(primary_key=True)
    phylonode = models.ForeignKey(Phylonode)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'phylonode_pub'
        app_label = u'base'


class PhylonodeOrganism(models.Model):
    phylonode_organism_id = models.IntegerField(primary_key=True)
    phylonode = models.ForeignKey(Phylonode)
    organism = models.ForeignKey(Organism)
    class Meta:
        db_table = u'phylonode_organism'
        app_label = u'base'


class Phylonodeprop(models.Model):
    phylonodeprop_id = models.IntegerField(primary_key=True)
    phylonode = models.ForeignKey(Phylonode)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'phylonodeprop'
        app_label = u'base'



class Contact(models.Model):
    contact_id = models.IntegerField(primary_key=True)
    type = models.ForeignKey(Cvterm)
    name = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    class Meta:
        db_table = u'contact'
        app_label = u'base'


class ContactRelationship(models.Model):
    contact_relationship_id = models.IntegerField(primary_key=True)
    type = models.ForeignKey(Cvterm)
    subject = models.ForeignKey(Contact, related_name = "contact_relationship_subject_set")
    object = models.ForeignKey(Contact, related_name = "contact_relationship_object_set")
    class Meta:
        db_table = u'contact_relationship'
        app_label = u'base'


class PhylonodeRelationship(models.Model):
    phylonode_relationship_id = models.IntegerField(primary_key=True)
    subject = models.ForeignKey(Phylonode, related_name = "pylonode_relationship_subject_set")
    object = models.ForeignKey(Phylonode, related_name = "pylonode_relationship_object_set")
    type = models.ForeignKey(Cvterm)
    rank = models.IntegerField()
    phylotree = models.ForeignKey(Phylotree)
    class Meta:
        db_table = u'phylonode_relationship'
        app_label = u'base'


class Expression(models.Model):
    expression_id = models.IntegerField(primary_key=True)
    uniquename = models.TextField(unique=True)
    md5checksum = models.TextField() # This field type is a guess.
    description = models.TextField()
    class Meta:
        db_table = u'expression'
        app_label = u'base'


class ExpressionCvterm(models.Model):
    expression_cvterm_id = models.IntegerField(primary_key=True)
    expression = models.ForeignKey(Expression)
    cvterm = models.ForeignKey(Cvterm, related_name = "expression_cvterm_cvterm_set")
    rank = models.IntegerField()
    cvterm_type = models.ForeignKey(Cvterm, related_name = "expression_cvterm_cvterm_type_set")
    class Meta:
        db_table = u'expression_cvterm'
        app_label = u'base'


class ExpressionCvtermprop(models.Model):
    expression_cvtermprop_id = models.IntegerField(primary_key=True)
    expression_cvterm = models.ForeignKey(ExpressionCvterm)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'expression_cvtermprop'
        app_label = u'base'


class Expressionprop(models.Model):
    expressionprop_id = models.IntegerField(primary_key=True)
    expression = models.ForeignKey(Expression)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'expressionprop'
        app_label = u'base'


class FeatureExpression(models.Model):
    feature_expression_id = models.IntegerField(primary_key=True)
    expression = models.ForeignKey(Expression)
    feature = models.ForeignKey(Feature)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'feature_expression'
        app_label = u'base'


class ExpressionPub(models.Model):
    expression_pub_id = models.IntegerField(primary_key=True)
    expression = models.ForeignKey(Expression)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'expression_pub'
        app_label = u'base'


class FeatureExpressionprop(models.Model):
    feature_expressionprop_id = models.IntegerField(primary_key=True)
    feature_expression = models.ForeignKey(FeatureExpression)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'feature_expressionprop'
        app_label = u'base'


class Eimage(models.Model):
    eimage_id = models.IntegerField(primary_key=True)
    eimage_data = models.TextField()
    eimage_type = models.CharField(max_length=255)
    image_uri = models.CharField(max_length=255)
    class Meta:
        db_table = u'eimage'
        app_label = u'base'


class ExpressionImage(models.Model):
    expression_image_id = models.IntegerField(primary_key=True)
    expression = models.ForeignKey(Expression)
    eimage = models.ForeignKey(Eimage)
    class Meta:
        db_table = u'expression_image'
        app_label = u'base'


class Mageml(models.Model):
    mageml_id = models.IntegerField(primary_key=True)
    mage_package = models.TextField()
    mage_ml = models.TextField()
    class Meta:
        db_table = u'mageml'
        app_label = u'base'


class Magedocumentation(models.Model):
    magedocumentation_id = models.IntegerField(primary_key=True)
    mageml = models.ForeignKey(Mageml)
    tableinfo = models.ForeignKey(Tableinfo)
    row_id = models.IntegerField()
    mageidentifier = models.TextField()
    class Meta:
        db_table = u'magedocumentation'
        app_label = u'base'


class Channel(models.Model):
    channel_id = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True)
    definition = models.TextField()
    class Meta:
        db_table = u'channel'
        app_label = u'base'


class Protocol(models.Model):
    protocol_id = models.IntegerField(primary_key=True)
    type = models.ForeignKey(Cvterm)
    pub = models.ForeignKey(Pub)
    dbxref = models.ForeignKey(Dbxref)
    name = models.TextField(unique=True)
    uri = models.TextField()
    protocoldescription = models.TextField()
    hardwaredescription = models.TextField()
    softwaredescription = models.TextField()
    class Meta:
        db_table = u'protocol'
        app_label = u'base'


class Protocolparam(models.Model):
    protocolparam_id = models.IntegerField(primary_key=True)
    protocol = models.ForeignKey(Protocol)
    name = models.TextField()
    datatype = models.ForeignKey(Cvterm, related_name = "protocolparam_datatype_set")
    unittype = models.ForeignKey(Cvterm, related_name = "protocolparam_unittype_set")
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'protocolparam'
        app_label = u'base'


class Arraydesign(models.Model):
    arraydesign_id = models.IntegerField(primary_key=True)
    manufacturer = models.ForeignKey(Contact)
    platformtype = models.ForeignKey(Cvterm, related_name = "arraydesign_platformtype_set")
    substratetype = models.ForeignKey(Cvterm, related_name = "arraydesign_substratetype_set")
    protocol = models.ForeignKey(Protocol)
    dbxref = models.ForeignKey(Dbxref)
    name = models.TextField(unique=True)
    version = models.TextField()
    description = models.TextField()
    array_dimensions = models.TextField()
    element_dimensions = models.TextField()
    num_of_elements = models.IntegerField()
    num_array_columns = models.IntegerField()
    num_array_rows = models.IntegerField()
    num_grid_columns = models.IntegerField()
    num_grid_rows = models.IntegerField()
    num_sub_columns = models.IntegerField()
    num_sub_rows = models.IntegerField()
    class Meta:
        db_table = u'arraydesign'
        app_label = u'base'


class Arraydesignprop(models.Model):
    arraydesignprop_id = models.IntegerField(primary_key=True)
    arraydesign = models.ForeignKey(Arraydesign)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'arraydesignprop'
        app_label = u'base'


class Assay(models.Model):
    assay_id = models.IntegerField(primary_key=True)
    arraydesign = models.ForeignKey(Arraydesign)
    protocol = models.ForeignKey(Protocol)
    assaydate = models.DateTimeField()
    arrayidentifier = models.TextField()
    arraybatchidentifier = models.TextField()
    operator = models.ForeignKey(Contact)
    dbxref = models.ForeignKey(Dbxref)
    name = models.TextField(unique=True)
    description = models.TextField()
    class Meta:
        db_table = u'assay'
        app_label = u'base'


class AssayProject(models.Model):
    assay_project_id = models.IntegerField(primary_key=True)
    assay = models.ForeignKey(Assay)
    project = models.ForeignKey(Project)
    class Meta:
        db_table = u'assay_project'
        app_label = u'base'


class Assayprop(models.Model):
    assayprop_id = models.IntegerField(primary_key=True)
    assay = models.ForeignKey(Assay)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'assayprop'
        app_label = u'base'


class Biomaterial(models.Model):
    biomaterial_id = models.IntegerField(primary_key=True)
    taxon = models.ForeignKey(Organism)
    biosourceprovider = models.ForeignKey(Contact)
    dbxref = models.ForeignKey(Dbxref)
    name = models.TextField(unique=True)
    description = models.TextField()
    class Meta:
        db_table = u'biomaterial'
        app_label = u'base'


class BiomaterialDbxref(models.Model):
    biomaterial_dbxref_id = models.IntegerField(primary_key=True)
    biomaterial = models.ForeignKey(Biomaterial)
    dbxref = models.ForeignKey(Dbxref)
    class Meta:
        db_table = u'biomaterial_dbxref'

        app_label = u'base'


class BiomaterialRelationship(models.Model):
    biomaterial_relationship_id = models.IntegerField(primary_key=True)
    subject = models.ForeignKey(Biomaterial, related_name = "biomaterial_relationship_subject_set")
    type = models.ForeignKey(Cvterm)
    object = models.ForeignKey(Biomaterial, related_name = "biomaterial_relationship_object_set")
    class Meta:
        db_table = u'biomaterial_relationship'
        app_label = u'base'


class Biomaterialprop(models.Model):
    biomaterialprop_id = models.IntegerField(primary_key=True)
    biomaterial = models.ForeignKey(Biomaterial)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'biomaterialprop'
        app_label = u'base'


class Treatment(models.Model):
    treatment_id = models.IntegerField(primary_key=True)
    rank = models.IntegerField()
    biomaterial = models.ForeignKey(Biomaterial)
    type = models.ForeignKey(Cvterm)
    protocol = models.ForeignKey(Protocol)
    name = models.TextField()
    class Meta:
        db_table = u'treatment'
        app_label = u'base'


class BiomaterialTreatment(models.Model):
    biomaterial_treatment_id = models.IntegerField(primary_key=True)
    biomaterial = models.ForeignKey(Biomaterial)
    treatment = models.ForeignKey(Treatment)
    unittype = models.ForeignKey(Cvterm)
    value = models.FloatField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'biomaterial_treatment'
        app_label = u'base'


class AssayBiomaterial(models.Model):
    assay_biomaterial_id = models.IntegerField(primary_key=True)
    assay = models.ForeignKey(Assay)
    biomaterial = models.ForeignKey(Biomaterial)
    channel = models.ForeignKey(Channel)
    rank = models.IntegerField()
    class Meta:
        db_table = u'assay_biomaterial'
        app_label = u'base'


class Acquisition(models.Model):
    acquisition_id = models.IntegerField(primary_key=True)
    assay = models.ForeignKey(Assay)
    protocol = models.ForeignKey(Protocol)
    channel = models.ForeignKey(Channel)
    acquisitiondate = models.DateTimeField()
    name = models.TextField(unique=True)
    uri = models.TextField()
    class Meta:
        db_table = u'acquisition'
        app_label = u'base'


class AcquisitionRelationship(models.Model):
    acquisition_relationship_id = models.IntegerField(primary_key=True)
    subject = models.ForeignKey(Acquisition, related_name = "acquisition_relationship_subject_set")
    type = models.ForeignKey(Cvterm)
    object = models.ForeignKey(Acquisition, related_name = "acquisition_relationship_object_set")
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'acquisition_relationship'
        app_label = u'base'


class Acquisitionprop(models.Model):
    acquisitionprop_id = models.IntegerField(primary_key=True)
    acquisition = models.ForeignKey(Acquisition)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'acquisitionprop'
        app_label = u'base'


class Quantification(models.Model):
    quantification_id = models.IntegerField(primary_key=True)
    acquisition = models.ForeignKey(Acquisition)
    operator = models.ForeignKey(Contact)
    protocol = models.ForeignKey(Protocol)
    analysis = models.ForeignKey(Analysis)
    quantificationdate = models.DateTimeField()
    name = models.TextField()
    uri = models.TextField()
    class Meta:
        db_table = u'quantification'
        app_label = u'base'


class Quantificationprop(models.Model):
    quantificationprop_id = models.IntegerField(primary_key=True)
    quantification = models.ForeignKey(Quantification)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'quantificationprop'
        app_label = u'base'


class QuantificationRelationship(models.Model):
    quantification_relationship_id = models.IntegerField(primary_key=True)
    subject = models.ForeignKey(Quantification, related_name = "quantification_relationship_subject_set")
    type = models.ForeignKey(Cvterm)
    object = models.ForeignKey(Quantification, related_name = "quantification_relationship_object_set")
    class Meta:
        db_table = u'quantification_relationship'
        app_label = u'base'


class Control(models.Model):
    control_id = models.IntegerField(primary_key=True)
    type = models.ForeignKey(Cvterm)
    assay = models.ForeignKey(Assay)
    tableinfo = models.ForeignKey(Tableinfo)
    row_id = models.IntegerField()
    name = models.TextField()
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'control'
        app_label = u'base'


class Element(models.Model):
    element_id = models.IntegerField(primary_key=True)
    feature = models.ForeignKey(Feature)
    arraydesign = models.ForeignKey(Arraydesign)
    type = models.ForeignKey(Cvterm)
    dbxref = models.ForeignKey(Dbxref)
    class Meta:
        db_table = u'element'
        app_label = u'base'


class Elementresult(models.Model):
    elementresult_id = models.IntegerField(primary_key=True)
    element = models.ForeignKey(Element)
    quantification = models.ForeignKey(Quantification)
    signal = models.FloatField()
    class Meta:
        db_table = u'elementresult'
        app_label = u'base'


class ElementRelationship(models.Model):
    element_relationship_id = models.IntegerField(primary_key=True)
    subject = models.ForeignKey(Element, related_name = "element_relationship_subject_set")
    type = models.ForeignKey(Cvterm)
    object = models.ForeignKey(Element, related_name = "element_relationship_object_set")
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'element_relationship'
        app_label = u'base'


class Study(models.Model):
    study_id = models.IntegerField(primary_key=True)
    contact = models.ForeignKey(Contact)
    pub = models.ForeignKey(Pub)
    dbxref = models.ForeignKey(Dbxref)
    name = models.TextField(unique=True)
    description = models.TextField()
    class Meta:
        db_table = u'study'
        app_label = u'base'


class StudyAssay(models.Model):
    study_assay_id = models.IntegerField(primary_key=True)
    study = models.ForeignKey(Study)
    assay = models.ForeignKey(Assay)
    class Meta:
        db_table = u'study_assay'
        app_label = u'base'


class ElementresultRelationship(models.Model):
    elementresult_relationship_id = models.IntegerField(primary_key=True)
    subject = models.ForeignKey(Elementresult, related_name = "elementresult_relationship_subject_set")
    type = models.ForeignKey(Cvterm)
    object = models.ForeignKey(Elementresult, related_name = "elementresult_relationship_object_set")
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'elementresult_relationship'
        app_label = u'base'


class Studydesign(models.Model):
    studydesign_id = models.IntegerField(primary_key=True)
    study = models.ForeignKey(Study)
    description = models.TextField()
    class Meta:
        db_table = u'studydesign'
        app_label = u'base'


class Studydesignprop(models.Model):
    studydesignprop_id = models.IntegerField(primary_key=True)
    studydesign = models.ForeignKey(Studydesign)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'studydesignprop'
        app_label = u'base'


class Studyprop(models.Model):
    studyprop_id = models.IntegerField(primary_key=True)
    study = models.ForeignKey(Study)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'studyprop'
        app_label = u'base'


class StudypropFeature(models.Model):
    studyprop_feature_id = models.IntegerField(primary_key=True)
    studyprop = models.ForeignKey(Studyprop)
    feature = models.ForeignKey(Feature)
    type = models.ForeignKey(Cvterm)
    class Meta:
        db_table = u'studyprop_feature'
        app_label = u'base'


class Studyfactor(models.Model):
    studyfactor_id = models.IntegerField(primary_key=True)
    studydesign = models.ForeignKey(Studydesign)
    type = models.ForeignKey(Cvterm)
    name = models.TextField()
    description = models.TextField()
    class Meta:
        db_table = u'studyfactor'
        app_label = u'base'


class Studyfactorvalue(models.Model):
    studyfactorvalue_id = models.IntegerField(primary_key=True)
    studyfactor = models.ForeignKey(Studyfactor)
    assay = models.ForeignKey(Assay)
    factorvalue = models.TextField()
    name = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'studyfactorvalue'
        app_label = u'base'


class Stock(models.Model):
    stock_id = models.IntegerField(primary_key=True)
    dbxref = models.ForeignKey(Dbxref)
    organism = models.ForeignKey(Organism)
    name = models.CharField(max_length=255)
    uniquename = models.TextField()
    description = models.TextField()
    type = models.ForeignKey(Cvterm)
    is_obsolete = models.BooleanField()
    class Meta:
        db_table = u'stock'
        app_label = u'base'


class StockPub(models.Model):
    stock_pub_id = models.IntegerField(primary_key=True)
    stock = models.ForeignKey(Stock)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'stock_pub'
        app_label = u'base'


class StockRelationship(models.Model):
    stock_relationship_id = models.IntegerField(primary_key=True)
    subject = models.ForeignKey(Stock, related_name = "stock_relationship_subject_set")
    object = models.ForeignKey(Stock, related_name = "stock_relationship_object_set")
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'stock_relationship'
        app_label = u'base'


class StockRelationshipPub(models.Model):
    stock_relationship_pub_id = models.IntegerField(primary_key=True)
    stock_relationship = models.ForeignKey(StockRelationship)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'stock_relationship_pub'
        app_label = u'base'


class Stockprop(models.Model):
    stockprop_id = models.IntegerField(primary_key=True)
    stock = models.ForeignKey(Stock)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'stockprop'
        app_label = u'base'


class StockpropPub(models.Model):
    stockprop_pub_id = models.IntegerField(primary_key=True)
    stockprop = models.ForeignKey(Stockprop)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'stockprop_pub'
        app_label = u'base'


class StockDbxref(models.Model):
    stock_dbxref_id = models.IntegerField(primary_key=True)
    stock = models.ForeignKey(Stock)
    dbxref = models.ForeignKey(Dbxref)
    is_current = models.BooleanField()
    class Meta:
        db_table = u'stock_dbxref'
        app_label = u'base'


class StockCvterm(models.Model):
    stock_cvterm_id = models.IntegerField(primary_key=True)
    stock = models.ForeignKey(Stock)
    cvterm = models.ForeignKey(Cvterm)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'stock_cvterm'
        app_label = u'base'


class StockGenotype(models.Model):
    stock_genotype_id = models.IntegerField(primary_key=True)
    stock = models.ForeignKey(Stock)
    genotype = models.ForeignKey(Genotype)
    class Meta:
        db_table = u'stock_genotype'
        app_label = u'base'


class Stockcollection(models.Model):
    stockcollection_id = models.IntegerField(primary_key=True)
    type = models.ForeignKey(Cvterm)
    contact = models.ForeignKey(Contact)
    name = models.CharField(max_length=255)
    uniquename = models.TextField()
    class Meta:
        db_table = u'stockcollection'
        app_label = u'base'


class StockcollectionStock(models.Model):
    stockcollection_stock_id = models.IntegerField(primary_key=True)
    stockcollection = models.ForeignKey(Stockcollection)
    stock = models.ForeignKey(Stock)
    class Meta:
        db_table = u'stockcollection_stock'
        app_label = u'base'


class Stockcollectionprop(models.Model):
    stockcollectionprop_id = models.IntegerField(primary_key=True)
    stockcollection = models.ForeignKey(Stockcollection)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'stockcollectionprop'
        app_label = u'base'


class Library(models.Model):
    library_id = models.IntegerField(primary_key=True)
    organism = models.ForeignKey(Organism)
    name = models.CharField(max_length=255)
    uniquename = models.TextField()
    type = models.ForeignKey(Cvterm)
    is_obsolete = models.IntegerField()
    timeaccessioned = models.DateTimeField()
    timelastmodified = models.DateTimeField()
    class Meta:
        db_table = u'library'
        app_label = u'base'


class Libraryprop(models.Model):
    libraryprop_id = models.IntegerField(primary_key=True)
    library = models.ForeignKey(Library)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'libraryprop'
        app_label = u'base'


class LibrarypropPub(models.Model):
    libraryprop_pub_id = models.IntegerField(primary_key=True)
    libraryprop = models.ForeignKey(Libraryprop)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'libraryprop_pub'
        app_label = u'base'


class LibrarySynonym(models.Model):
    library_synonym_id = models.IntegerField(primary_key=True)
    synonym = models.ForeignKey(Synonym)
    library = models.ForeignKey(Library)
    pub = models.ForeignKey(Pub)
    is_current = models.BooleanField()
    is_internal = models.BooleanField()
    class Meta:
        db_table = u'library_synonym'

        app_label = u'base'


class LibraryPub(models.Model):
    library_pub_id = models.IntegerField(primary_key=True)
    library = models.ForeignKey(Library)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'library_pub'
        app_label = u'base'


class LibraryFeature(models.Model):
    library_feature_id = models.IntegerField(primary_key=True)
    library = models.ForeignKey(Library)
    feature = models.ForeignKey(Feature)
    class Meta:
        db_table = u'library_feature'
        app_label = u'base'


class LibraryCvterm(models.Model):
    library_cvterm_id = models.IntegerField(primary_key=True)
    library = models.ForeignKey(Library)
    cvterm = models.ForeignKey(Cvterm)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'library_cvterm'
        app_label = u'base'


class LibraryDbxref(models.Model):
    library_dbxref_id = models.IntegerField(primary_key=True)
    library = models.ForeignKey(Library)
    dbxref = models.ForeignKey(Dbxref)
    is_current = models.BooleanField()
    class Meta:
        db_table = u'library_dbxref'
        app_label = u'base'


class CellLine(models.Model):
    cell_line_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    uniquename = models.CharField(max_length=255)
    organism = models.ForeignKey(Organism)
    timeaccessioned = models.DateTimeField()
    timelastmodified = models.DateTimeField()
    class Meta:
        db_table = u'cell_line'
        app_label = u'base'


class CellLineFeature(models.Model):
    cell_line_feature_id = models.IntegerField(primary_key=True)
    cell_line = models.ForeignKey(CellLine)
    feature = models.ForeignKey(Feature)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'cell_line_feature'
        app_label = u'base'


class CellLineprop(models.Model):
    cell_lineprop_id = models.IntegerField(primary_key=True)
    cell_line = models.ForeignKey(CellLine)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'cell_lineprop'
        app_label = u'base'


class CellLinepropPub(models.Model):
    cell_lineprop_pub_id = models.IntegerField(primary_key=True)
    cell_lineprop = models.ForeignKey(CellLineprop)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'cell_lineprop_pub'
        app_label = u'base'


class CellLineRelationship(models.Model):
    cell_line_relationship_id = models.IntegerField(primary_key=True)
    subject = models.ForeignKey(CellLine, related_name = "cell_line_relationship_subject_set")
    object = models.ForeignKey(CellLine, related_name = "cell_line_relationship_object_set")
    type = models.ForeignKey(Cvterm)
    class Meta:
        db_table = u'cell_line_relationship'
        app_label = u'base'


class CellLineDbxref(models.Model):
    cell_line_dbxref_id = models.IntegerField(primary_key=True)
    cell_line = models.ForeignKey(CellLine)
    dbxref = models.ForeignKey(Dbxref)
    is_current = models.BooleanField()
    class Meta:
        db_table = u'cell_line_dbxref'
        app_label = u'base'


class CellLineSynonym(models.Model):
    cell_line_synonym_id = models.IntegerField(primary_key=True)
    cell_line = models.ForeignKey(CellLine)
    synonym = models.ForeignKey(Synonym)
    pub = models.ForeignKey(Pub)
    is_current = models.BooleanField()
    is_internal = models.BooleanField()
    class Meta:
        db_table = u'cell_line_synonym'
        app_label = u'base'


class CellLineCvterm(models.Model):
    cell_line_cvterm_id = models.IntegerField(primary_key=True)
    cell_line = models.ForeignKey(CellLine)
    cvterm = models.ForeignKey(Cvterm)
    pub = models.ForeignKey(Pub)
    rank = models.IntegerField()
    class Meta:
        db_table = u'cell_line_cvterm'
        app_label = u'base'


class CellLineCvtermprop(models.Model):
    cell_line_cvtermprop_id = models.IntegerField(primary_key=True)
    cell_line_cvterm = models.ForeignKey(CellLineCvterm)
    type = models.ForeignKey(Cvterm)
    value = models.TextField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'cell_line_cvtermprop'
        app_label = u'base'


class FeatureDisjoint(models.Model):
    subject_id = models.IntegerField()
    object_id = models.IntegerField()
    class Meta:
        db_table = u'feature_disjoint'
        app_label = u'base'


class FeatureUnion(models.Model):
    subject_id = models.IntegerField()
    object_id = models.IntegerField()
    srcfeature_id = models.IntegerField()
    subject_strand = models.SmallIntegerField()
    object_strand = models.SmallIntegerField()
    fmin = models.IntegerField()
    fmax = models.IntegerField()
    class Meta:
        db_table = u'feature_union'
        app_label = u'base'


class CellLinePub(models.Model):
    cell_line_pub_id = models.IntegerField(primary_key=True)
    cell_line = models.ForeignKey(CellLine)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'cell_line_pub'
        app_label = u'base'


class FeatureIntersection(models.Model):
    subject_id = models.IntegerField()
    object_id = models.IntegerField()
    srcfeature_id = models.IntegerField()
    subject_strand = models.SmallIntegerField()
    object_strand = models.SmallIntegerField()
    fmin = models.IntegerField()
    fmax = models.IntegerField()
    class Meta:
        db_table = u'feature_intersection'
        app_label = u'base'


class FeatureDifference(models.Model):
    subject_id = models.IntegerField()
    object_id = models.IntegerField()
    srcfeature_id = models.SmallIntegerField()
    fmin = models.IntegerField()
    fmax = models.IntegerField()
    strand = models.IntegerField()
    class Meta:
        db_table = u'feature_difference'
        app_label = u'base'


class FeatureDistance(models.Model):
    subject_id = models.IntegerField()
    object_id = models.IntegerField()
    srcfeature_id = models.IntegerField()
    subject_strand = models.SmallIntegerField()
    object_strand = models.SmallIntegerField()
    distance = models.IntegerField()
    class Meta:
        db_table = u'feature_distance'
        app_label = u'base'


class CellLineLibrary(models.Model):
    cell_line_library_id = models.IntegerField(primary_key=True)
    cell_line = models.ForeignKey(CellLine)
    library = models.ForeignKey(Library)
    pub = models.ForeignKey(Pub)
    class Meta:
        db_table = u'cell_line_library'
        app_label = u'base'


class Gff3View(models.Model):
    feature_id = models.IntegerField()
    ref = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    type = models.CharField(max_length=1024)
    fstart = models.IntegerField()
    fend = models.IntegerField()
    score = models.FloatField()
    strand = models.SmallIntegerField()
    phase = models.IntegerField()
    seqlen = models.IntegerField()
    name = models.CharField(max_length=255)
    organism_id = models.IntegerField()
    class Meta:
        db_table = u'gff3view'
        app_label = u'base'


class AllFeatureNames(models.Model):
    feature_id = models.IntegerField()
    name = models.CharField(max_length=255)
    organism_id = models.IntegerField()
    class Meta:
        db_table = u'all_feature_names'
        app_label = u'base'


class Dfeatureloc(models.Model):
    featureloc_id = models.IntegerField()
    feature_id = models.IntegerField()
    srcfeature_id = models.IntegerField()
    nbeg = models.IntegerField()
    is_nbeg_partial = models.BooleanField()
    nend = models.IntegerField()
    is_nend_partial = models.BooleanField()
    strand = models.SmallIntegerField()
    phase = models.IntegerField()
    residue_info = models.TextField()
    locgroup = models.IntegerField()
    rank = models.IntegerField()
    class Meta:
        db_table = u'dfeatureloc'

        app_label = u'base'


class FType(models.Model):
    feature_id = models.IntegerField()
    name = models.CharField(max_length=255)
    dbxref_id = models.IntegerField()
    type = models.CharField(max_length=1024)
    residues = models.TextField()
    seqlen = models.IntegerField()
    md5checksum = models.TextField() # This field type is a guess.
    type_id = models.IntegerField()
    timeaccessioned = models.DateTimeField()
    timelastmodified = models.DateTimeField()
    class Meta:
        db_table = u'f_type'

        app_label = u'base'


class FnrType(models.Model):
    feature_id = models.IntegerField()
    name = models.CharField(max_length=255)
    dbxref_id = models.IntegerField()
    type = models.CharField(max_length=1024)
    residues = models.TextField()
    seqlen = models.IntegerField()
    md5checksum = models.TextField() # This field type is a guess.
    type_id = models.IntegerField()
    timeaccessioned = models.DateTimeField()
    timelastmodified = models.DateTimeField()
    class Meta:
        db_table = u'fnr_type'

        app_label = u'base'


class FLoc(models.Model):
    feature_id = models.IntegerField()
    name = models.CharField(max_length=255)
    dbxref_id = models.IntegerField()
    nbeg = models.IntegerField()
    nend = models.IntegerField()
    strand = models.SmallIntegerField()
    class Meta:
        db_table = u'f_loc'
        app_label = u'base'


class FpKey(models.Model):
    feature_id = models.IntegerField()
    pkey = models.CharField(max_length=1024)
    value = models.TextField()
    class Meta:
        db_table = u'fp_key'
        app_label = u'base'


class FeatureMeets(models.Model):
    subject_id = models.IntegerField()
    object_id = models.IntegerField()
    class Meta:
        db_table = u'feature_meets'
        app_label = u'base'


class FeatureMeetsOnSameStrand(models.Model):
    subject_id = models.IntegerField()
    object_id = models.IntegerField()
    class Meta:
        db_table = u'feature_meets_on_same_strand'
        app_label = u'base'


class FeatureContains(models.Model):
    subject_id = models.IntegerField()
    object_id = models.IntegerField()
    class Meta:
        db_table = u'feature_contains'
        app_label = u'base'


class FeaturesetMeets(models.Model):
    subject_id = models.IntegerField()
    object_id = models.IntegerField()
    class Meta:
        db_table = u'featureset_meets'
        app_label = u'base'


class MaterializedView(models.Model):
    materialized_view_id = models.IntegerField()
    last_update = models.DateTimeField()
    refresh_time = models.IntegerField()
    name = models.CharField(unique=True, max_length=64)
    mv_schema = models.CharField(max_length=64)
    mv_table = models.CharField(max_length=128)
    mv_specs = models.TextField()
    indexed = models.TextField()
    query = models.TextField()
    special_index = models.TextField()
    class Meta:
        db_table = u'materialized_view'
        app_label = u'base'


class GffSortTmp(models.Model):
    refseq = models.CharField(max_length=4000)
    id = models.CharField(max_length=4000)
    parent = models.CharField(max_length=4000)
    gffline = models.CharField(max_length=4000)
    row_id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'gff_sort_tmp'
        app_label = u'base'


class GffMeta(models.Model):
    name = models.CharField(max_length=100)
    hostname = models.CharField(max_length=100)
    starttime = models.DateTimeField()
    class Meta:
        db_table = u'gff_meta'
        app_label = u'base'


class OrthologGraph(models.Model):
    ortholog_graph_id = models.IntegerField(primary_key=True)
    feature_a = models.ForeignKey(Feature, db_column='feature_a', related_name = "ortholog_graph_feature_a_set")
    feature_b = models.ForeignKey(Feature, db_column='feature_b', related_name = "ortholog_graph_feature_b_set")
    class Meta:
        db_table = u'ortholog_graph'
        app_label = u'base'


class TmpGffLoadCache(models.Model):
    feature_id = models.IntegerField()
    uniquename = models.CharField(max_length=1000)
    type_id = models.IntegerField()
    organism_id = models.IntegerField()
    class Meta:
        db_table = u'tmp_gff_load_cache'
        app_label = u'base'


class TmpCdsHandler(models.Model):
    cds_row_id = models.IntegerField(primary_key=True)
    seq_id = models.CharField(max_length=1024)
    gff_id = models.CharField(max_length=1024)
    type = models.CharField(max_length=1024)
    fmin = models.IntegerField()
    fmax = models.IntegerField()
    object = models.TextField()
    class Meta:
        db_table = u'tmp_cds_handler'
        app_label = u'base'


class TmpCdsHandlerRelationship(models.Model):
    rel_row_id = models.IntegerField(primary_key=True)
    cds_row = models.ForeignKey(TmpCdsHandler)
    parent_id = models.CharField(max_length=1024)
    grandparent_id = models.CharField(max_length=1024)
    class Meta:
        db_table = u'tmp_cds_handler_relationship'
        app_label = u'base'


### ------------------------------- ###
#   Gene Links to link the Two DB's   #
### ------------------------------- ###

class GeneLink(models.Model):
    tag = models.ForeignKey(Tag)
    feature = models.ForeignKey(Feature)
    dateCreated = models.DateTimeField(auto_now_add=True, editable=False)
    lastModified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    isPrivate = models.BooleanField(default=True)
    class Meta:
        db_table = u'genelink'
        app_label = u'base'

        unique_together = ('tag', 'feature')
    
    def readPermissions(self, user):
        # if the tag group is public then anyone can read it
        if not self.isPrivate:
            return True
        
        exists = user and user.is_authenticated()
        # user exists and is an admin so they get read permissions 
        # no matter what
        if exists and user.is_staff:
            return True
        
        # need read permissions on the tag to have read permissions
        # on one of its gene links
        if not self.tag.readPermissions(user):
            return False
        
        # check to see if user exists, if so do they have permissions?
        if exists:
            return self.user == user
        
        return False
    
    def writePermissions(self, user):
        exists = user and user.is_authenticated()
        # user exists and is an admin so they get write permissions 
        # no matter what
        if exists and user.is_staff:
            return True
        
        # need write permissions on the picture to have write permissions
        # on one of its tag groups
        if not self.tag.writePermissions(user):
            return False
        
        # check to see if user exists, if not then they do not 
        # have write permissions
        if exists:
            # if the image is public then anyone can write to it
            if not self.isPrivate:
                return True
            # check user permissions on a private image
            return self.user == user
        
        return False
    
    def __unicode__(self):
        return str(self.tag.name) + " and " + str(self.feature.uniquename)
    
class PictureDefinitionTag(models.Model):
    picture = models.ForeignKey(Picture)
    organism = models.ForeignKey(Organism)
    class Meta:
        db_table = u'picturedefinitiontag'
        app_label = u'base'

    def __unicode__(self):
        return ", ".join((str(self.picture.imageName), str(self.organism.common_name)))
