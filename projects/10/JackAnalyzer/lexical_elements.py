"""Constants for reference by Parser and Tokenizer"""
from typing import List, Dict

KEYWORDS: List[str] = [
    "class",
    "constructor",
    "function",
    "method",
    "field",
    "static",
    "var",
    "int",
    "char",
    "boolean",
    "void",
    "true",
    "false",
    "null",
    "this",
    "let",
    "do",
    "if",
    "else",
    "while",
    "return",
]

SYMBOLS: List[str] = [
    ".",
    ",",
    ";",
    "+",
    "-",
    "*",
    "/",
    "(",
    ")",
    "{",
    "}",
    "[",
    "]",
    "&",
    "|",
    ">",
    "<",
    "~",
    "=",
]


LEXICAL_ELEMENTS: List[str] = [
    "keyword",
    "symbol",
    "integerConstant",
    "stringConstant",
    "identifier",
]
SPECIAL_SYMBOLS: Dict[str, str] = {
    "<": "&lt;",
    ">": "&gt;",
    "&": "&amp;",
    '"': "&quot;",
}
