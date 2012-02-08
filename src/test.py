from pmatch import *

def main():

  m = Match(
            [], 'print([])',
            [42, []] , 'print(42)',
            {}, 'print({})',
            {'toto' : 42, 'tata' : '.*'}, 'print("dic toto")',
            '_', 'print("year")')

  m({'toto' : 42, 'tata' : 'aaaaaaa'})

if __name__ == '__main__':
  main()
