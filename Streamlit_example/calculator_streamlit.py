import ast
import math
import operator
import re

import streamlit as st


st.set_page_config(
	page_title="Calculator",
	page_icon=":material/calculate:",
	layout="centered",
)


def _checked_number(value):
	try:
		number = float(value)
	except OverflowError as error:
		raise ValueError("That result is too large to display.") from error
	if not math.isfinite(number):
		raise ValueError("That result is outside the calculator's range.")
	return number


def _evaluate_node(node):
	if isinstance(node, ast.Expression):
		return _evaluate_node(node.body)
	if isinstance(node, ast.Constant) and type(node.value) in (int, float):
		return _checked_number(node.value)
	if isinstance(node, ast.UnaryOp) and type(node.op) in (ast.UAdd, ast.USub):
		operand = _evaluate_node(node.operand)
		return _checked_number(operand if isinstance(node.op, ast.UAdd) else -operand)

	operations = {
		ast.Add: operator.add,
		ast.Sub: operator.sub,
		ast.Mult: operator.mul,
		ast.Div: operator.truediv,
		ast.Mod: operator.mod,
	}
	if isinstance(node, ast.BinOp) and type(node.op) in operations:
		left = _evaluate_node(node.left)
		right = _evaluate_node(node.right)
		return _checked_number(operations[type(node.op)](left, right))

	raise ValueError("Use numbers and basic arithmetic operators only.")


def _calculate(expression):
	if not expression.strip():
		raise ValueError("Enter an expression first.")
	if len(expression) > 120:
		raise ValueError("Keep expressions under 120 characters.")

	normalized = expression.translate(str.maketrans({"÷": "/", "×": "*", "−": "-"}))
	normalized = re.sub(r"(?<=[0-9)])%", "/100", normalized)
	try:
		tree = ast.parse(normalized, mode="eval")
	except SyntaxError as error:
		raise ValueError("Check the expression and try again.") from error
	if sum(1 for _ in ast.walk(tree)) > 80:
		raise ValueError("That expression is too complex.")
	return _evaluate_node(tree)


def _format_result(value):
	return f"{value:,.10g}"


def _calculate_current():
	expression = st.session_state.expression
	try:
		value = _calculate(expression)
	except (ValueError, ZeroDivisionError) as error:
		st.session_state.error = str(error)
		st.session_state.has_result = False
		return

	formatted = _format_result(value)
	st.session_state.history.insert(0, (expression, formatted))
	st.session_state.history = st.session_state.history[:6]
	st.session_state.expression = format(value, ".12g")
	st.session_state.error = ""
	st.session_state.has_result = True


def _press_key(label):
	if label == "AC":
		st.session_state.expression = ""
		st.session_state.error = ""
		st.session_state.has_result = False
		return
	if label == "⌫":
		st.session_state.expression = st.session_state.expression[:-1]
	elif label == "=":
		_calculate_current()
		return
	else:
		if st.session_state.has_result and (label.isdigit() or label in (".", "(")):
			st.session_state.expression = ""
		st.session_state.expression += label

	st.session_state.error = ""
	st.session_state.has_result = False


st.session_state.setdefault("expression", "")
st.session_state.setdefault("history", [])
st.session_state.setdefault("error", "")
st.session_state.setdefault("has_result", False)

st.title("Calculator", icon=":material/calculate:")
st.caption("A clear workspace for quick, accurate arithmetic.")

calculator_column, history_column = st.columns([1.35, 0.8], gap="large", vertical_alignment="top")

with calculator_column:
	with st.container(border=True):
		st.caption("EXPRESSION")
		st.text_input(
			"Expression",
			key="expression",
			placeholder="Try 12 × (4 + 3)",
			label_visibility="collapsed",
			on_change=_calculate_current,
		)

		try:
			preview = _calculate(st.session_state.expression)
			preview_text = _format_result(preview)
		except (ValueError, ZeroDivisionError):
			preview_text = "—"
		st.metric("Live result", preview_text)

		if st.session_state.error:
			st.error(st.session_state.error, icon=":material/error:")

		keypad = [
			["AC", "(", ")", "⌫"],
			["7", "8", "9", "÷"],
			["4", "5", "6", "×"],
			["1", "2", "3", "−"],
			["0", ".", "%", "+"],
		]
		for row_index, row in enumerate(keypad):
			columns = st.columns(4, gap="small")
			for column_index, label in enumerate(row):
				with columns[column_index]:
					if label == "⌫":
						st.button(
							"Delete",
							icon=":material/backspace:",
							help="Delete the last character",
							key=f"key_{row_index}_{column_index}",
							width="stretch",
							on_click=_press_key,
							args=(label,),
						)
					else:
						st.button(
							label,
							key=f"key_{row_index}_{column_index}",
							width="stretch",
							on_click=_press_key,
							args=(label,),
						)

		st.button(
			"Calculate",
			icon=":material/equal:",
			key="calculate",
			type="primary",
			width="stretch",
			on_click=_calculate_current,
		)

with history_column:
	with st.container(border=True):
		st.subheader("Recent calculations", icon=":material/history:")
		if st.session_state.history:
			for expression, result in st.session_state.history:
				st.text(f"{expression}  =  {result}")
			st.button(
				"Clear history",
				icon=":material/delete:",
				key="clear_history",
				on_click=lambda: st.session_state.update(history=[]),
			)
		else:
			st.caption("Your latest calculations will appear here.")

		st.caption("Percent converts a value to a fraction of 100.")
