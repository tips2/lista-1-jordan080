import os

from backward_chaining import BackwardChaining
from forward_chaining import ForwardChaining
from mixed_chaining import MixedChaining

program = ""

while True:
    print("Encadeamento para frente, para trás ou misto? Insira uma das seguintes siglas:")
    print("EF - Encadeamento para frente")
    print("ET - Encadeamento para trás")
    print("EM - Encadeamento misto")
    program = input()
    if program == "EF" or program == "ET" or program == 'EM':
        break
    print("Opção incorreta.")

file_name = ""
while True:
    file_name = input("Nome do arquivo:\n")
    if os.path.isfile(file_name):
        break
    else:
        print("Arquivo não encontrado.")

if program == "EF":
    ForwardChaining(file_name)
if program == "ET":
    BackwardChaining(file_name)
if program == "EM":
    MixedChaining(file_name)