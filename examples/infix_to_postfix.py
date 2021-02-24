import ARgorithmToolkit

def precedence(a,b) -> bool:
    if b == '(' :
        return False
    order = {
        "+" : 1,
        "-" : 1,
        "*" : 2,
        "/" : 2,
        "^" : 3 
    }
    return order[a] <= order[b]

def run(**kwargs):
    algo = ARgorithmToolkit.StateSet()

    exp = ARgorithmToolkit.String(
        name="expr" , 
        algo=algo , 
        body=kwargs["expression"] , 
        comments="The infix expression"
        )

    st = ARgorithmToolkit.Stack(
        name="stack",
        algo=algo,
        comments="We will use a stack to convert infix to postfix" 
        )
    
    output = ARgorithmToolkit.String(
        name="output",
        algo=algo,
        comments="We will store the postfix expression in this"
    )

    for ch in exp:
        if ch.isalpha():
            output.append(ch,comments="character is operand so we directly add it to postfix")

        elif ch == '(':
            st.push(ch,comments="We push opening bracket into stack")

        elif ch == ')':
            while ( not st.empty() and st.top() != '('):
                a = st.pop(comments="pop operators till opening bracket is found")
                output.append(a)
            if ( not st.empty() and st.top() != '(' ):
                raise ARgorithmToolkit.ARgorithmClientError("Invalid infix expression")
            else:
                st.pop(comments="eject parenthesis from stack")

        else:
            try:
                while ( not st.empty() and precedence(ch,st.top())):
                    a = st.pop(comments="pop operators with higher precedence")
                    output.append(a)
                st.push(ch,comments="add operator to stack")
            except KeyError as ke:
                raise ARgorithmToolkit.ARgorithmClientError("Invalid operator used") from ke

    while not st.empty():
        a = st.pop(comments="Pop remaining operators to end of expression")
        output.append(a)

    algo.add_comment("Infix has been converted to postfix")

    return algo
