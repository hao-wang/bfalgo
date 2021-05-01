def regex_to_postfix(re: str) -> str:
    """Convert RegExp to postfix expressions. Eg.
        eg.1: (ab)?ba -> ab.?b.a.
        eg.2: a(bb)+a -> abb.+.a.
        eg.3: a(bb)?c*b|abc -> abb.?.c*.b.ab.c.|
        eg.4: a(b|c)c*a+|abc|a(a+) -> abc|.c*.a+.ab.c.aa+.||

    Construct postfix string according to RegEx's operator precedence:
        [] > () > *+? > concat > ^$ > |

    n_atom counts the atomic operands, such as (ab) in eg.1, (bb) in eg.2,
     c* in eg.3, and all single symbolacters without trailing meta-symbols (
         like b, a in eg.1). Whenever n_atom > 1, we add a dot(.) to dst.

    n_alt counts the number of "|" (alternatives). Because alternative operator
    has the lowest precedence, we make sure characters on the two sides of |
    NOT concatenate by concatenate everything on the left ("clearance").

    Args:
        re (str): [description]

    Returns:
        str: [description]
    """
    dst = ''
    n_alt = 0
    n_atom = 0
    idx_p = 0
    p = []
    for symbol in re:
        if symbol == '(':
            if n_atom > 1:
                n_atom -= 1
                dst = dst + '.'

            # Save the snapshot before entering ()
            p.append({'n_alt': n_alt, 'n_atom': n_atom})
            n_atom = 0
            n_alt = 0
        elif symbol == ')':
            if len(p) == 0:
                return None
            if n_atom == 0:
                return None
            while n_atom > 1:  # n_atom should be at least 1
                n_atom -= 1
                dst = dst + '.'
            while n_alt > 0:
                n_alt -= 1
                dst = dst + '|'
            curr_paren = p.pop()

            # Restore the snapshot before entering on exiting
            n_alt = curr_paren['n_alt']
            n_atom = curr_paren['n_atom']
            n_atom += 1
        elif symbol == '|':
            if n_atom == 0:
                return None
            while n_atom > 1:
                n_atom -= 1
                dst = dst + '.'
            n_alt += 1
        elif symbol in ['*', '+', '?']:
            # special symbols must not exist without atomic, normal characters
            if n_atom == 0:
                return None
            dst = dst + symbol
        else:
            if n_atom > 1:
                n_atom -= 1
                dst = dst + '.'
            dst = dst + symbol
            n_atom += 1

    if len(p) != 0:
        return None
    while n_atom > 1:
        n_atom -= 1
        dst = dst + '.'
    while n_alt > 0:
        n_alt -= 1
        dst = dst + '|'

    return dst


if __name__ == "__main__":
    print(regex_to_postfix("(ab)?ba") == 'ab.?b.a.')
    print(regex_to_postfix("a(bb)+a") == 'abb.+.a.')
    print(regex_to_postfix("a(bb)?c*b|abc") == 'abb.?.c*.b.ab.c.|')
    print(regex_to_postfix("a(b|c)c*a+|abc|a(a+)") ==
          'abc|.c*.a+.ab.c.aa+.||')
