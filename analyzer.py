import ast
from pylint import epylint as lint

#Feedback for common mistakes
no_method = "No method called two_fer."
malformed_code = "The code is malformed and cannot be parsed for analysis."
simple_concat = "String concatenation with the + operator is a valid approach, but f-strings and str.format offer more " \
                "functionality and elegant solutions."
no_def_arg = "No default arguments are used in this solution. An ideal solution should make use of a default argument " \
             "and either f-strings or str.format."
conditionals = "Conditionals are unnecessarily used in this solution. An ideal solution should make use of a default " \
               "argument and either f-strings or str.format."
no_return = "'return' is not used to return the result string. This solution should fail pytest. Try run 'pytest' inside" \
            "the two-fer directory and observe the pass/fail results."

def analyze(user_solution):
    """
    Analyze the user's Two Fer solution to give feedback and disapprove malformed solutions.

    :return: A tuple containing a list of feedback comments as its first entry and a bool indicating whether a
        solution should be approved as its second entry.
    """

    try:
        tree = ast.parse(user_solution)
    except:
        #If ast.parse fails, the code is malformed
        return ([malformed_code], False, [])

    #List of comments to return at end, each comment is a string
    comments = []
    pylint_comments =[]
    #Whether to approve the user's solution based on analysis. Note that this only denotes if it's POSSIBLE for the
    #user's solution to be approved; just because the user didn't submit something that automatically makes it get
    #disapproved, like an empty file or missing method header, doesn't mean it's actually correct. Final assessment
    #of the user's solution must be done by a mentor.
    approve = True
    #Does the solution have a method called two_fer?
    has_method = False
    #Does the solution correctly use a default argument?
    uses_def_arg = False
    #Does the solution has return
    has_return = False

    for node in ast.walk(tree):
        #Search for method called two_fer
        if isinstance(node, ast.FunctionDef):
            if node.name == 'two_fer': has_method = True

        #Search for use of string concatenation with + operator
        elif isinstance(node, ast.Add) and simple_concat not in comments: comments += [simple_concat]

        #Search for use of default arguments
        elif isinstance(node, ast.arguments):
            if node.defaults: uses_def_arg = True

        #Search for use of unnecessary conditionals
        elif isinstance(node, ast.If) and conditionals not in comments: comments += [conditionals]

        #Search for return
        elif isinstance(node, ast.Return): has_return = True

    if not has_method:
        comments += [no_method]
        approve = False

    if not uses_def_arg:
        comments += [no_def_arg]

    if not has_return:
        comments += [no_return]
        approve = False

    # Use Pylint to generate comments for code, e.g. if code follows PEP8 Style Convention
    file = open('pylint_temp.txt',  'w')
    file.write(user_solution)
    file.close()
    (pylint_stdout, pylint_stderr) = lint.py_run('pylint_temp.txt', return_std=True)
    pylint_comments += [pylint_stdout.getvalue()]
    
    return (comments, approve, pylint_comments)
