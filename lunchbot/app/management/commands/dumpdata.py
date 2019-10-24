import codecs
from django.core.management.commands.dumpdata import Command as Dumpdata


class Command(Dumpdata):
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--pretty', default=False, action='store_true',
            dest='pretty', help='Avoid unicode escape symbols'
        )

    def handle(self, *args, **kwargs):
        super(Command, self).handle(*args, **kwargs)
        if kwargs.get('pretty') and kwargs.get('output'):
            fname = kwargs.get('output')
            source = codecs.open(fname, 'br').read().decode('unicode_escape')
            codecs.open(fname, "w", encoding='utf-8').write(source)
