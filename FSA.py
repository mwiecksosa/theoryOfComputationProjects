#!/usr/bin/python2

"""
CISC 4090 (Theory of Computation)
Spring, 2020

Project 1: A Deterministic Finite-State Automaton

This file describes a class FSA that implements a deterministic
finite state automaton.

This implementation does no error-checking on the input file. 

Author: Michael Wieck-Sosa
Date:   February 10, 2020"""

import sys

class FSA:

    """Initialize class FSA by reading in the input string, splitting by white space,
    and assigning variables alphabet, number of states, starting state, accept states, transitions.
    Calls __get_state_stable member function to assemble the state table defining transitions."""
    def __init__(self, ifs):

        data = ifs.read().split() ### read() string ifs, split() by whitespace, then store in data variable
        
        self.alphabet = data[0] ### possible elements for input strings of the FSA, implicitly including the empty string
        self.numStates = data[1] ### total number of states of the FSA
        self.startState = data[2] ### initial state of the FSA
        self.numAcceptStates = data[3] ### number of accept states of the FSA
        self.acceptStates = data[4:(4+int(self.numAcceptStates))] ### final accept states of the FSA
                                                                  ### if 1, then gets [data[4]]
                                                                  ### if 2, then gets [data[4], data[5]]
        self.trans = data[(4+int(self.numAcceptStates)):] ### transitions from one state to another given an input
                                                          ### if 1, then gets [data[5], data[6], ... data[-1]]
                                                          ### if 2, then gets [data[6], data[7], ... data[-1]]

        self.__get_state_table() ### call to get_state_table() member function

    """Member function to have self.state_table hold the state table from the given states and transition functions."""
    def __get_state_table(self):     

        self.state_table = dict() ### initialize state_table as empty dictionary

        for i in range(int(self.numStates)):
            self.state_table[i+1] = (self.trans[2*i], self.trans[2*i+1]) ### assign dictionary key a 2-tuple of transitions 
                                                                         ### 2*i for when a is input, and 2*i+1 for when b is input
    
    """Member function to print the contents of the FSA to describe it. 
    Will print alphabet, # of states, starting state, # accepting states, and the state table"""
    def describe(self):
        
        print "alphabet = " + self.alphabet 
        print "# states = " + self.numStates
        print "start state = " + self.startState
        print "accept states = " + ' '.join(self.acceptStates) 
        print "state table:"
        
        for state, trans in self.state_table.items(): ### loop through state_table dictionary keys=states, values=transitions
            print str(state) + ":  " + str(trans[0]) + " " + str(trans[1]) ### print state and a, b transitions

    """Member function to trace the states and determine & print whether input string is accepted or not. 
    Raises EOFError when parsing through string and reads an element not in the FSA alphabet"""
    def trace(self, in_string):
        
        stateTrace = [self.startState] ### variable stateTrace is list of current & previous states 
    
        currState = self.startState ### variable currState holds the current state

        if in_string is '': ### if the current element of the input string is the empty string

            if currState in self.acceptStates: ### if current state is in 2-tuple of accept states, then accept
                print "State trace: " + ' '.join(stateTrace) + " ... accepted" 

            else: ### else the current state is not in 2-tuple of accept states, then not accepted
                print "State trace: " + ' '.join(stateTrace) + " ... not accepted"

        for i in range(len(in_string)): ### loop through 0 to the length of the string, access elements with in_string[i]
                                        ### loop does not execute if empty string so implicit conditional is not '' 

            if in_string[i] in self.alphabet: ### if current element of input string is in the FSA alphabet

                if in_string[i] is self.alphabet[0]: ### if current element of the string is a
                    stateTrace.append(self.state_table[int(currState)][0]) ### add to the list of current & previous states
                    currState = self.state_table[int(currState)][0] ### make the transition caused by this element the current state
               
                elif in_string[i] is self.alphabet[1]: ### if current element of the input string is b
                    stateTrace.append(self.state_table[int(currState)][1]) ### add to the list of current & previous states
                    currState = self.state_table[int(currState)][1] ### make the transition caused by this element the current state

            else: ### else current element of input string is NOT in the FSA alphabet            
                print "State trace: " + ' '.join(stateTrace) 
                print "Illegal input!" 
    
                raise EOFError ### raise for end of file condition because encountered element not in alphabet

            if i is len(in_string)-1: ### if currently parsing last element of the string

                if currState in self.acceptStates: ### if current state is in 2-tuple of accept states, then accept
                    print "State trace: " + ' '.join(stateTrace) + " ... accepted" 

                else: ### else the current state is not in 2-tuple of accept states, then not accepted
                    print "State trace: " + ' '.join(stateTrace) + " ... not accepted" 




