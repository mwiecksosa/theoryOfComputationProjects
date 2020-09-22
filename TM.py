#!/usr/bin/python2

"""
CISC 4090 (Theory of Computation)
Spring, 2020

Project 2: A Turing Machine Emulator

This file describes a class TM that implements a Turing machine

The program does no error-checking on the input file. 

Author: Michael Wieck-Sosa
Date:   March 18, 2020"""

import sys

class Table_entry:
    """one-parameter constructor, reads table entry to transition function
    from input file stream raw_string"""
    def __init__(self, raw_string):
        ### split on comma
        self.data = raw_string.split(',')

        ### set the transition state
        self.new_state = int(self.data[0][1:])

        ### set the transition character
        self.new_char = self.data[1]

        ### set the transition direction
        self.direction = self.data[2][0]
        
    """string representation of Table_entry object"""
    def __str__(self):
        return('('+'{:3d}'.format(self.new_state)+','+
                   '{:1s}'.format(self.new_char)+','+
                   '{:1s}'.format(self.direction)+')')

class TM:
    """one-parameter constructor, reads Turing Machine data from input file stream ifs"""
    def __init__(self, ifs):
        ### snarf the data file, split on while space 
        self.data = ifs.read().split() 

        ### determine number of states 
        self.__num_states = self.data[0]

        ### determine input alphabet
        self.__sigma = self.data[1] 

        ### determine tape alphabet 
        self.__gamma = self.data[2] 

        ### determine blank symbol
        self.__blank = self.data[2][2]

        ### determine initial state
        self.__init_state = 1

        ### determine accept states, list because possibly many
        self.__acc_states = [0]

        ### determine reject states, list because possibly many
        self.__rej_states = [-1]

        ### determine transition function with code below and the helper member function
        self.__delta = []
        state_table = []
        dir_set = set()

        ### loop through raw state transitions 
        for transition in self.data[3:]:
            state_table.append(Table_entry(transition))
            dir_set.add(transition[-2])

        ### determine directions 
        self.__directions = list(dir_set)

        ### add states to self.__delta transition function
        for i in range(1,int(self.__num_states)+1):
            temp_list = []
            for entry in state_table[3*(i-1):3+3*(i-1)]:
                temp_list.append(entry)
            ### self.__delta is a list of 3 lists with 3 table entries each
            self.__delta.append(temp_list)
            
    """prints description of the Turing Machine"""
    def describe(self):
        ### print out the description
        print "sigma = {}".format(self.__sigma)
        print "gamma = {}".format(self.__gamma)
        print "blank = {}".format(self.__blank)
        print "number of states = {}".format(self.__num_states)
        print ### new line
        print "state transition table:"
        print ### new line
        print 8*' '+'{:1s}'.format(self.__gamma[0]),
        print 8*' '+'{:1s}'.format(self.__gamma[1]),
        print 8*' '+'{:1s}'.format(self.__gamma[2])

        ### loop through the number of states
        for i in range(int(self.__num_states)):
            print str(i+1)+":",
            ### loop through the number of possible input symbols
            for j in range(len(self.__delta[0])):
                print self.__delta[i][j], 
            print ### new line

    """utility function to print a given configuration of the Turing Machine"""
    def print_config(self, state, pos, in_string):
        for i in range(len(in_string)):
            ### if at this position in the string print below
            if i == pos:
                print "q"+str(state)+" "+in_string[i],
            ### if not at this position just print symbol
            elif i != pos:
                print in_string[i],
        ### if at last position in the string print below
        if pos == len(in_string):
            print "q"+str(state),

        print ### new line

    """trace the operation of the Turing Machine on an input string"""
    def trace(self, in_string): 
        ### if in_string contains any element other than 0, then reject
        for element in in_string:
            if element is not self.__sigma:
                print("illegal input char '{:1s}'!".format(element))
                return False

        ### add blank symbol to the end of the string 
        in_string += self.__blank
        ### set initial state to q1
        curr_state = self.__init_state
        ### beginning position in the input string
        pos = 0
        ### beginning symbol in input string
        curr_symbol = in_string[pos] 
        
        while True:
            ### print string representing the current state of the Turing Machine
            self.print_config(state=curr_state, pos=pos, in_string=in_string)

            new_string = ""

            if curr_symbol == self.__gamma[0]:
                ### get the table entry from the transition function
                transition = self.__delta[curr_state - 1][0]
                curr_state = transition.new_state
                ### transition the Turing Machine
                for i in range(len(in_string)):
                    ### add the rest of the string not changed
                    if i != pos:
                        new_string += in_string[i]
                    ### add the changed character to string
                    elif i == pos:
                        new_string += transition.new_char
                in_string = new_string

            if curr_symbol == self.__gamma[1]:
                ### get the table entry from the transition function 
                transition = self.__delta[curr_state - 1][1]
                curr_state = transition.new_state
                ### transition the Turing Machine
                for i in range(len(in_string)):
                    ### add the rest of the string not changed
                    if i != pos:
                        new_string += in_string[i]
                    ### add the changed character to string
                    elif i == pos:
                        new_string += transition.new_char
                in_string = new_string

            if curr_symbol == self.__gamma[2]:
                ### get the table entry from the transition function 
                transition = self.__delta[curr_state - 1][2]
                curr_state = transition.new_state
                ### transition the Turing Machine
                for i in range(len(in_string)):
                    if i != pos:
                        new_string += in_string[i]
                    elif i == pos:
                        new_string += transition.new_char
                in_string = new_string
            
            ### if direction is left 
            if transition.direction == self.__directions[1]:
                try:
                    ### if not at beginning of string increment pos down by 1
                    if pos > 0:
                        pos -= 1
                        curr_symbol = in_string[pos]
                    ### if at beginning of string do not increment down
                    elif pos == 0:
                        curr_symbol = in_string[pos]
                except IndexError as err:
                    print("IndexError: {0}".format(err))
                    
            ### if direction is right    
            elif transition.direction == self.__directions[0]:
                try:
                    ### if not at end of string increment pos up by 1
                    if pos < len(in_string) - 1:
                        pos += 1
                        curr_symbol = in_string[pos]
                    ### if at end of string do not increment up 
                    elif pos == len(in_string):
                        curr_symbol = in_string[pos]
                except IndexError as err:
                    print("IndexError: {0}".format(err))
            
            ### if current state in list of accepting states, then accept 
            if curr_state in self.__acc_states:
                self.print_config(state=curr_state, pos=pos, in_string=in_string)
                return True
                    
            ### if current state in list of rejecting states, then reject
            if curr_state in self.__rej_states:
                self.print_config(state=curr_state, pos=pos, in_string=in_string)
                return False
                

