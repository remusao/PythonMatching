from pmatch import *

def main():

  m = Match(
            [], 'return 1',
            'e::t', 'return (e * self(t))')

  m([1,2,3,4,5])

if __name__ == '__main__':
  main()
