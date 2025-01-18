from ghidra.app.cmd.function import ApplyFunctionSignatureCmd
from ghidra.program.model.symbol.SourceType import USER_DEFINED
from ghidra.program.database.data import FunctionDefinitionDB

funcAddr = currentAddress # select function entry addr
funcTypeName = askString("Enter Function Type Name", "")

types = []
dtm = currentProgram.getDataTypeManager()
dtm.findDataTypes(funcTypeName, types)
funcDataType = None
for t in types:
    if type(t) == FunctionDefinitionDB:
        funcDataType = t

if funcDataType == None:
    print("DataType not found");
else:
    cmd = ApplyFunctionSignatureCmd(funcAddr, funcDataType, USER_DEFINED)
    runCommand(cmd)
    print("Function DataType applied successfully!");

