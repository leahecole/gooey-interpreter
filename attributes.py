from pypeg2 import *

#Various regex to catch different value types
rgbRegex = re.compile('\(\d{1,3}\,\s*\d{1,3}\,\s*\d{1,3}\)')
intRegex = re.compile('\d+')
hexRegex = re.compile('\#[A-Fa-f0-9]{6}')
actionPrint = re.compile('"(.*?)"')
valueRegex = re.compile('\"(.+?)\"|\w+')

#Colors
class ColorKeywordValue(Keyword):
	grammar = Enum(K("red"),K("blue"),K("green"))

class ColorRGBValue(str):
	grammar = rgbRegex

class ColorHEXValue(str):
	grammar = hexRegex

class ColorAttribute:
	grammar = "color", blank, attr("value", [ColorRGBValue, ColorHEXValue, ColorKeywordValue])

#Sizes
class SizeKeywordValue(Keyword):
	grammar = Enum(K("small"),K("large"))

class SizeIntValue(str):
	grammar = intRegex

class SizeAttribute:
	grammar = "size", blank, attr("value", [SizeKeywordValue, SizeIntValue])

#Parent window for a Button
class WindowAttribute:
	grammar = "window", blank, attr("value", name())

#Text
class TextAttribute:
	grammar = "text", blank, attr("value", word)

#Menu Values
class MenuValuesAttribute:
	grammar = "values", blank, attr("value", maybe_some(valueRegex))

#Button action (name of a function): 
class ActionAttribute:
	grammar = "action", blank, attr("value", word), optional(attr("text", actionPrint)), optional(attr("color", [ColorRGBValue, ColorHEXValue, ColorKeywordValue]))

#Wrap as Attribute object and put into AttributeList
class Attribute:
	grammar = [attr("color", ColorAttribute), attr("size", SizeAttribute), attr("window",WindowAttribute), attr("text",TextAttribute), attr("action",ActionAttribute), attr("values",MenuValuesAttribute)]

class AttributeList(List):
	grammar = csl(Attribute)
