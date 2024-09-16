import pytest
import os

def test_ex0():
    compiler_output = os.popen("python3 ../Compiler/main.py ../Compiler/examples/ex0.aqua").read()
    assert compiler_output == open("./expected_results/ex0").read()

def test_ex1():
    compiler_output = os.popen("python3 ../Compiler/main.py ../Compiler/examples/ex1.aqua").read()
    assert compiler_output == open("./expected_results/ex1").read()

def test_ex2():
    compiler_output = os.popen("python3 ../Compiler/main.py ../Compiler/examples/ex2.aqua").read()
    assert compiler_output == open("./expected_results/ex2").read()

def test_ex3():
    compiler_output = os.popen("python3 ../Compiler/main.py ../Compiler/examples/ex3.aqua").read()
    assert compiler_output == open("./expected_results/ex3").read()

def test_ex4():
    compiler_output = os.popen("python3 ../Compiler/main.py ../Compiler/examples/ex4.aqua").read()
    assert compiler_output == open("./expected_results/ex4").read()
