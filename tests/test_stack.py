from pytest import raises
from stack.Stack import Stack
def test_size():
    stack = Stack()
    assert stack.size() == 0
    stack.push(1)
    assert stack.size() == 1
    stack.peek()
    assert stack.size() == 1
    stack.pop()
    assert stack.size() == 0
    
def test_empty():
    stack = Stack()
    assert stack.empty() == True
    stack.push(1)
    assert stack.empty() == False
    stack.pop()
    assert stack.empty() == True

def test_push_none():
    stack = Stack()
    with raises(Exception):
        stack.push(None)

def test_pop_from_empty_stack():
    stack = Stack()
    with raises(Exception):
        stack.pop()

def test_peek_from_empty_stack():
    stack = Stack()
    with raises(Exception):
        stack.peek()

def test__str__():
    stack = Stack()
    assert str(stack) == ""
    stack.push(1)
    assert str(stack) == "1"
    stack.push(2)
    assert str(stack) == "2->1"
    stack.pop()
    assert str(stack) == "1"
    stack.pop()
    assert str(stack) == ""