from pydantic import BaseModel
from typing import Literal, NewType


Identifier = NewType("Identifier", str)

type PrimitiveType = Literal["int", "bool", "float", "char"]
type Type = PrimitiveType | Pointer

type ConstantValue = int | float | bool | str

type Operation = ArgumentedValueOperation | ArgumentedOperation | EmptyOperation | LabelOperation | FunctionCall | Return | EffectOperation | PhiOperation
type Instruction = Constant | Operation


class StrictBaseModel(BaseModel):
    model_config = { "extra": "forbid" }


class Position(StrictBaseModel):
    row: int
    col: int


class Pointer(StrictBaseModel):
    ptr: Type


class FunctionArgument(StrictBaseModel):
    name: Identifier
    type: Type


class Label(StrictBaseModel):
    label: Identifier
    pos: Position | None = None


class Constant(StrictBaseModel):
    op: Literal["const"]
    value: ConstantValue
    dest: Identifier
    type: Type
    pos: Position | None = None


class BaseOperation(StrictBaseModel):
    pos: Position | None = None

# TODO somehow mark operations that may have side effects
# TODO somehow classify operations better

class ArgumentedOperation(BaseOperation):
    args: list[Identifier]


class ValueOperation(BaseOperation):
    dest: Identifier
    type: Type


class ArgumentedValueOperation(ArgumentedOperation, ValueOperation):
    op: Literal[ 
        "id", 
        "add", "mul", "sub", "div",
        "fadd", "fmul", "fsub", "fdiv",
        "eq", "lt", "gt", "ge", "le", 
        "feq", "flt", "fgt", "fge", "fle", 
        "ceq", "clt", "cgt", "cge", "cle", 
        "not", "and", "or",
        "load", "ptradd", "alloc",
        "char2int", "int2char"
    ]


class EmptyOperation(BaseOperation):
    op: Literal["nop", "speculate", "commit"]


class LabelOperation(BaseOperation):
    op: Literal["guard", "br", "jmp"]
    labels: list[Identifier]
    args: list[Identifier] | None = None    # for guard only


class PhiOperation(BaseOperation):
    op: Literal["phi"]
    labels: list[Identifier]
    args: list[Identifier]
    type: Type
    dest: Identifier


class EffectOperation(ArgumentedOperation):
    op: Literal["free", "store", "print"]


class FunctionCall(BaseOperation):
    op: Literal["call"]
    args: list[Identifier] | None = None
    funcs: list[Identifier]
    dest: Identifier | None = None
    type: Type | None = None


class Return(BaseOperation):
    op: Literal["ret"]
    args: list[Identifier] | None = None


class Function(StrictBaseModel):
    name: Identifier
    args: list[FunctionArgument] | None = None
    instrs: list[Label | Instruction]
    type: Type | None = None
    pos: Position | None = None


class Program(StrictBaseModel):
    functions: list[Function]
