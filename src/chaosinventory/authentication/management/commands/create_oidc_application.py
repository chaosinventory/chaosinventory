from django.core.exceptions import ValidationError
from django.core.management.base import (
    BaseCommand, CommandError, CommandParser,
)
from django.core.validators import URLValidator

from chaosinventory.authentication.models import OIDCApplication


def ask_parameter(label: str = 'Value: '):
    user_input = input(label).strip()
    return None if not user_input else user_input


def validate_uri(uri: str, raise_error: bool = True) -> bool:
    try:
        URLValidator()(uri)
    except ValidationError:
        if not raise_error:
            return False
        raise CommandError(f'{uri} is not a valid URL.')
    return True


class Command(BaseCommand):
    help = 'Creat an OIDCApplication.'
    requires_migrations_checks = True

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            'name',
            help='Name of the application',
        )
        parser.add_argument(
            '--description',
            help='Description for the Application',
            required=False,
        )
        parser.add_argument(
            'access_type',
            help='Access type for the Application.',
            choices=[
                i[0] for i in OIDCApplication.ACCESS_TYPES
            ],
        )
        parser.add_argument(
            '--default-redirect',
            help='The default / fallback redirect uri.'
        )
        parser.add_argument(
            '--redirect',
            help=(
                'A list of redirect uris. At least one is required. '
                'NOTE: Currently, no wildcards are supported!'
            ),
            nargs='*',
            default=[]
        )

        parser.add_argument(
            '--no-interactive',
            '-n',
            help='Do not prompt for optional undefined arguments.',
            action='store_true',
            default=False,
        )

    def handle(self, *args, **options):
        if not options['no_interactive']:
            if not options['description']:
                options['description'] = ask_parameter(
                    'Description (empty line to skip): '
                )

            if len(options['redirect']) < 1:
                last_input = True
                self.stdout.write(
                    'Enter redirect uris line by line. '
                    'Enter a new line to end the input. '
                    'At least one is required!'
                )
                while last_input is not None:
                    last_input = ask_parameter('> ')
                    if last_input is not None:
                        options['redirect'].append(last_input)

            if not options['default_redirect']:
                options['default_redirect'] = ask_parameter(
                    'Enter default redirect uri (empty to skip): '
                )

        if len(options['redirect']) < 1:
            raise CommandError('At least one redirect uri must be specified!')

        default_redirect = options['default_redirect']

        for uri in options['redirect']:
            validate_uri(uri)
        if default_redirect is not None:
            validate_uri(default_redirect)

        application = OIDCApplication(
            name=options['name'],
            description=options['description'],
            access_type=options['access_type'],
            redirect_uris=options['redirect'],
            default_redirect_uri=default_redirect,
        )

        client_secret = application.generate_new_client_secret(save=False)

        try:
            application.full_clean()
        except ValidationError as e:
            raise CommandError(e)
        application.save()

        self.stdout.write(
            self.style.SUCCESS('\nApplication created!\n\n') +
            '{:<16} {}\n{:<16} {}'.format(
                'client_id:',
                application.pk,
                'client_secret:',
                client_secret
            )
        )
