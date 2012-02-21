from pmatch import *

def main():

  #
  # Ex 1
  #
  facto = Match(
                0, '1',
                1, '1',
                '_e_', '_e_ * rec(_e_ - 1)')
  print(facto(5))

  #
  # Ex 2
  #
  sum_all = Match(
                  [], '0',
                  'h::t', 'h + rec(t)')
  print(sum_all([1, 2, 3, 4]))

  #
  # Ex 3
  #
  mult = Match(
               [], '1',
               'h::t', 'h * rec(t)')
  print(mult([2, 4, 8]))

  #
  # Ex 4
  #
  l = [[x for x in range(1, 5)], [x for x in range(6, 10)]]
  m = Match(
            [[], []], 'print("over")',
            [[], '_e_'], 'print(_e_)',
            ['_e_', []], 'print(_e_)',
            ['e::h', 't::i'], 'rec([h,i])',
            '_', 'print(1337)')
  m(l)


if __name__ == '__main__':
  main()
