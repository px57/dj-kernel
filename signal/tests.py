
import unittest
from .event import SIGNAL_CENTER

class TestSignal(unittest.TestCase):
    """
        @description: 
    """

    def test_create_existing_signal(self):
        """
            @description:
        """
        try:
            SIGNAL_CENTER.create(
                'profile.load_me',
                description="""
                    Fetch all the signal information of the user. 
                """
            )
        except Exception as e:
            self.assertEqual(
                str(e),
                'Event exists profile.load_me'
            )

    def test_show_signal_info(self):
        """
            @description:
        """
        # SIGNAL_CENTER.show_info('profile.load_me')
        pass

    def test_bind_receptor(self):
        """
            @description:
        """
        def test_de_cette_fonction():
            """
                @description:
            """
            print('test_de_cette_fonction')

        SIGNAL_CENTER.bind(
            'profile.load_me',
            test_de_cette_fonction
        )

    def test_unbind_receptor(self):
        """
            @description:
        """
        def test_de_cette_fonction():
            """
                @description:
            """
            print('test_de_cette_fonction')

        SIGNAL_CENTER.bind(
            'profile.load_me',
            test_de_cette_fonction
        )

        SIGNAL_CENTER.unbind(
            'profile.load_me',
            test_de_cette_fonction
        )

    def test_execute(self):
        """
            @description:
        """
        def test_de_cette_fonction():
            """
                @description:
            """
            print('#######################################33')

        SIGNAL_CENTER.bind(
            'profile.load_me',
            test_de_cette_fonction
        )

        SIGNAL_CENTER.execute('profile.load_me')

    def test_show_all_events(self):
        """
            @description:
        """
        SIGNAL_CENTER.show_all_events()


if __name__ == '__main__':
    SIGNAL_CENTER.create(
        'profile.load_me',
        description="""
            Fetch all the signal information of the user. 
        """
    )
    unittest.main()