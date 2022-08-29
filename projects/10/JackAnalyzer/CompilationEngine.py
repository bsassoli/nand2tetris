""" Compiles a list of tokens to XML
"""

from typing import List


class Compiler:
    """Compiler: Class producing the compiled program
    """

    def __init__(self, tokens: List[str], tagged: List[str], types):
        """__init__ Initializes a Compiler class

        Args:
            tokens (List[str]): A list of tokens
            tagged (List[str]): A list of tagged tokens in the format: <tag> token </tag>
            types (_type_): _description_
        """
        self.tokens = tokens
        self.current_token = ""
        self.current_position = 0
        self.tagged_tokens = tagged
        self.current_tagged_token = ""
        self.token_dict = dict(enumerate(list(zip(self.tokens, self.tagged_tokens))))
        self.out = ""
        self.token_types = types

    def advance(self):
        """Advance: consumes a toekn and advances one step
        """
        self.current_token = self.tokens[self.current_position]
        self.current_tagged_token = self.token_dict.pop(self.current_position)[1]
        self.current_position += 1
        return self.current_token, self.current_tagged_token

    def output_token(self):
        """Outputs current tagged token and advances to next token"""
        self.out += self.current_tagged_token
        self.advance()

    def get_current_token_type(self):
        """Returns the type of the current token"""
        return self.get_current_token_tags()[1:-1]

    def get_current_token_tags(self):
        """Returns the opening tag of the current token"""
        return self.current_tagged_token.split()[0]

    def compile(self):
        """Starts the compilation process"""
        self.output_token()
        self.compileClass()

    def compileClass(self):
        """Compiles class where class has structure:
            'class' className '{' classVarDec* subroutineDec* '}'
        """
        self.out += "<class>\n"  # write <class> tag
        self.output_token()  # write keyword class
        self.output_token()  # write className
        self.output_token()  # write l bracket
        self.compileClassVarDec()  # compileClassVarDec
        self.compileSubRoutine()  # write subroutineDec*
        self.out += self.current_tagged_token  # write r bracket
        self.out += "</class>\n"  # write closing <class> tag

    def compileClassVarDec(self):
        """Compiles class var declaration where declaration has structure:
            ('static' | 'field' ) type varName (',' varName)* ';'
        """
        while self.current_token in ["static", "field"]:
            self.out += "<classVarDec >\n"
            self.output_token()  # write static | field
            self.output_token()  # output type
            self.output_token()  # output varname
            # optional other vars
            while True:
                if self.current_token == ";":
                    break
                self.output_token()  # output varname
            self.output_token()  # ending semicolon
            self.out += "</classVarDec >\n"  # closing <classVarDec> tag

    def compileSubRoutine(self):
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
        while self.current_token in ["constructor", "function", "method"]:
            self.out += "<subroutineDec >\n"
            self.output_token()  # constructor | method | function
            self.output_token()  # void | type
            self.output_token()  # subroutineName
            self.output_token()  # l paren
            self.compileParameterList()
            self.output_token()  # r paren
            # subroutineBody
            # '{' varDec* statements '}'
            self.out += "<subroutineBody>\n"
            self.output_token()  # l bracket
            self.compileVarDec()
            self.compileStatements()
            self.output_token()  # r bracket
            self.out += "</subroutineBody>\n"
            self.out += "</subroutineDec >\n"

    def compileParameterList(self):
        """Compiles list of params.
        ( (type varName) (',' type varName)*)?
        """
        self.out += "<parameterList>\n"
        while self.current_token != ")":
            self.output_token()
        self.out += "</parameterList>\n"

    def compileVarDec(self):
        """Compiles variable declaration.
            'var' type varName (',' varName)* ';'"""
        while True:
            if self.current_token != "var":
                break
            self.out += "<varDec>\n"
            self.output_token()  # var
            self.output_token()  # type
            self.output_token()  # varName
            while True:
                if self.current_token != ",":
                    break
                self.output_token()
                self.output_token()
            self.output_token()
            self.out += "</varDec>\n"

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

    def compileIf(self):
        """Compiles if statement. Structure:
            if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?"""
        self.out += "<ifStatement>\n"
        self.output_token()  # if
        self.output_token()  # (
        self.compileExpression()
        self.output_token()  # )
        self.output_token()  # {
        self.compileStatements()
        self.output_token()  # }
        if self.current_token == "else":
            self.output_token()  # else
            self.output_token()  # {
            self.compileStatements()
            self.output_token()  # }
        self.out += "</ifStatement>\n"

    def compileLet(self):
        """Compiles let instruction.
            'let' varName('[' expression ']')? '=' expression ';'
        """
        self.out += "<letStatement>\n"
        self.output_token()  # let
        self.output_token()  # varName
        if self.current_token == "[":
            self.output_token()  # opt Array [
            self.compileExpression()  # expression
            self.output_token()  # opt end Array ]
        self.output_token()  # opt Array [
        self.compileExpression()
        self.output_token()  # ;
        self.out += "</letStatement>\n"

    def compileDo(self):
        """Compiles do instruction:
         'do' subroutineCall ';'"""
        self.out += "<doStatement>\n"
        self.output_token()  # do
        self.compileSubroutineCall()  # subroutine call TO IMPLEMENT
        self.output_token()  # ;
        self.out += "</doStatement>\n"

    def compileSubroutineCall(self):
        """Compiles subroutine call
            subroutineName '(' expressionList ')'
            | ( className | varName)
            '.'
            subroutineName '(' expressionList ')'
        """

        # print subroutine name
        self.output_token()
        # Either expression list
        if self.current_token == "(":

            self.output_token()  # left paren
            self.compileExpressionList()  # expressionList
            self.output_token()  # right paren
        # Or ( className | varName) '.' subroutineName '(' expressionList ')'
        else:
            self.output_token()  # print '.'
            self.output_token()  # print subroutineName
            self.output_token()  # print '('
            self.compileExpressionList()  # expressionList
            self.output_token()  # print ')'

    def compileWhile(self):
        """Compiles while statement.
            'while' '(' expression ')' '{' statements '}'
        """
        self.out += "<whileStatement>\n"
        self.output_token()  # while
        self.output_token()  # l paren
        self.compileExpression()
        self.output_token()  # r paren
        self.output_token()  # l curly
        self.compileStatements()
        self.output_token()  # r curly
        self.out += "</whileStatement>\n"

    def compileReturn(self):
        """Compiles return statement. 
            'return' expression? ';'"""
        self.out += "<returnStatement>\n"
        self.output_token()  # return
        if self.current_token != ";":
            self.compileExpression()
        self.output_token()  # semicolon
        self.out += "</returnStatement>\n"

    def compileExpression(self):
        """compileExpression compiles an expression of form:
            term (op term)*
        """
        self.out += "<expression>\n"
        self.compileTerm()
        while self.current_token in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            self.output_token()
            self.compileTerm()
        self.out += "</expression>\n"

    def compileTerm(self):
        """compileTerm Compiles a term
            IntegerConstant | 
            stringConstant |
            keywordConstant |
            varName |
            varName '[' expression ']' |
            subroutineCall |
            '(' expression ')' |
            unaryOp term
        """
        self.out += "<term>\n"
        lookahead = self.tokens[self.current_position]
        if self.current_token in ["-", "~"]:
            self.output_token()  # write
            self.compileTerm()  # write

        elif self.get_current_token_type() in [
            "integerConstant",
            "stringConstant",
            "true",
            "false",
            "null",
            "this",
        ]:
            self.output_token()  # write

        elif self.current_token == "(":
            self.output_token()  # write (
            self.compileExpression()  # compile expression
            self.output_token()  # write )
            # careful could go in infinite loop?

        elif lookahead == "[":  # array
            self.output_token()  # write varNmae
            self.output_token()  # write [
            self.compileExpression()  # compile expression
            self.output_token()  # write ]

        elif lookahead in [".", "("]:
            self.compileSubroutineCall()

        else:
            self.output_token()
        self.out += "</term>\n"

    def compileExpressionList(self):
        """Compiles list of expressions.
            (expression (',' expression)* )?"""
        self.out += "<expressionList>\n"
        while self.current_token != ")":
            if self.current_token == ",":
                self.output_token()
            self.compileExpression()
        self.out += "</expressionList>\n"
