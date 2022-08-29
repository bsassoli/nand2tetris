"""
For each source Xxx.jack file:
    1. Create a tokenizer from the Xxx.jack file
    2. Open an Xxx.xml file and prepare it for writing
    3. Compile(INPUT: tokenizer, OUTPUT: output file)
Where output file refers to the Xxx.xml file.
"""
import sys
import os
from JackTokenizer import Tokenizer
from CompilationEngine import Compiler


def tokenize_file(file):
    """Given file name writes tokenized program as .xml"""
    tokenizer = Tokenizer(file)
    tokenizer.open()
    tokenizer.preprocess()
    tokenizer.tokenize()
    while tokenizer.has_more_tokens():
        tokenizer.advance()
    tokenizer.write()
    return tokenizer.tokens, tokenizer.tagged_tokens, tokenizer.token_types


def compile_file(tokens, tagged, types, output):
    """
    ***TODO***
    """
    compiler = Compiler(tokens, tagged, types, output)
    compiler.compile()
    with open(output, "w") as file:
        file.write(compiler.out)


def main():
    """Accepts dir or filename. Outputs tokenized files"""
    is_dir = False
    try:
        path = sys.argv[1]
    except IndexError:
        print("You must provide an argument")
    if os.path.isdir(path):
        is_dir = True
    if is_dir:
        files = [file for file in os.listdir(path) if file.split(".")[1] == "jack"]
    else:
        file_path = os.path.basename(path)
        if file_path.split(".")[1] == "jack":
            files = [file_path]
        else:
            print("Wrong filetype: must provide a .jack file")
            return
    if not is_dir:
        os.chdir(os.path.join(os.path.dirname(path)))
    for file in files:
        print(f"Tokenizing: {file}")
        assert file.split(".")[1] == "jack", "Wrong filetype: must provide a .jack file"
        if is_dir:
            file = os.path.join(path, file)
        tokenized, tagged, types = tokenize_file(file)
        if is_dir:
            out_file = os.path.join(file.split(".")[0] + ".xml")
        else:
            out_file = file.split(".")[0] + ".xml"
        compile_file(tokenized, tagged, types, out_file)


if __name__ == "__main__":
    main()
