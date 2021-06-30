from __future__ import annotations

import typing
from dataclasses import dataclass, field

from anytree import Node, RenderTree
from anytree.exporter import DotExporter


class _NodeNameUnifier:

    def __init__(self):
        self._nodes = []

    def __call__(self, node: Node):
        if node not in self._nodes:
            node.name = f"{node.name}-{len(self._nodes)}"
            self._nodes.append(node)
        return node.name


@dataclass(frozen=True)
class ChainTree:
    tree: str
    root_node: Node

    def to_picture(self, path):
        DotExporter(self.root_node, nodenamefunc=_NodeNameUnifier()).to_picture(path)

    def __repr__(self):
        return self.tree


@dataclass
class BasePredicate:
    func: typing.Callable
    description: str = field(init=False)

    def __post_init__(self):
        self.description = self.func.__doc__

    def __or__(self, other):
        return UnionOr(self, other)

    def __and__(self, other):
        return UnionAnd(self, other)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def _to_tree(self, root):
        return Node(f"{type(self).__name__}({self.func.__name__})", parent=root)


class InvertedPredicate(BasePredicate):

    def __invert__(self):
        return Predicate(self.func)

    def __call__(self, *args, **kwargs):
        return not super(InvertedPredicate, self).__call__(*args, **kwargs)


class Predicate(BasePredicate):
    def __invert__(self):
        return InvertedPredicate(self.func)


P = Predicate


class BaseUnion:
    def __or__(self, other):
        return UnionOr(self, other)

    def __and__(self, other):
        return UnionAnd(self, other)

    def __invert__(self):
        return InvertedUnion(self)

    def __call__(self, *args, **kwargs):
        pass

    def to_tree(self):
        root_node = self._to_tree()
        rendered = RenderTree(root_node)
        return ChainTree(
            "\n".join(
                "%s%s" % (pre, node.name)
                for pre, fill, node in rendered
            ),
            root_node
        )

    def _to_tree(self, parent=None):
        pass


@dataclass(frozen=True)
class Union(BaseUnion):
    lhs: typing.Union[BasePredicate, BaseUnion]
    rhs: typing.Union[BasePredicate, BaseUnion]

    def _to_tree(self, parent=None):
        root = Node(type(self).__name__, parent=parent)
        self.rhs._to_tree(root)
        self.lhs._to_tree(root)
        return root


@dataclass(frozen=True)
class InvertedUnion(BaseUnion):
    union: BaseUnion

    def __invert__(self):
        return self.union

    def __call__(self, *args, **kwargs):
        return not self.union(*args, **kwargs)

    def _to_tree(self, parent=None):
        root = Node(type(self).__name__, parent=parent)
        self.union._to_tree(root)
        return root


class UnionAnd(Union):

    def __call__(self, *args, **kwargs):
        return self.lhs(*args, **kwargs) and self.rhs(*args, **kwargs)

    def __or__(self, other):
        return UnionOr(self, other)


class UnionOr(Union):

    def __call__(self, *args, **kwargs):
        return self.lhs(*args, **kwargs) or self.rhs(*args, **kwargs)

    def __and__(self, other):
        return UnionAnd(self, other)
