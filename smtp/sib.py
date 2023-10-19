"""
    @description: Send in blue, a python wrapper for the Send in Blue API
"""

from __future__ import print_function

from django.conf import settings
from django.utils import timezone
from django.template.loader import get_template
from django.template import Context
# Template 
from django.template.loader import render_to_string

from kernel.http.request import generate_fake_request

from sib_api_v3_sdk.rest import ApiException

from profiles.models import UnsubscribeEmail
from pprint import pprint

import sib_api_v3_sdk
import os

def single_send_email(email, message):
    """
        @description:
    """
    send_email_html(html_content=message, destination_email=email, subject='Feedback AI', destination_name='TEST`')

def send_email_html(
    html_content='', 
    destination_email='', 
    subject='', 
    destination_name='',
):
    """
        @description: 
        @param: html_content
        @param: destination_email
        @param: subject
        @param: destination_name
        @return {void}
    """
    import time
    import sib_api_v3_sdk
    from sib_api_v3_sdk.rest import ApiException
    from pprint import pprint

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.ANYMAIL['SENDINBLUE_API_KEY']

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[
            {
                "email": "contact@example.com",
                "name": "Prepera"
            }
        ], 
        bcc=[{
            "name": destination_name,
            "email": destination_email
        }], 
        cc=[{
            "email":"example2@example2.com",
            "name":"Prepera"
        }],
        reply_to={
            "email": "contact@prepera.io",
            "name": "Prepera"
        }, 
        headers={
            "Some-Custom-Name": "unique-id-1234"
        },
        html_content=html_content, 
        sender={
            "name": "Prepera",
            "email": "noreply@prepera.io"
        }, 
        subject=subject
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)



def unsubscribed_email(profile, email_name):
    """
        @description:
    """
    if email_name in settings.NOT_UNSUSCRIBABLE_EMAIL:
        return False
    
    if UnsubscribeEmail.objects.filter(profile=profile).exists():
        return True
    return False


def get_all_campaign():
    """
        @description: 
    """
    instance = get_instance()
    api_instance = sib_api_v3_sdk.EmailCampaignsApi(sib_api_v3_sdk.ApiClient(instance))
    # type = 'classic'
    status = 'draft'
    limit = 100
    offset = 0

    try:
        api_response = api_instance.get_email_campaigns(
            # type=type, 
            # status=status, 
            limit=limit, 
            offset=offset
        )
        return api_response
    except ApiException as e:
        print("Exception when calling EmailCampaignsApi->get_email_campaigns: %s\n" % e)

def sendinblue__send_email(template_id, profile, subject='My Subject'):
    """
        @description: Send an email campaign now, based on a campaign id
    """
    instance = get_instance()
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(instance))

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[
            {
                "email": "contact@example.com",
                "name": "Prepera"
            }
        ], 
        bcc=[{
            "name": 'Mr ' + profile.user.first_name + ' ' + profile.user.last_name,
            "email": profile.user.email
        }], 
        cc=[{
            "email":"example2@example2.com",
            "name":"Prepera"
        }], 
        reply_to={
            "email": "contact@prepera.io",
            "name": "Prepera"
        }, 
        headers={
            "Some-Custom-Name": "unique-id-1234"
        },
        template_id=template_id,
        sender={
            "name": "Prepera",
            "email": "noreply@prepera.io"
        }, 
        subject=subject,
        params={
            'TOKENFORGETPASSWORD': 'https://www.google.fr/oeauoeuaoeu',
            'PRENOM': '@@@@@@@@@@@@@@@@@@@@@@@@@',
            'contact': {
                'PRENOM': '@@@@@@@@@@@@@@@@@@@@@@@@@',
            }
        },
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)


def get_instance():
    """
        @description: Generate a Send in Blue instance.
    """
    # Configure API key authorization: api-key
    instance = sib_api_v3_sdk.Configuration()
    instance.api_key['api-key'] = settings.ANYMAIL.get('SENDINBLUE_API_KEY')
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # configuration.api_key_prefix['api-key'] = 'Bearer'
    # Configure API key authorization: partner-key
    # instance = sib_api_v3_sdk.Configuration()
    # instance.api_key['partner-key'] = 'YOUR_API_KEY'
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # configuration.api_key_prefix['partner-key'] = 'Bearer'

    # create an instance of the API class
    return instance

def get_template():
    """
        @description: 
    """
    instance = get_instance()
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(instance))
    limit = 50
    offset = 0

    try:
        api_response = api_instance.get_smtp_templates(limit=limit, offset=offset)
        return api_response
    except ApiException as e:
        print("Exception when calling SMTPApi->get_smtp_templates: %s\n" % e)
    return None

class EmailTemplate:    
    """
        @description:
    """

    def __init__(self) -> None:
        """
            @description:
        """
        self.complex_name = {
            'en': None,
            'fr': None,
        }
        self.template_id = None

    def get_name(self):
        """
            @description: 
        """
        for key_name in self.complex_name:
            if self.complex_name[key_name] is not None:
                return self.complex_name[key_name]['name']
        return None

    def setComplexName(self, complex_name, template):
        """
            @description: Save the complex name of the template.
            @immutable: After set, the complex name cannot be changed.
        """
        if self.complex_name[complex_name['language']] is not None:
            return
        
        self.complex_name[complex_name['language']] = complex_name
        self.complex_name[complex_name['language']]['template'] = template

    def update(self, new_template):
        """
            @description:
        """

    def get_template_path(self, profile):
        """
            @description:
        """
        path = 'email/'
        path = os.path.join(path, self.complex_name[profile.language]['name'] + '_' + profile.language + '.html')
        return path
    
    def get_real_template_path(self, profile):
        """
            @description:
        """
        template_path = self.get_template_path(profile)
        template_path = os.path.join('templates', template_path)
        template_path = os.path.join(settings.BASE_DIR, template_path)
        return template_path

    def get_or_create_template(self, profile):
        """
            @description:
        """
        template_path = self.get_template_path(profile)
        if os.path.exists(template_path):
            return template_path

        fd = open(self.get_real_template_path(profile), 'w+')
        fd.write(self.complex_name[profile.language]['template'].html_content)
        fd.close()
        return template_path

    def generate_html_content(self, profile, ctx):
        """
            @description:
        """
        template_path = self.get_or_create_template(profile)
        html_content = self.complex_name[profile.language]['template'].html_content
        html_content = render_to_string(template_path, ctx)
        return html_content



    def send_email(self, profile, ctx):
        """
            @description: 
            @param: profile: The profile of the user
            @param: ctx: The context of the email
        """
        if unsubscribed_email(profile, self.complex_name[profile.language]['name']):
            return
        
        template = self.complex_name[profile.language]['template']
        html_content = template.html_content
        subject = template.subject
        sender = template.sender

        # -> add the unsubscribe link
        ctx['unsubscribe'] = os.path.join(settings.DOMAIN, 'unsubscribe/' + profile.user.email)

        request = generate_fake_request()

        # -> la liste des emails que l'ont va envoyer avec ce processus.
        send_email_html_list = [
            'FORGOT_PASSWORD',
        ]

        if self.get_name() in send_email_html_list:
            send_email_html(
                html_content=self.generate_html_content(profile, ctx),
                destination_email=profile.user.email, 
                subject=template.subject,
                destination_name='Mr ' + profile.user.first_name + ' ' + profile.user.last_name,
            )
            return;
    
        sendinblue__send_email(template.id, profile, template.subject)


class EmailTemplateList:
    """
        @description:
    """
    def __init__(self) -> None:
        """
            @description:
        """
        self.email_templates_attach = self.__generate_template_attach(settings.EMAIL_TEMPLATE)
        self.template = {}
        self.__load(self.template)
    
    def __generate_template_attach(self, EMAIL_TEMPLATE):
        """
            @description:
        """
        email_templates_attach = {}
        email_templates_attach = EMAIL_TEMPLATE.copy()
        return email_templates_attach

    def __create_email_template_dir(self):
        """
            @description: If not exists create email_template directory
        """
        if not os.path.exists('email_template'):
            os.mkdir('email_template')

    def __load(self, template_list):
        """
            @description:
        """
        self.__create_email_template_dir()
        # try:
        templates = get_template()
        self.__load_totemplates(templates)
    
    def __load_tofile_cache(self):
        """
            @description: 
        """

    def __load_totemplates(self, templates):
        """
            @description: 
        """
        for template in templates.templates:
            complex_name = self.__get_the_languagetothename(template.name)
            if complex_name is None:
                continue
            if complex_name['name'] not in self.template:
                self.template[complex_name['name']] = EmailTemplate()
            self.template[complex_name['name']].setComplexName(complex_name, template)
            self.__save_htmlto_file(
                complex_name['name'],
                complex_name['language'],
                template
            )
        

    def show_template(self):
        """
            @description:
        """
        print ('*** Template list ***')
        for key in self.template:
            if key == 'FORGOT_PASSWORD':
                print (self.template[key].complex_name['en'])
            print ('    - ' + key)

    def __save_htmlto_database(self):
        """
            @description: 
        """
        pass
        # for key in self.email_templates_attach:
        #     if template.id == self.email_templates_attach[key]:
        #         fd = open('email_template/%s.html' % key, 'w')
        #         template.html_content = template.html_content.replace('#top', '<%= URL %>?code=<%= TOKEN %>')
        #         fd.write(template.html_content)
        #         fd.close()
        #         break

    def __save_htmlto_file(self, name, language, template):
        """
            @description:
        """
        key = name + '_' + language
        # fd = open('email_template/%s.html' % key, 'w')
        
        # fd.write(template.html_content)
        # fd.close()

    def __get_the_languagetothename(self, name):
        """
            @description:
            @example: Welcome - Association (fr)
            @return: {
                'name': 'Welcome - Association ',
                'language': 'fr'
            }
        """
        complex_name = {}
        if '(' in name:
            complex_name['name'] = name.split('(')[0].strip()
            complex_name['language'] = name.split('(')[1].replace(')', '').strip()
        else:
            complex_name['name'] = name
            complex_name['language'] = 'en'
        complex_name['name'] = self.__uniformize_name(complex_name['name'])

        if complex_name['language'] not in ['en', 'fr']:
            return None
        
        return complex_name
    
    def __uniformize_name(self, name):
        """
            @description: Supprime les caractères spéciaux et remplace les espaces par des _
            @example: Welcome - Association (fr)
            @return: welcome_association
        """
        name = ' '.join(name.split())
        replace_list = [
            ' ', 
            '-', 
            '\\', 
            '(', 
            ')', 
            '?', 
            '!', 
            ','
        ]
        for replace in replace_list:
            name = name.replace(replace, '_')
        
        # delete multiple _ 
        # WELCOME___SCHOOLS -> WELCOME_SCHOOLS
        while '__' in name:
            name = name.replace('__', '_')

        # delete _ at the end
        # WELCOME_SCHOOLS_ -> WELCOME_SCHOOLS
        if name[-1] == '_':
            name = name[:-1]

        # delete _ at the start
        # _WELCOME_SCHOOLS -> WELCOME_SCHOOLS
        if name[0] == '_':
            name = name[1:]

        name = name.upper()
        return name

    def __get_email_to_rattach(self, template_id):
        """
            @description:
        """
        for template in self.email_templates_attach:
            if self.email_templates_attach[template] == template_id:
                return template
        return None

    def update(self):
        """
            @description:
        """
        self.__load(self.template)
        LAST_UPDATE_TEMPLATE = timezone.now()

    def send_email(self, profile, template, ctx):
        """
            @description:
            @params: dbProfile
            @params: template -> complex_name['name']
            @params: ctx -> context
        """
        if template not in self.template:
            raise Exception('Template not found ' + template)
        self.template[template].send_email(profile, ctx)

LAST_UPDATE_TEMPLATE = None
EMAIL_TEMPLATE_LIST = EmailTemplateList()

