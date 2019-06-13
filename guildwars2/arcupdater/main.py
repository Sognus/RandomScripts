from arcupdater import ArcUpdater
import argparse

# TODO: Allow users to configure updater behaviour via configuration file
# TODO: Check last-modified for build templates and extras before downloading files
# TODO: Create forced mode to ignore md5 and last-modified flags
# TODO: Terminal interface
# TODO: QT5 or tkinter user interface
# TODO: Allow user to delete or temporarily disable arcdps

def setup_argparse():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('-t', '--terminal', help='Run updater as terminal application', action='store_const', dest='mode',
                      const='t')
    mode.add_argument('-g', '--gui', help='Run updater as GUI application', action='store_const', dest='mode',
                      const='g')
    mode.add_argument('-n', '--no-output', help='Run updater without visual output', action='store_const', dest='mode',
                      const='n')
    parser.add_argument('--arc-url', help='Override arc download location', dest="arc_url")
    parser.add_argument('-f', '--folder', help='Specify arc root folder (same as GW2)', dest='arc_location')
    parser.add_argument('-e', '--extras', help='Enable update of arcdps extras', dest="arc_extras", action='store_true',
                        default=False)
    parser.add_argument('-b', '--templates', '--build-templates', help='Enable update of arcdps build templates',
                        dest="arc_templates", action='store_true', default=False)
    parser.set_defaults(mode='n')
    parser.set_defaults(arc_location=r'C:\Program Files\Guild Wars 2\bin64')
    parser.set_defaults(arc_url=r'https://www.deltaconnected.com/arcdps/x64/')
    return parser


def main():
    parser = setup_argparse()
    args = parser.parse_args()
    updater = ArcUpdater(args)


if __name__ == '__main__':
    main()
