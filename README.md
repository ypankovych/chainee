# Chainee


[![Downloads](https://static.pepy.tech/personalized-badge/chainee?period=total&units=none&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/chainee)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/chainee.svg)](https://pypi.python.org/pypi/chainee/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/ypankovych/chainee/graphs/commit-activity)
[![MIT License](https://img.shields.io/pypi/l/chainee.svg)](https://opensource.org/licenses/MIT)
[![PyPi status](https://img.shields.io/pypi/status/chainee.svg)](https://pypi.python.org/pypi/chainee)
[![PyPI version fury.io](https://badge.fury.io/py/chainee.svg)](https://pypi.python.org/pypi/chainee/)
[![PyPI implementation](https://img.shields.io/pypi/implementation/chainee.svg)](https://pypi.python.org/pypi/chainee/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

### What is this?
> Chainee is a simple chaining tool for your predicates. 
> 
> Chain any number of predicates as deep as you want, and visualize it.

### Installation

`pip install chainee`

### Usage

Everything is based on `P` object (`from chainee import P`), you simply wrap your predicates with `P`
and start chaining it. E.g:

```python
from chainee import P

def validate_name_length(name):
    """Check that name has at least 4 characters"""
    return len(name) > 3

def validate_name_lower(name):
    """Make sure that name is in lower case"""
    return name.islower()

chain = P(validate_name_length) & P(validate_name_lower)
print(chain("yaroslav"))  # True
```

As you can see, it's very easy and readable.

You can achieve any nesting level, the following is possible:
```python
chain = ~((P(validate_name_length) & ~P(validate_name_lower)) | (P(validate_name_length) & P(validate_name_lower)))
```

You have a few operators you can use, `&` (and), `|` (or) and `~` (not).
Basically that's all Chainee gets you, which is quite enough.

### Visualizing

You can build a tree from your chain. Let's build a tree for the chain above:
```python
>>> print(chain)
InvertedUnion(union=UnionOr(lhs=UnionAnd(lhs=Predicate(func=<function validate_name_length at 0x10fa4f160>, description='Check that name has at least 4 characters'), rhs=InvertedPredicate(func=<function validate_name_lower at 0x10fbcb8b0>, description='Make sure that name is in lower case')), rhs=UnionAnd(lhs=Predicate(func=<function validate_name_length at 0x10fa4f160>, description='Check that name has at least 4 characters'), rhs=Predicate(func=<function validate_name_lower at 0x10fbcb8b0>, description='Make sure that name is in lower case'))))
# note that doc strings copied into description
```
Now, lets build an actual tree:
```python
>>> tree = chain.to_tree()
>>> print(tree)
NOT
└── OR
    ├── AND
    │   ├── Predicate(validate_name_lower)
    │   └── Predicate(validate_name_length)
    └── AND
        ├── NOT Predicate(validate_name_lower)
        └── Predicate(validate_name_length)
```
You can convert it into a picture as well:
```python
>>> tree.to_picture("tree.png")
```
Which gives us the following:
![tree](https://user-images.githubusercontent.com/31005942/123926790-eb3d9180-d994-11eb-8307-1c3a36103538.png)

