from django.core.management.base import BaseCommand

from ...models import Entity, Item, Location, Product


class Command(BaseCommand):
    help = 'Loads demo data'

    def handle(self, *args, **options):
        e_clerie = Entity(
            name="clerie",
        )
        e_clerie.save()

        e_e1mo = Entity(
            name="e1mo",
        )
        e_e1mo.save()

        e_margau = Entity(
            name="margau",
        )
        e_margau.save()

        e_fem = Entity(
            name="FeM",
        )
        e_fem.save()

        l_germany = Location(
            name="Germany",
        )
        l_germany.save()

        l_erfurt = Location(
            name="Erfurt",
            in_location=l_germany,
        )
        l_erfurt.save()

        l_fulda = Location(
            name="Fulda",
            in_location=l_germany,
        )
        l_fulda.save()

        l_fem_office = Location(
            name="FeM Office",
            in_location=l_germany,
            belongs_to=e_fem,
        )
        l_fem_office.save()

        p_thinkpad_l380 = Product(
            name="ThinkPad L380",
        )
        p_thinkpad_l380.save()

        p_ocedo_koala = Product(
            name="Ocedo Koala",
        )
        p_ocedo_koala.save()

        i_krypton = Item(
            name="krypton",
            product=p_thinkpad_l380,
            belongs_to=e_clerie,
        )
        i_krypton.save()

        i_flourine = Item(
            name="flourine",
            product=p_ocedo_koala,
            actual_location=l_fulda,
            belongs_to=e_margau,
        )
        i_flourine.save()
