from eigenflow.transitions import derivative_transition,peak_transition,consensus_transitions

def test_transition_helpers():
    d=derivative_transition([0,1,2],[0,1,5]); assert d["parameter"] in {1.0,2.0}
    p=peak_transition([0,1,2],[1,5,2]); assert p["parameter"]==1.0
    c=consensus_transitions([{"parameter":1.0},{"parameter":1.1},{"parameter":3}],.2); assert c["support"]==2
