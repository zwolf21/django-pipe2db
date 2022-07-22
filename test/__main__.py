import argparse, os, sys

ENV_DIR = os.path.dirname(os.path.dirname(__file__))


try:
    from bookstore.insert import insert
except:
    sys.path.append(ENV_DIR)
    from bookstore.insert import insert




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