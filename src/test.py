from pmatch import *

def main():

  l = [[x for x in range(1, 5)], [x for x in range(5, 10)]]
  m = Match(
            [[], '_e_'], 'print(_e_)',
            ['_e_', []], 'print(_e_)',
            ['e::h', 't::i'], 'rec([h,i])',
            '_', 'print(1337)')

  print(m(l))

if __name__ == '__main__':
  main()
