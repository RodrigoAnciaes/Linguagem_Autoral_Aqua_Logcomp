"""
Module: teste
Description: This module provides a function to test the execution of the main.py script
             with different arguments and handle any errors that occur.
"""

import subprocess

def test_main(args):
    """
    Executes the main.py script with the provided arguments and checks for errors.

    Args:
        args (list): A list of arguments to pass to main.py.

    Returns:
        None
    """
    try:
        # Execute main.py with the provided arguments
        with subprocess.Popen(['python', 'main.py'] + args, stderr=subprocess.PIPE) as process:
            _, stderr = process.communicate()

            # Check for errors in stderr
            if stderr:
                print(f"Erro ao executar main.py com os argumentos {args}:")
                print(stderr.decode())
            else:
                print(f"main.py executado com sucesso com os argumentos {args}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao chamar o processo: {str(e)}")
    except OSError as e:
        print(f"Erro no sistema operacional: {str(e)}")


# Teste com diferentes argumentos
test_main(['ex0.aqua'])
