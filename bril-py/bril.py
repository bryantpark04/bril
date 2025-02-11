from pydantic import BaseModel

from abc import ABC
from typing import Literal, NewType


Identifier = NewType("Identifier", str)

type PrimitiveType = Literal["int", "bool", "float", "char"]
type Type = PrimitiveType | Pointer

type ConstantValue = int | float | bool | str

type Operation = DataOperation | EmptyOperation | LabelOperation | FunctionCall | ReturnStatement | EffectOperation
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


class BaseEntity(StrictBaseModel):
    pos: Position | None = None


class BaseOperation(BaseEntity):
    op: str


class Label(BaseEntity):
    label: Identifier


# TODO somehow mark operations that may have side effects


class ArgumentedOperation(BaseOperation):
    args: list[Identifier]


class ValueOperation(BaseOperation):
    dest: Identifier
    type: Type


class Constant(ValueOperation):
    op: Literal["const"]
    value: ConstantValue


class DataOperation(ArgumentedOperation, ValueOperation):
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
    op: Literal["guard", "br", "jmp", "phi"]
    labels: list[Identifier]
    args: list[Identifier] | None = None    # for guard only
    type: Type | None = None    # for phi only
    dest: Identifier | None = None  # for phi only


class EffectOperation(ArgumentedOperation):
    op: Literal["free", "store", "print"]


class FunctionCall(BaseOperation):
    op: Literal["call"]
    args: list[Identifier] | None = None
    funcs: list[Identifier]
    dest: Identifier | None = None
    type: Type | None = None


class ReturnStatement(BaseOperation):
    op: Literal["ret"]
    args: list[Identifier] | None = None


class Function(BaseEntity):
    name: Identifier
    args: list[FunctionArgument] | None = None
    instrs: list[Label | Instruction]
    type: Type | None = None


class Program(StrictBaseModel):
    functions: list[Function]
