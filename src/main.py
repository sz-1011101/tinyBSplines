
import Interpreter as inp

def __main__():
    interpreter = inp.Interpreter()

    print("#####\n###\n#####\n### B-Splines Script\n#####\n###\n#####")
    command_counter = 0
    while interpreter.interpret():
        command_counter += 1


if __name__ == "__main__":
    __main__()

