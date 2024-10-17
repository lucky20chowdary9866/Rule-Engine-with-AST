

import ast

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type
        self.left = left
        self.right = right
        self.value = value

def create_rule(rule_string):
    rule_ast = ast.parse(rule_string, mode='eval')
    # The ast.parse function returns an ast.Expression object.
    # We need to access the body of this object to get the actual rule AST.
    return convert_ast(rule_ast.body) # Changed this line

def convert_ast(rule_ast):
    if isinstance(rule_ast, ast.BoolOp):
        node = Node("operator", value=rule_ast.op.__class__.__name__)
        node.left = convert_ast(rule_ast.values[0])
        node.right = convert_ast(rule_ast.values[1])
        return node
    elif isinstance(rule_ast, ast.Compare):
        node = Node("operand", value=f"{rule_ast.left.id} {get_operator(rule_ast.ops[0])} {rule_ast.comparators[0].n}")
        return node
    elif isinstance(rule_ast, ast.BinOp):
        node = Node("operator", value=get_operator(rule_ast.op))
        node.left = convert_ast(rule_ast.left)
        node.right = convert_ast(rule_ast.right)
        return node
    elif isinstance(rule_ast, ast.UnaryOp):
        node = Node("operator", value=get_operator(rule_ast.op))
        node.left = convert_ast(rule_ast.operand)
        return node
    else:
        raise ValueError("Unsupported AST node type")

def get_operator(op):
    if isinstance(op, ast.Add):
        return "+"
    elif isinstance(op, ast.Sub):
        return "-"
    elif isinstance(op, ast.Mult):
        return "*"
    elif isinstance(op, ast.Div):
        return "/"
    elif isinstance(op, ast.Eq):
        return "=="
    elif isinstance(op, ast.NotEq):
        return "!="
    elif isinstance(op, ast.Lt):
        return "<"
    elif isinstance(op, ast.LtE):
        return "<="
    elif isinstance(op, ast.Gt):
        return ">"
    elif isinstance(op, ast.GtE):
        return ">="
    else:
        raise ValueError("Unsupported operator")

#Create individual rules and verify their AST representation
rule1 = "age > 30 and department == 'Sales'"
rule2 = "age < 25 and department == 'Marketing'"

ast1 = create_rule(rule1)
ast2 = create_rule(rule2)

print(ast1.value)
print(ast2.value)

#Combine the example rules and ensure the resulting AST reflects the combined logic

combined_ast = combine_rules([rule1, rule2])

print(combined_ast.value)

def eval_operand(ast, json_data):
    operand_str = ast.value
    #print(operand_str)
    operand_parts = operand_str.split()
    if len(operand_parts) == 3: #check if the operand_parts have all 3 elements
        attr_name = operand_parts[0]
        operator = operand_parts[1]
        value = operand_parts[2]

        # handle int, float, and boolean string values
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                if value in ('True', 'False'):
                    value = value == 'True' # set value as True if string is 'True'
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1] # remove quotes for string variables

        attr_value = json_data[attr_name]

        if operator == "==":
            return attr_value == value
        elif operator == "!=":
            return attr_value != value
        elif operator == ">":
            return attr_value > value
        elif operator == ">=":
            return attr_value >= value
        elif operator == "<":
            return attr_value < value
        elif operator == "<=":
            return attr_value <= value
    else:
        return False

#Implement sample JSON data and test evaluate_rule for different scenarios
json_data1 = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
json_data2 = {"age": 20, "department": "Marketing", "salary": 40000, "experience": 2}

result1 = evaluate_rule(json_data1, combined_ast)
result2 = evaluate_rule(json_data2, combined_ast)

print(result1)
print(result2)

#Explore combining additional rules and test the functionality
rule3 = "salary > 50000 or experience > 5"
combined_ast = combine_rules([rule1, rule2, rule3])

json_data3 = {"age": 40, "department": "IT", "salary": 70000, "experience": 10}

result3 = evaluate_rule(json_data3, combined_ast)
print(result3)

#Error handling
def create_rule(rule_string):
    try:
        rule_ast = ast.parse(rule_string, mode='eval')
        return convert_ast(rule_ast)
    except SyntaxError:
        raise ValueError("Invalid rule string")

def evaluate_rule(json_data, ast):
    try:
        return eval_operand(ast, json_data)
    except KeyError:
        raise ValueError("Missing attribute in data")
    except TypeError:
        raise ValueError("Invalid data format")

#Atrribute validation
def create_rule(rule_string):
    ast = convert_ast(ast.parse(rule_string, mode='eval'))
    validate_attributes(ast)
    return ast

def validate_attributes(ast):
    if ast.node_type == "operand":
        attr_name = ast.value.split()[0]
        if attr_name not in ["age", "department", "salary", "experience"]:
            raise ValueError("Invalid attribute")
    elif ast.node_type == "operator":
        validate_attributes(ast.left)
        validate_attributes(ast.right)

import ast



def convert_ast(rule_ast):
    """
    Converts a Python AST to a custom AST format.
    """
    if isinstance(rule_ast, ast.Expression):
        # Extract the body for better handling
        return convert_ast(rule_ast.body)
    elif isinstance(rule_ast, ast.Compare):
        # Handle comparisons
        return create_node("operand", rule_ast.left.id + " " + get_operator(rule_ast.ops[0]) + " " + str(rule_ast.comparators[0].value))
    elif isinstance(rule_ast, ast.BoolOp):
        # Handle Boolean operations
        return create_node("operator", get_operator(rule_ast.op), convert_ast(rule_ast.values[0]), convert_ast(rule_ast.values[1]))

import ast



class Node:
    def __init__(self, node_type, value, left=None, right=None):
        self.node_type = node_type
        self.value = value
        self.left = left
        self.right = right

def create_node(node_type, value, left=None, right=None):
    """
    Creates a new node for the custom AST.
    """
    return Node(node_type, value, left, right)

def convert_ast(rule_ast):
    """
    Converts a Python AST to a custom AST format.
    """
    if isinstance(rule_ast, ast.Expression):
        # Extract the body for better handling
        return convert_ast(rule_ast.body)
    elif isinstance(rule_ast, ast.Compare):
        # Handle comparisons
        return create_node("operand", rule_ast.left.id + " " + get_operator(rule_ast.ops[0]) + " " + str(rule_ast.comparators[0].value))
    elif isinstance(rule_ast, ast.BoolOp):
        # Handle Boolean operations
        return create_node("operator", get_operator(rule_ast.op), convert_ast(rule_ast.values[0]), convert_ast(rule_ast.values[1]))

import ast



def get_operator(op):
    if isinstance(op, ast.Gt):
        return ">"
    elif isinstance(op, ast.Lt):
        return "<"
    elif isinstance(op, ast.GtE):
        return ">="
    elif isinstance(op, ast.LtE):
        return "<="
    elif isinstance(op, ast.Eq):
        return "=="
    elif isinstance(op, ast.NotEq):
        return "!="
    elif isinstance(op, ast.And):
        return "and"
    elif isinstance(op, ast.Or):
        return "or"
    else:
        raise ValueError("Unsupported operator")

#modifying existing rules
def modify_rule(ast, operator=None, operand_value=None):
    if ast.node_type == "operand":
        if operator:
            ast.value = f"{ast.value.split()[0]} {operator} {ast.value.split()[1]}"
        if operand_value:
            ast.value = f"{ast.value.split()[0]} {ast.value.split()[1]} {operand_value}"
    elif ast.node_type == "operator":
        if operator:
            ast.value = operator
        modify_rule(ast.left, operator, operand_value)
        modify_rule(ast.right, operator, operand_value)


rule_string = "age > 30 and department == 'Sales'"
ast = convert_ast(ast.parse(rule_string, mode='eval'))
modify_rule(ast, operator="<", operand_value="25")
print(ast.value)

import json

with open('rules.json') as f:
    rules_data = json.load(f)

for rule in rules_data["rules"]:
    print(f"Rule {rule['id']}: {rule['description']} - {rule['condition']} => {rule['action']}")