from django.core.management.base import BaseCommand, CommandError
from argo_floats.utils import crawl

class Command(BaseCommand):
    args = '<url> <select>'
    help = '''
        Add Argo float to archive. 
        
        Args:
            <url>: the url to the thredds server
            <select>: You can select datasets based on their THREDDS ID using
            the 'select' parameter

            url = http://tds0.ifremer.fr/thredds/catalog/CORIOLIS-ARGO-GDAC-OBS/kordi/catalog.html

        '''
 
    def add_arguments(self, parser):
        parser.add_argument('url', nargs='*', type=str)
#        parser.add_argument('--platnum',
#                            action='store',
#                            default='',
#                            help='''Argo float number''')
#        parser.add_argument('--filename',
#                            action='store',
#                            default='',
#                            help='''Filename of a specific dataset''')

    def handle(self, *args, **options):
        if not len(options['url'])==1:
            raise IOError('Please provide a url to the data')
        url = options.pop('url')[0]
        print(url)
        added = crawl(url)
        self.stdout.write(
            'Successfully added metadata of %s Argo float profiles' %added)
