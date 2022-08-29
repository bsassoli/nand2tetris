"""Implements Tokenizer class to tokenize a .jack program"""
import re
from typing import List
from textwrap import dedent
from lexical_elements import SYMBOLS, KEYWORDS, SPECIAL_SYMBOLS


class Tokenizer:
    """Tokenizer _summary_
    """

    def __init__(self, path):
        """Initializes Tokenizer"""
        self.path = path
        self.current_token = ""
        self.current_position = -1
        self.tokens = []
        self.processed_lines = []
        self.tagged_tokens = []
        self.token_types = []

    def open(self) -> List[str]:
        """Opens file and return list of lines"""
        with open(self.path, "r") as file:
            lines = file.readlines()
        return lines

    def preprocess(self) -> List[str]:
        """Given a list of strings returns the same list without whitespaces,
            indentation, inline comments or line comments.
        """
        # Remove whitespace and indentation
        lines = self.open()
        lines = [dedent(line).strip() for line in lines]
        # Remove comments
        lines = [line for line in lines if line[:3] != "/**"]  # block comments
        lines = [line for line in lines if not line.startswith("*")]  # block comments
        lines = [line for line in lines if line[:2] != "//"]  # line comments
        lines = [line for line in lines if line[:2] != "*/"]  # end block comments
        lines = [line.split("//")[0].strip() for line in lines]  # inline comments
        # Remove empty lines
        lines = [line for line in lines if line != ""]
        # assert all(" " not in inline for inline in lines), "Whitespace present"
        self.processed_lines = [word for line in lines for word in line.split()]
        return self.processed_lines

    def has_more_tokens(self):
        """Checks whether reached end of program"""
        return self.current_position < len(self.tokens) - 1

    def advance(self):
        """Moves ahead and returns current token"""
        self.current_position += 1
        self.current_token = self.tokens[self.current_position]
        return self.current_token

    def token_type(self, token):
        """Given token return its type as string"""
        if token in KEYWORDS:
            return "keyword"
        if token in SYMBOLS:
            return "symbol"
        if token.isdigit():
            return "integerConstant"
        if token[0] == '"':
            return "stringConstant"
        return "identifier"

    def keyword(self, token):
        """Returns value of keyword"""
        assert self.token_type(token) == "keyword"
        return token

    def symbol(self, token):
        """Returns value of symbol"""
        assert self.token_type(token) == "symbol"
        return token

    def intVal(self, token):
        """Returns value of integer constant"""
        assert self.token_type(token) == "intConstant"
        return token

    def stringVal(self, token):
        """Returns value of string constant"""
        assert self.token_type(token) == "stringConstant"
        return token[1:-1]

    def identifier(self, token):
        """Returns value of identifier"""
        assert self.token_type(token) == "identifier"
        return token

    def tokenize(self):
        """Given list of lines returns list of tokens"""
        tokens = re.findall(r'"[^"]*"|\w+|[^\w\s]', " ".join(self.processed_lines))
        for token in tokens:
            self.tokens.append(token)
        return self.tokens

    def output_token(self, token):
        """Outputs a tagged token"""
        token_type = self.token_type(token)
        if token_type == "stringConstant":
            return (
                f"<{token_type}>" + " " + token[1:-1] + " " + f"</{token_type}>" + "\n"
            )
        if token_type == "symbol":
            if token in SPECIAL_SYMBOLS:
                return (
                    f"<{token_type}>"
                    + SPECIAL_SYMBOLS[token]
                    + f"</{token_type}>"
                    + "\n"
                )
            return f"<{token_type}>" + " " + token + " " + f" </{token_type}>" + "\n"
        return f"<{token_type}>" + " " + token + " " + f"</{token_type}>" + "\n"

    def write(self):
        """Writes list of tokens to file as filename_mine.xml"""
        with open(self.path.split(".")[0] + "MT" + ".xml", "w") as file:
            file.write("<tokens>\n")
            for token in self.tokens:
                tok = self.output_token(token)
                file.write(tok)
                self.tagged_tokens.append(tok)
                self.token_types.append(self.token_type(token))
            file.write("</tokens>\n")
