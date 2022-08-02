import argparse, os, sys

BASE_DIR = os.path.dirname(__file__)
ENV_DIR = os.path.dirname(BASE_DIR)
sys.path.append(ENV_DIR)

from bookstore.insert import insert, insert_and_update



def main():
    '''python test insert
    '''
    
    argparser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='django-pipe2db test'
    )

    argparser.add_argument('appname', nargs='?', type=str)

    args = argparser.parse_args()

    if args.appname == 'insert':
        insert()

    if args.appname == 'update':
        insert_and_update()



if __name__ == '__main__':
    main()