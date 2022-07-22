import argparse

from insert import insert


def main():
    
    argparser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='django-pipe2db test'
    )

    argparser.add_argument('appname', nargs='?', type=str)

    args = argparser.parse_args()

    if args.appname == 'insert':
        insert()



if __name__ == '__main__':
    main()