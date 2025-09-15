import ttg
import time

variables = []

# Truth table operations and the ttg variant
operations = {
    "∧": " and ",
    "&": " and ",
    "&&": " and ",
    "^": " and ",
    "|": " or ",
    "||": " or ",
    "∨": " or ",
    "~": " not ",
    "¬": " not ",
    "!": " not ",
    "->": " implies ",
    "=>": " implies ",
    "⇒": " implies ",
    "<->": " = ",
    "<=>": " = ",
    "⇔": " = "
}

while True:
    # Define your expression (user input works too)
    expression = input("\nInput expression here please : ")
    if expression.lower() in ['exit', 'keluar']:
        print("Exiting the program. Goodbye!")
        time.sleep(1)
        break

    # Add all alphabetical variables
    for char in expression:
        if char.isalpha() and char not in variables:
            variables.append(char)

    # Handle reverse implication (⇐) by converting it to forward implication
    # A ⇐ B is equivalent to B ⇒ A
    def handle_reverse_implication(expr):
        # Find all instances of reverse implication
        while '⇐' in expr:
            # Find the position of ⇐
            pos = expr.find('⇐')

            # Find the left operand (work backwards from ⇐)
            left_end = pos - 1
            while left_end >= 0 and expr[left_end] == ' ':
                left_end -= 1

            if expr[left_end] == ')':
                # Handle parentheses - find matching opening parenthesis
                paren_count = 1
                left_start = left_end - 1
                while left_start >= 0 and paren_count > 0:
                    if expr[left_start] == ')':
                        paren_count += 1
                    elif expr[left_start] == '(':
                        paren_count -= 1
                    left_start -= 1
                left_start += 1
            else:
                # Simple variable - work backwards to find start
                left_start = left_end
                while left_start > 0 and (expr[left_start-1].isalpha() or expr[left_start-1] == '~' or expr[left_start-1] == ' '):
                    left_start -= 1
                    if left_start > 0 and expr[left_start-1] != ' ' and expr[left_start-1] != '~':
                        break

            # Find the right operand (work forwards from ⇐)
            right_start = pos + 1
            while right_start < len(expr) and expr[right_start] == ' ':
                right_start += 1

            if right_start < len(expr) and expr[right_start] == '(':
                # Handle parentheses - find matching closing parenthesis
                paren_count = 1
                right_end = right_start + 1
                while right_end < len(expr) and paren_count > 0:
                    if expr[right_end] == '(':
                        paren_count += 1
                    elif expr[right_end] == ')':
                        paren_count -= 1
                    right_end += 1
                right_end -= 1
            else:
                # Simple variable or negation - work forwards to find end
                right_end = right_start
                if right_start < len(expr) and expr[right_start] == '~':
                    right_end += 1
                    while right_end < len(expr) and expr[right_end] == ' ':
                        right_end += 1
                while right_end < len(expr) and expr[right_end].isalpha():
                    right_end += 1
                right_end -= 1

            # Extract operands
            left_operand = expr[left_start:left_end+1].strip()
            right_operand = expr[right_start:right_end+1].strip()

            # Replace A ⇐ B with B ⇒ A
            replacement = f"{right_operand} ⇒ {left_operand}"
            expr = expr[:left_start] + replacement + expr[right_end+1:]

        return expr

    # Handle reverse implication
    expression = handle_reverse_implication(expression)

    # Replace operations in the correct order (longest first to avoid conflicts)
    # Sort keys by length in descending order
    sorted_operations = sorted(operations.items(), key=lambda item: len(item[0]), reverse=True)
    for key, value in sorted_operations:
        expression = expression.replace(key, value)

    # Replace all brackets with curly ones
    expression = expression.replace("[", "(")
    expression = expression.replace("]", ")")

    print(f"Processed expression: {expression}")
    print(f"Variables found: {variables}")

    # Create the truth table
    table = ttg.Truths(variables, [expression])

    # Print the table
    print(table)

    # Clear variables for next iteration
    variables.clear()