from typing import List

class Compiler:
    """Compiler: Class producing the compiled program
    """

    def __init__(self, tokens: List[str], tagged: List[str], output: str):
        """__init__ _summary_

        Args:
            tokens (List[str]): a list of tokens
            tagged (List[str]): the tagged tokens

        """
        self.tokens = tokens
        self.current_token = ""
        self.current_position = 0
        self.tagged_tokens = tagged
        self.current_tagged_token = ""
        self.token_dict = {
            key: val
            for key, val in enumerate(list(zip(self.tokens, self.tagged_tokens)))
        }
        self.out = ""

    def advance(self):
        """advance: consumes a toekn and advances one step

        Returns:
            _type_: _description_
        """
        self.current_token = self.tokens[self.current_position]
        self.current_tagged_token = self.token_dict.pop(
            self.current_position)[1]
        self.current_position += 1

        print(
            f"Advancing to pos {self.current_position}, current: {self.current_token}"
        )
        return self.current_token, self.current_tagged_token

    def output_token(self):
        self.out += self.current_tagged_token
        self.advance()


    def get_current_token_tags(self):
        start_tag, token, end_tag = self.current_tagged_token.split()
        return start_tag, token, end_tag

    def compile(self):
        self.output_token()
        self.compileClass()
    
    def compileClass(self):
        """Compiles class where class has structure:
            'class' className '{' classVarDec* subroutineDec* '}'
        """
        # write <class> tag
        self.out += "<class>\n"
        # write keyword class
        
        assert self.current_token == "class", "Class declaration must begin with <class>, got {} instead".format(self.current_token)
        print("Printing keyword 'class': " + self.current_token)
        self.output_token()
        # write className
        print("Printing className: " + self.current_token)
        self.output_token()
        # write l bracket
        print("Printing lbracket: " + self.current_token)
        self.output_token()
        # compileClassVarDec
        self.compileClassVarDec()
        # write subroutineDec*
        self.compileSubRoutine()
        # write r bracket
        # TODO
        self.out += self.current_tagged_token
        # write closing <class> tag
        self.out += "</class>\n"
        print(self.out)
    
    def compileClassVarDec(self):
        """Compiles class var declaration where declaration has structure:
            ('static' | 'field' ) type varName (',' varName)* ';'
        """
        while self.current_token in ["static", "field"]:
            self.out += "<classVarDec >\n"
            # write static | field
            assert self.current_token in ["static", "field"], f"Ecprected on of 'static', 'field', got {self.current_token} instead."
            self.output_token()
            # output type
            self.output_token()
            # output varname
            self.output_token()
            # optional other vars
            while True:
                if self.current_token == ";":
                    break
                else:
                    # output varname
                    self.output_token()
            # ending semicolon
            self.output_token()
            # closing <classVarDec> tag        
            print(self.current_token)
            self.out += "</classVarDec >\n"
    
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
            print("Hey, I am in a subroutine delcaration!")
            self.out += "<subroutineDec >\n"
            self.output_token() # constructor | method | function
            self.output_token() # void | type
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
            self.output_token() # type
            self.output_token() # varName
            if self.current_token != ",":
                break
            self.output_token()
            self.out += "</varDec>\n"
    def compileStatements(self):
        """Compiles statements:
            letStatement | ifStatement | whileStatement | doStatement | returnStatement"""
        self.out += "<statements>\n"
        print("In compile")
        print(self.current_token)
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
        """Compiles if statement.
        if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?"""
        self.out += "<ifStatement>\n"
        self.output_token() # if
        self.output_token()  # (
        self.compileExpression()
        self.output_token()  # )
        self.output_token()  # {
        self.compileStatements()
        if self.current_token == "else":
            self.output_token() # {
            self.compileStatements()
        
        self.output_token()  # }
        self.out += "</ifStatement>\n"
    def compileLet(self):
        """Compiles let instruction.
            'let' varName('[' expression ']')? '=' expression ';'
        """
        self.out += "<letStatement>\n"
        self.output_token() # let
        self.output_token()  # varName
        self.output_token()  # opt Array [
        self.compileExpression() # expression
        self.output_token()  # opt end Array ]
        self.out += "</letStatement>\n"

    def compileDo(self):
        """Compiles do instruction:
         'do' subroutineCall ';'"""
        self.out += "<doStatement>\n"
        self.output_token() # do
        self.compileSubroutineCall()  # subroutine call TO IMPLEMENT        
        self.output_token()  # ;
        self.out += "</doStatement>\n"
    
    def compileSubroutineCall(self):
        """Compiles subroutine call
            subroutineName '(' expressionList ')' | ( className | varName) '.' subroutineName '(' expressionList ')'
        """
        
        # print subroutine name
        print("Output suborutine name")
        self.output_token()
        # Either expression list
        if self.current_token == "(":
            # left paren
            self.output_token()
            print("Just output lparen " + self.current_token)
            print("Calling compiling Expressrion LIST")
            self.compileExpressionList()
            # right paren
            self.output_token()
        # Or ( className | varName) '.' subroutineName '(' expressionList ')'
        else:
            # print '.'
            self.output_token()
            # print subroutineName
            self.output_token()
            # print '('
            self.output_token()
            # expressionList
            print("Calling compiling Expressrion LIST")
            self.compileExpressionList()
            # print ')'
            self.output_token()

    def compileWhile(self):
        self.output_token()

    def compileReturn(self):
        """Compiles return statement. 
            'return' expression? ';'"""
        self.out += "<returnStatement>\n"
        self.output_token() # return
        if self.get_current_token_tags()[0] == "<identifier>":
            self.compileExpression()
        self.output_token()  # semicolon
        self.out += "</returnStatement>\n"

    def compileExpression(self):
        """compileExpression compiles an expression of form:
            term (op term)*
        """
        # TODO
        # EXTEND TO COMPLEX EXPRESSIONS
        self.out += "<expression>\n"
        self.compileTerm()
        self.out += "</expression>\n"

    def compileTerm(self):
        """compileTerm _summary_
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
        
        if self.current_token == "(":         
            self.output_token()  # write (
            self.compileExpression()  # compile expression
            self.output_token()  # write )
            # careful could go in infinite loop?
        else:
            self.output_token()
            # [ expression ]
            if self.current_token == "[":
                self.output_token() # write [
                self.compileExpression()   # compile expression
                self.output_token() # write ]
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

