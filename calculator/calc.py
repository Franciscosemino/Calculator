from __future__ import division
import math
import re
import operator

"""
Clase Calculator es la clase base de la calculadora, con dos metodos muy
importantes. El primero es to_rpn lo cual su funcion es recibir un input
de operaciones matematicas y convertirlo en RPN(Notacion polaca inversa,
https://es.wikipedia.org/wiki/Notaci%C3%B3n_polaca_inversa). En base es el
algoritmo de shutting yard de Edsger Dijkstra
(https://es.wikipedia.org/wiki/Algoritmo_shunting_yard) con una modificacion
para aceptar los numeros negativos con la salvedad que se aceptan entre
parentesis.

Luego tenemos el metodo calculate que es el encargado de procesar la operacion
matematica ya convertida en RPN a el resultado.

El metodo is_int solamente es un metodo auxiliar para poder saber si un token
es un numero de una forma sencilla.

el metodo precedencia_check es un metodo para ver la precendecia del ultimo
operador en el stack y compararlo con el token actual para saber que hacer con
ese token. es un metodo aparte ya que se utiliza dos veces en el metodo to_rpn
por la modificacion para aceptar los numeros negativos
"""
class Calculator(object):

    def __init__(self, command):
        self.expression = command
        self.operators = {'*' : operator.mul, '/' : operator.div,
         '+' : operator.add,'-' : operator.sub}
        self.precedencia = {'*' : 2, '/' : 2, '+' : 1, '-': 1}
        self.items = ['(', ')', 'log']
        self.tail = []
        self.stack = []
        self.calculate_stack = []

    def to_rpn(self):
        tokens = re.findall(r'[+-/*//()]|\d+|[log]+',self.expression)
        tokenbefore = ''
        negative = False
        for token in tokens:
            if self.is_int(token):
                if negative:
                    number = float('-' + token)
                    self.tail.append(number)
                    negative = False
                else:
                    number = float(token)
                    self.tail.append(number)
            elif token == '-':
                if tokenbefore in self.items or tokenbefore in self.operators:
                    negative = True
                else:
                    self.precedencia_check(token)
            elif token in self.operators:
                self.precedencia_check(token)
            elif token == "(":
                self.stack.append(token)
            elif token == ")":
                findpair = True
                while findpair:
                    epopfromstack = self.stack.pop()
                    if epopfromstack != "(":
                        self.tail.append(epopfromstack)
                    else:
                        findpair = False
            elif token == "log":
                self.stack.append(token)
            tokenbefore = token
        while len(self.stack)!=0:
            self.tail.append(self.stack.pop())
        return self.tail

    def calculate(self):
        for elem in self.tail:
            if self.is_int(elem):
                self.calculate_stack.append(elem)
            elif elem in self.operators:
                num0 = self.calculate_stack.pop()
                num1 = self.calculate_stack.pop()
                oper = self.operators[elem]
                result = oper(num1,num0)
                self.calculate_stack.append(result)
            elif elem == "log":
                num = self.calculate_stack.pop()
                result = math.log(num,10)
                self.calculate_stack.append(result)
        return self.calculate_stack[0]

    def is_int(self,s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def precedencia_check(self,token):
        if not self.stack or self.stack[len(self.stack)-1] in self.items:
            self.stack.append(token)
        else:
            if self.precedencia[token] <= self.precedencia[self.stack[len(self.stack)-1]]:
                self.tail.append(self.stack.pop())
                self.stack.append(token)
            else:
                self.stack.append(token)
