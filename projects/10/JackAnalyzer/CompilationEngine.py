""" For every non-terminal building block of the language,
we equip the parser with a recursive procedure designed
to parse that non- terminal. If the non-terminal consists
of terminal atoms only, the procedure will simply read them.
Otherwise, for every non-terminal building block, the
procedure will recursively call the procedure designed to
parse the non-terminal. The process will continue recursively,
until all the terminal atoms have been reached and read.
"""

from typing import List
import math

class Compiler:
    """Compiler _summary_
    """

    def __init__(self, tokens: List[str], tagged: List[str], output: str):
        """__init__ _summary_

        Args:
            input (List[str]): _description_
            output (str): _description_
        """
        self.tokens = tokens
        self.output = ""
        self.current_token = ""
        self.current_position = -math.inf
        self.tagged_tokens = tagged
        self.current_tagged_token = ""
        self.token_dict = {
            key: val
            for key, val in enumerate(list(zip(self.tokens, self.tagged_tokens)))
        }
        self.out = ""        

    def advance(self):
        self.current_token = self.tokens[self.current_position]
        self.current_tagged_token = self.token_dict.pop(self.current_position)[1]
        self.current_position += 1
        print(f"Advancing to pos {self.current_position}, current: {self.current_token}")        
        return self.current_token, self.current_tagged_token

    def get_current_token_tags(self):
        start_tag, token, end_tag = self.current_tagged_token.split()
        return start_tag, token, end_tag

    def compile(self):
        self.current_position = 0
        self.current_token = self.tokens[self.current_position]
        assert (
            self.current_token == "class"
        ), f"program should begin with keyword class, got '{self.current_token}' instead."
        self.compileClass()
        print(self.out)

    def compileClass(self):
        """Compiles class where class has structure:
            'class' className '{' classVarDec* subroutineDec* '}'
        """
        self.advance()
        assert (
            self.current_token == "class"
        ), f"Wrong method 'compileClass' dispatched for {self.current_token}."

        self.out +=  "<class>\n"
        tags = self.get_current_token_tags()
        assert (
            tags[0] == "<keyword>"
        ), "Expected <keyword> tag for `class`, got {}".format(tags[0])
        assert (
            tags[2] == "</keyword>"
        ), "Expected </keyword> tag for `class`, got {}".format(tags[2])
        self.out += self.current_tagged_token

        self.advance()
        tags = self.get_current_token_tags()
        assert (
            tags[0] == "<identifier>"
        ), "Expected <identifier> tag for `class`, got {}".format(tags[0])
        assert (
            tags[2] == "</identifier>"
        ), "Expected <identifier> tag for `class`, got {}".format(tags[2])
        self.out += self.current_tagged_token
        self.advance()
        
        tags = self.get_current_token_tags()
        assert self.current_token == "{"
        assert (
            tags[0] == "<symbol>"
        ), "Expected <symbol> tag for left curly, got {}".format(tags[0])
        assert tags[1] == "{", "Expected <symbol> tag for left curly, got {}".format(
            tags[1]
        )
        assert (
            tags[2] == "</symbol>"
        ), "Expected </symbol> tag for right curly, got {}".format(tags[2])
        self.out += self.current_tagged_token

        self.compileClassVarDec()
        self.compileSubroutine()
        # End r bracket
        self.out += self.current_tagged_token
        self.out += "</class>\n"

    def compileClassVarDec(self):
        """Compiles class var declaration where declaration has strcture:
            ('static' | 'field' ) type varName (',' varName)* ';'
        """
        self.advance()
        # Loop
        while True:
            self.out += "<classVarDec >\n"
            tags = self.get_current_token_tags()
            assert self.current_token in [
                "static",
                "field",
            ], "Expected one of 'static', 'field' tag, got {}".format(
                self.current_token
            )
            assert tags[0] == "<keyword>", "Expected <keyword> tag, got {}".format(
                tags[0]
            )
            assert tags[1] in [
                "static",
                "field",
            ], "Expected one of 'static', 'field' tag, got {}".format(tags[1])
            assert tags[2] == "</keyword>", "Expected </keyword> tag, got {}".format(
                tags[2]
            )
            self.out += self.current_tagged_token
            # type
            self.advance()
            tags = self.get_current_token_tags()
            assert tags[0] == "<keyword>", "Expected <keyword> tag, got {}".format(
                tags[0]
            )
            assert tags[2] == "</keyword>", "Expected </keyword> tag, got {}".format(
                tags[2]
            )
            self.out += self.current_tagged_token
            self.advance()
            # compileVarName
            while True:
                if self.current_token == ";":
                    self.out += self.current_tagged_token
                    break
                self.out += self.current_tagged_token
                self.advance()
                if self.current_token == ",":
                    self.out += self.current_tagged_token
                    self.advance()
            self.advance()
            self.out += "</classVarDec>\n"
            if self.current_token not in ["static", "field"]:
                break
        # close

    def compileSubroutine(self):
        """Compiles a complete method, function, or constructor.
        Structure of subroutine:
            ('constructor' | 'function' | 'method')
            ('void' | type)
            subroutineName
            '('
            parameterList
            ')'
            subroutineBody
        """
        # declaration
        while True:
            if self.current_token == "}":
                break
            self.out += "<subroutineDec >\n"
            tags = self.get_current_token_tags()
            assert (
                tags[0] == "<keyword>"
            ), "Expected <keyword> tag for subroutineDec, got {}".format(tags[0])
            assert tags[1] in [
                "constructor",
                "method",
                "function",
            ], "Expected 'constructor', 'method', 'function', got {}".format(tags[1])
            self.out += self.current_tagged_token
            # type
            self.advance()
            self.out += self.current_tagged_token
            # name
            self.advance()
            self.out += self.current_tagged_token

            self.advance()
            assert self.current_token == "(", "Expected left paren"
            self.out += self.current_tagged_token
            self.advance()

            self.compileParameterList()
            self.out += self.current_tagged_token
            self.advance()

            self.compileSubRoutineBody()

            self.out += "</subroutineDec >\n"            

    def compileParameterList(self):
        """Compiles list of params.
        ( (type varName) (',' type varName)*)?
        """
        self.out += "<parameterList>\n"
        while self.current_token != ")":
            self.out += self.current_tagged_token
            self.advance()
        self.out += "</parameterList>\n"

    def compileSubRoutineBody(self):
        """ Compiles subroutine body.
        '{' varDec* statements '}'
        """
        self.out += "<subroutineBody>\n"
        self.out += self.current_tagged_token
        self.advance()
        if self.get_current_token_tags()[1] == "var":            
            while self.current_token != "}":
                self.compileVarDec()
                self.advance()
            if self.current_token == ";":
                self.out += self.current_tagged_token
                self.advance
        # statements
        self.compileStatements()        
        
        # rbracket
        self.out += self.current_tagged_token     
        #close
        self.out += "</subroutineBody>\n"
        

    def compileVarDec(self):
        """Compiles variable declaration.
        'var' type varName (',' varName)* ';'"""
        self.out += self.current_tagged_token
        self.advance()
        self.out += self.current_tagged_token
        self.advance()
        self.out += self.current_tagged_token
        self.advance()
        self.out += self.current_tagged_token
        self.advance()

    def compileStatements(self):
        """Compiles statements:
            letStatement | ifStatement | whileStatement | doStatement | returnStatement"""
        self.out += "<statements>\n"
        while True:
            if self.current_token not in ["if", "let", "do", "while"]:
                break
            if self.current_token == "if":
                self.compileIf()
            if self.current_token == "let":                
                self.compileLet()
            if self.current_token == "do":
                self.compileDo()
            if self.current_token == "while":
                self.compileWhile()
            if self.current_token == "return":
                self.compileReturn()
        self.out += "</statements>\n"
    
    def compileDo(self):
        """Compiles do instruction:
         'do' subroutineCall ';'"""
        self.out += "<doStatement>\n"
        self.out += self.current_tagged_token
        self.advance()

        self.compileSubroutineCall()
        self.out += "</doStatement>\n"


    def compileLet(self):
        """Compiles let instruction.
            'let' varName('[' expression ']')? '=' expression ';'
        """
        while self.current_token != ";":
            if self.current_token == ";":
                break
            self.out += "<letStatement>\n"
            # print let
            self.out += self.current_tagged_token            
            self.advance()
            # print varName
            self.out += self.current_tagged_token
            self.advance()
            # check opt expression
            if self.current_token == "[":
                self.out += self.current_tagged_token
                self.advance()                
                self.compileExpression() 
                self.out += self.current_tagged_token
                self.advance()
            # print '='
            self.out += self.current_tagged_token
            self.advance()
            # compile expression
            self.compileExpression()
        # semicolon
        self.out += self.current_tagged_token
        self.advance()
        self.out += "</letStatement>\n"

    def compileWhile(self):
        """Compiles while statement.
            'while' '(' expression ')' '{' statements '}'
        """
        self.out += "<whileStatement>\n"
        # print 'while'
        self.out += self.current_tagged_token
        self.advance()
        # print left paren
        self.out += self.current_tagged_token
        self.advance()

        self.compileExpression()
        
        # right paren
        self.out += self.current_tagged_token
        self.advance()
        # left bracket
        self.out += self.current_tagged_token
        self.advance()

        self.compileStatements()
        
        # right bracket
        self.out += self.current_tagged_token
        self.advance()

    def compileReturn(self):
        """Compiles return statement. 
            'return' expression? ';'"""
        self.out += "<returnStatement>\n"
        self.out += self.current_tagged_token
        self.advance()
        if self.get_current_token_tags()[0] == "<identifier>":
            self.compileExpression()
        # print semicolon
        self.out += self.current_tagged_token
        self.advance()
        # close tag
        self.out += "</returnStatement>\n"

    def compileIf(self):
        """Compiles if statement.
        if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?"""
        self.out += "<ifStatement>\n"
        assert self.get_current_token_tags(
        )[1] == "If", "If statment must begine with if"        
        self.out += self.current_tagged_token
        self.advance()
        assert self.get_current_token_tags(
        )[1] == "(", "If statment must be followed by left paren"
        self.out += self.current_tagged_token
        self.advance()
        self.compileExpression()
        self.out += self.current_tagged_token
        self.advance()
        
        self.out += self.current_tagged_token
        self.advance()
        self.compileStatements()
        print("Compiled staments form within if statement")
        
        if self.current_token == "else":
            self.out += self.current_tagged_token
            self.advance()
            self.out += self.current_tagged_token
            self.advance()
            self.compileStatements()
            self.out += self.current_tagged_token
            self.advance()
        else:
            self.out += self.current_tagged_token
            self.advance()


        self.out += self.current_tagged_token
        self.advance()
        
        print(f"Breaking out of if Statement at position: {self.current_position} with current token: {self.current_token}")
        self.out += "</ifStatement>\n"
        print(self.out)
        

    def compileExpression(self):
        """Compiles expression"""
        self.out += "<expression>\n"
        self.compileTerm()
        self.out += "</expression>\n"
        

    def compileTerm(self):
        """Compiles term"""
        self.out += "<term>\n"
        self.out += self.current_tagged_token
        self.out += "</term>\n"
        self.advance()

    def compileExpressionList(self):
        """Compiles list of expressions"""
        self.out += "<expressionList>\n"
        while self.current_token != ")":
            self.compileExpression()
        self.out += "</expressionList>\n"
        self.out += self.current_tagged_token
        self.advance()
    
    def compileSubroutineCall(self):
        """Compiles subroutine call
            subroutineName '(' expressionList ')' | ( className | varName) '.' subroutineName '(' expressionList ')'
        """
        print("SUBROUTINE CALL")        
        # print subroutine name
        self.out += self.current_tagged_token
        self.advance()
        # Either expression list
        if self.current_token == "(":
            # left paren
            self.out += self.current_tagged_token
            self.advance()
            # expression list
            self.compileExpressionList()
            # right paren
            self.out += self.current_tagged_token
            self.advance()
        # Or ( className | varName) '.' subroutineName '(' expressionList ')'
        else:
            # ( className | varName)
            self.out += self.current_tagged_token
            self.advance()
            # print '.'
            self.out += self.current_tagged_token
            self.advance()
            # print subroutineName
            self.out += self.current_tagged_token
            self.advance()
            # print '('
            self.out += self.current_tagged_token
            self.advance()
            # expressionList
            self.compileExpressionList()
            # print ')'
            self.out += self.current_tagged_token
            self.advance()
            
