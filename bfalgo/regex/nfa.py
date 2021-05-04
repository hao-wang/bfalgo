import sys

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
            # n_atom should be at least 1
            while n_atom > 1:  
                n_atom -= 1
                dst = dst + '.'
            while n_alt > 0:
                n_alt -= 1
                dst = dst + '|'
            curr_paren = p.pop()

            # Restore the snapshot before entering on exiting.
            n_alt = curr_paren['n_alt']
            n_atom = curr_paren['n_atom']
            n_atom += 1
        elif symbol == '|':
            if n_atom == 0:
                return None
            while n_atom > 1:
                n_atom -= 1
                dst = dst + '.'
            # Force clear n_atom, no concatenation between the two sides.
            n_atom = 0  
            n_alt += 1
        elif symbol in ['*', '+', '?']:
            # special symbols cannot exist without normal chars.
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

# for ascii characters
SPLIT = 256  
MATCHED = 257
state_id = 0

class State:
    def __init__(self, value, out, out1):
        """
        State is classified by value,
            value (int): 
                <256 ('consume'), 
                256 ('split'), 
                257 ('stop' or 'matched') 
        and has different out pointers:
            out (State): 
            out1 (State): 
        """
        global state_id
        self.state_id = state_id
        self.value = value
        self.out = out  # a single state or None
        self.out1 = out1  # a single state or None
        state_id += 1

    def collect_state(s, layer, all_states):
        # !!!Danger: mind the loops
        if s.out is not None:
            collect_state(s.out, layer+1)
        if s.out1 is not None:
            collect_state(s.out1, layer+1)
        
    def __repr__(self):
        collect_state(self, 0)

    

class Fragment:
    """An NFA is composed of Fragment's. Each fragment is a black box,
    exposing to outside world with a start state and a list of connected
    pointers, pointing to None or some state. 
    """
    def __init__(self, start: State, out: 'list[State]'):
        self.start = start
        self.out = out

def patch(outlist, state):
    """

    Args:
        outlist ([type]): [description]
        state ([type]): [description]
    """
    outlist.pop()
    outlist.append(state)
    return outlist

def join_outs(outlist1: 'list[State]', outlist2: 'list[State]'):
    """The last element of outlist1 is always None

    Args:
        outlist1 (List[State]): [description]
        outlist2 (List[State]): [description]
    """
    outlist1.pop()
    return outlist1.extend(outlist2)

def list1(state: State):
    return [state] 

def postfix_to_nfa(postfix):
    nfa_nodes = []
    for rc in postfix:
        if rc == '.':
            e2 = nfa_nodes.pop()
            e1 = nfa_nodes.pop()
            patch(e1.out, e2.start)
            nfa_nodes.append(Fragment(e1.start, e2.out))
        elif rc == '|':
            e2 = nfa_nodes.pop()
            e1 = nfa_nodes.pop()
            s = State(SPLIT, e1.start, e2.start)
            nfa_nodes.append(Fragment(s, join_outs(e1.out, e2.out)))
        elif rc == '*':
            e1 = nfa_nodes.pop()
            s = State(SPLIT, e1.start, None)
            patch(e1.out, s)
            nfa_nodes.append(Fragment(s, list1(s.out1)))
        elif rc == '?':
            e1 = nfa_nodes.pop()
            s = State(SPLIT, e1.start, None)
            nfa_nodes.append(Fragment(s, join_outs(e1.out, list1(s.out1))))
        elif rc == '+':
            e1 = nfa_nodes.pop()
            s = State(SPLIT, e1.start, None)
            patch(e1.out, s)
            nfa_nodes.append(Fragment(e1.start, list1(s.out1)))
        else:
            s = State(rc, None, None)
            nfa_nodes.append(Fragment(s, list1(s.out)))
    
    e = nfa_nodes.pop()
    if len(nfa_nodes) != 0:
        return None
    patch(e.out, State(MATCHED, None, None))
    return e

def ismatch(l: 'list[State]') -> bool:
    for s in l:
        if s.value == MATCHED:
            return 1
    return 0

def addstate(state_list: 'list[State]', state: State):
    if state.value == SPLIT:
        addstate(state_list, state.out)
        addstate(state_list, state.out1)
        return    
    else:
        state_list.append(state)

def step(current_states, c):
    next_states = []
    for s in current_states:
        if s.value == c:
            addstate(next_states, s.out) 
    return next_states 

def match(start: State, string: str) -> bool:
    clist = [start]
    nlist = []
    for c in string:
        c = ord(c)
        clist = step(clist, c)
    return ismatch(clist)

def main(reg, string):
    postfix = regex_to_postfix(reg)
    if postfix is None:
        print(f"Bad regexp {reg}\n")

    nfa = postfix_to_nfa(postfix)
    print("ho")

    if match(nfa, string):
        print(f"{string} matched RegEx {reg}")
    return 0

if __name__ == "__main__":
    test_cases = [
        ("(ab)?ba", "ab.?b.a."), 
        ("a(bb)+a", "abb.+.a."),
        ("a(bb)?c*b|abc", "abb.?.c*.b.ab.c.|"), 
        ("a(b|c)c*a+|abc|a(a+)", "abc|.c*.a+.ab.c.aa+.||")
        ]
    for reg, s in test_cases:
        if regex_to_postfix(reg) != s:
            print(f"{reg} --> {regex_to_postfix(reg)} (should be {s})")

    reg, string = sys.argv[1:]
    main(reg, string)