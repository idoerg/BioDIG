'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for Tag Groups.

    Created on January 13, 2013

    @author: Andrew Oberlin
'''
from django import forms
from django.contrib.auth.models import User
from biodig.base.models import UserProfile
from biodig.base import forms as bioforms
from biodig.base.serializers import UserSerializer
from biodig.base.exceptions import UserDoesNotExist, DatabaseIntegrity
from rest_framework.exceptions import PermissionDenied
from django.db import transaction, DatabaseError
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import uuid

class FormUtil:
    @staticmethod
    def clean_user_id(data):
        '''
            Cleans an user id ensuring that it is a positive integer.
        '''
        if data['user_id'] < 0:
            raise ValidationError("User id is incorrect.")
        return data['user_id']

class MultiGetForm(forms.Form):
    # Query Parameters
    offset = forms.IntegerField(required=False)
    limit = forms.IntegerField(required=False)
    # User filters (Query)
    username = forms.IntegerField(required=False)
    email = forms.EmailField(required=False)
    is_active = forms.BooleanField(required=False)

    def clean(self):
        if not self.cleaned_data['offset']: self.cleaned_data['offset'] = 0
        return self.cleaned_data


    def submit(self, request):
        '''
            Submits the form for getting multiple Users
            once the form has cleaned the input data.
        '''
        qbuild = bioforms.QueryBuilder(User)

        # add permissions to query
        if request.user and request.user.is_authenticated():
            if not request.user.is_staff:
                qbuild.q = qbuild().filter(isPrivate = False) | User.objects.filter(user__pk__exact=request.user.pk)
        else:
            qbuild.q = qbuild().filter(isPrivate=False)

        filterkeys = {
            'email' : 'email',
            'username' : 'username'
        }
        for buildkey, key in filterkeys.iteritems():
            qbuild.filter(buildkey, self.cleaned_data[key])

        if self.cleaned_data['is_active'] is not None:
            qbuild.filter('is_active', self.cleaned_data['is_active'])

        if not self.cleaned_data['limit'] or self.cleaned_data['limit'] < 0:
            qbuild.q = qbuild()[self.cleaned_data['offset']:]
        else:
            qbuild.q = qbuild()[self.cleaned_data['offset'] : self.cleaned_data['offset']+self.cleaned_data['limit']]

        return UserSerializer(qbuild(), many=True).data

class PostForm(forms.Form):
    # POST (data section) Body Parameters
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for creating a User
            once the form has cleaned the input data.
        '''
        # start saving the new tag now that it has passed all tests
        user = User(username=self.cleaned_data['username'], email=self.cleaned_data['email'],
            is_active=False, password=self.cleaned_data['password'])

        if self.cleaned_data['first_name']:
            user.first_name = self.cleaned_data['first_name']

        if self.cleaned_data['last_name']:
            user.last_name = self.cleaned_data['last_name']

        # begin the email sending process
        subject = 'Thank you for registering with BioDIG',
        from_email, to = settings.EMAIL, user.email
        html_content = '''
            <html>
                <body>
                    <p>Please click the link below to activate your account</p>
                    <a href=%s>Click Here</a>
                </body>
            </html>
        '''

        msg = EmailMultiAlternatives(subject, '', from_email, [to])

        userProfile = UserProfile(activation_key=str(uuid.uuid4()))

        try:
            user.save()
            userProfile.user = user
            userProfile.save()
            url = settings.SITE_URL + 'activate/%s/%s' % (str(user.pk), userProfile.activation_key)
            msg.attach_alternative(html_content % (url), "text/html")
            msg.send()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()

        return UserSerializer(user).data

class DeleteForm(forms.Form):
    # Path Parameters
    user_id = forms.IntegerField(required=True)

    def clean_user_id(self):
        return FormUtil.clean_user_id(self.cleaned_data)


    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for deleting a User
            once the form has cleaned the input data.
        '''

        try:
            user = User.objects.get(pk__exact=self.cleaned_data['user_id'])
        except (User.DoesNotExist, ValueError):
            raise UserDoesNotExist()

        if not request.user.is_staff and request.user != user:
            raise PermissionDenied()

        serialized = UserSerializer(user).data

        try:
            user.delete()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()

        return serialized

class PutForm(forms.Form):
    # Path Parameters
    user_id = forms.IntegerField(required=True)

    # Data Body Parameters
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    activation_key = forms.CharField(required=False)

    def clean_user_id(self):
        return FormUtil.clean_user_id(self.cleaned_data)

    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for updating a User
            once the form has cleaned the input data.
        '''
        try:
            user = User.objects.get(pk__exact=self.cleaned_data['user_id'])
        except (User.DoesNotExist, ValueError):
            raise UserDoesNotExist()

        if not request.user.is_staff and request.user != user:
            raise PermissionDenied()

        props = ['username', 'email', 'password', 'first_name', 'last_name']
        for key in props:
            # update the username
            if self.cleaned_data[key]:
                setattr(user, key, self.cleaned_data[key])

        if self.cleaned_data['activation_key']:
            profile = UserProfile.objects.get(user=user)
            if profile.activation_key == self.cleaned_data['activation_key']:
                user.is_active = True

        try:
            user.save()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()

        return UserSerializer(user).data

class SingleGetForm(forms.Form):
    # Path Parameters
    user_id = forms.IntegerField(required=True)

    def clean_user_id(self):
        return FormUtil.clean_user_id(self.cleaned_data)

    def submit(self, request):
        '''
            Submits the form for getting a User
            once the form has cleaned the input data.
        '''
        try:
            user = User.objects.get(pk__exact=self.cleaned_data['user_id'])
        except (User.DoesNotExist, ValueError):
            raise UserDoesNotExist()

        return UserSerializer(user).data
