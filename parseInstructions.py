import json
import sys
from typing import List

AvailableCommands = [
    "MoveJoints",
    "MoveLinRelWRF"
]

AvailableOptions = [
    "Note"
]

###########################################################################################################
class Instruction(): 
    name: str
    parameters: List[str]

    def __init__(self, jsobject):
        self.name = jsobject["name"]
        self.parameters = jsobject["parameters"]
        pass

    def __repr__(self) -> str:
        return f"Instruction(name: {self.name}, params: {self.parameters})"

    def execute(self):
        if self.name in AvailableCommands:
            print("Executing Meca Command")
        elif self.name in AvailableOptions:
            print("Doing special thing")
            pass
        else:
            print("INVALID COMMAND")


###########################################################################################################
class InstructionFile():
    filepath: str

    def __init__(self, fpath):
        self.filepath = fpath
        pass

    def print_dump(self):
        print("Reading file: ", self.filepath)
        with open(self.filepath, "r") as file:
            js = json.load(file)
        print(js)

    def getInstructions(self):
        with open(self.filepath, "r") as file:
            js = json.load(file)
        instrs = []
        for instr in js["instructions"]:
            instrs.append(Instruction(instr))
        return instrs


if __name__ == "__main__":
    test = InstructionFile("./components/soi/tape.json")
    test.print_dump()
    print(str(test.getInstructions()))
    