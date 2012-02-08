from pmatch import *

def main():

  l = str([x for x in range(1, 10)])
  print(l)
  m = Match(
            [], 'print(69)',
            l, 'print("year")',
            'e::t', 'print(42)',
            '_', 'print(1337)')

  m(l)

if __name__ == '__main__':
  main()
