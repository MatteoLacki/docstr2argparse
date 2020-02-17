A = ap.ArgumentParser('APEX')
A.add_argument('manna')
A.print_help()

A.parse_args(['10'])

B = ap.ArgumentParser('BPEX')
B.add_argument('hosanna')
B.print_help()

# vars(B)
# vars(B._positionals._group_actions)
# vars(B._positionals._group_actions[0])

C = ap.ArgumentParser(parents=[A,B], conflict_handler='resolve')
C.add_argument('manna')
C.print_help()

D = ap.ArgumentParser()
DA = D.add_argument_group('A')


C.parse_args(['10', '20', '30','30'])


parent_parser = ap.ArgumentParser(add_help=False)
parent_parser.add_argument('--parent', type=int)

foo_parser = ap.ArgumentParser(parents=[parent_parser])
foo_parser.add_argument('foo')
foo_parser.parse_args(['--parent', '2', 'XXX'])
foo_parser.print_help()

bar_parser = ap.ArgumentParser(parents=[parent_parser])
bar_parser.add_argument('--bar')
bar_parser.parse_args(['--bar', 'YYY'])
bar_parser.print_help()