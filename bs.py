# Ghidra Script to define function types for all EfiBootServices functions of DxeCore
#
# Memo: Applying Function Data Types
#   1. Find the DataType of the function type you want to apply from DataTypeManager
#     - dtm.findDataTypes("EFI_RAISE_TPL", list)
#   2. cmd = ApplyFunctionSignatureCmd(funcAddr, funcDataType, USER_DEFINED)
#   3. runCommand(cmd)

from ghidra.app.cmd.function import ApplyFunctionSignatureCmd
from ghidra.program.model.symbol.SourceType import USER_DEFINED

addr = currentAddress # select RaiseTPL addr in BS
base = currentProgram.getImageBase()

dtm = currentProgram.getDataTypeManager()
l = []
dtm.findDataTypes("EFI_BOOT_SERVICES", l);
bs = l[0]

for i in range(44):
    funcTypeName = bs.getComponent(i+1).getDataType().getName()
    funcName = bs.getComponent(i+1).getFieldName()
    print(i, funcName)
    if funcName=="Reserved":
        addr = addr.add(8)
        continue
    l = []
    dtm.findDataTypes(funcTypeName, l)
    funcDataType = l[1]
    funcAddr = base.add(getInt(addr))
    print(" ", funcDataType, funcAddr)
    cmd = ApplyFunctionSignatureCmd(funcAddr, funcDataType, USER_DEFINED)
    runCommand(cmd)

    func = getFunctionAt(funcAddr)
    if func==None:
        func = createFunction(funcAddr, funcName)
    func.setName(funcName + "_" + funcAddr.toString()[-4:], USER_DEFINED)
    addr = addr.add(8)

