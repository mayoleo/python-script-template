#!/usr/bin/env python

import os
import sys
import getopt
import unittest

Options = { 'verbose' : 0 }

#   Sample code.
#
class Greetings:

    def __init__(self):
        pass

    def hello(self, name):
        greeting = "Hello %s." % name
        return greeting

    def good_morning(self, name):
        greeting = "Good morning %s." % name
        return greeting

    def good_afternoon(self, name):
        greeting = "Good afternoon %s." % name
        return greeting

    def good_evening(self, name):
        greeting = "Good evening %s." % name
        return greeting

#   Sample code.
#
class GreetingsTest(unittest.TestCase):

    def test_hello(self):
        greet = Greetings()
        self.assertEqual(greet.hello("John Doe"), "Hello John Doe.")

    def test_good_morning(self):
        greet = Greetings()
        self.assertEqual(greet.good_morning("John Doe"), "Good morning John Doe.")

    def test_good_afternoon(self):
        greet = Greetings()
        self.assertEqual(greet.good_afternoon("John Doe"), "Good afternoon John Doe.")

    def test_good_evening(self):
        greet = Greetings()
        self.assertEqual(greet.good_evening("John Doe"), "Good evening John Doe.")

class UnitTest:

    def __init__(self):
        self._tests = {}
        self._tests.update({'greetings' : [ GreetingsTest, "Test Greetings class" ]}) # sample code

    def test(self, test):
        if len(self._tests) > 0:
            if test == "all":
                self._run_all_tests()
            elif test == 'list':
                self._list_all_tests()
            else:
                self._run_test(test)
        else:
            print("ERROR: No unit test available.")

    def _list_all_tests(self):
        msg = "\nAvailable unit tests:\n\n"
        for test in self._tests.keys():
            name, info = self._get_test_info(test)
            desc = info[1]
            msg += "%s - %s\n" % (name, desc)
        print(msg)

    def _run_all_tests(self):
        for test in self._tests.keys():
            self._run_test(test)

    def _run_test(self, test):
        name, info = self._get_test_info(test)
        if name != None:
            testClass = info[0]
            suite = unittest.TestLoader().loadTestsFromTestCase(testClass)
            unittest.TextTestRunner(verbosity=2).run(suite)
        else:
            print("ERROR: Unknown test '%s'" % test)
            self._list_all_tests()

    def _get_test_info(self, test):
        name = None
        info = []
        if test in self._tests.keys():
            name = test
            info = self._tests[test]
        return (name, info)

class CLIHandler():

    def __init__(self):
        self._commands = {}
        self._commands.update({'help'  : [ self._show_help,   1 ]})
        self._commands.update({'test'  : [ self._run_test,    1 ]})
        self._commands.update({'hello' : [ self._greet_hello, 1 ]}) # Sample code

    def show_usage(self):
        """
NAME
    %s - A python script template

SYNOPSIS
    %s [<options>] <commands> [<arguments>]

DESCRIPTION
    A simple template for implementating python scripts

COMMANDS
%s
OPTIONS
    --verbose
        Verbose output

VERSION
    0.10

CONTACT
    email@address
"""
        commands = ""
        for command in self._commands.keys():
            commands += "    - %s\n" % command
        out = self.show_usage.__doc__ % (Filename, Filename, commands)
        print(out)

    def _get_command_info(self, command):
        name = None
        info = []
        if command in self._commands.keys():
            name = command
            info = self._commands[command]
        return (name, info)

    def get_opts_args(self):
        try:
            longopts = []
            for key, value in Options.iteritems():
                if isinstance(value, str) == 1:
                    key += "="
                    longopts.append(key)
                else:
                    longopts.append(key)
            opts, args = getopt.getopt(sys.argv[1:], "", longopts)
        except getopt.error, msg:
            print(msg)
            sys.exit(2)
        for opt, arg in opts:
            for key, value in Options.iteritems():
                tmp = "--%s" % key
                if opt == tmp:
                    if isinstance(value, str) == 1:
                        Options[key] = arg
                    else:
                        Options[key] = 1
        return args

    def process_args(self, args):
        command = args[0]
        name, info = self._get_command_info(command)
        if name != None:
            handler = info[0]
            arg_num = info[1]
            if len(args[1:]) >= arg_num:
                handler(args[1:])
            else:
                print("ERROR: Missing arguments for command '%s'" % name)
                self._show_help([name, ""])
        else:
            print("ERROR: Unknown command '%s'" % command)
            print("Run '%s' to see list of supported commands" % Filename) 

    def _show_help(self, args):
        """
SYNOPSIS
    %s help <command>

DESCRIPTION
    Show help for command.
        """
        command = args[0]
        name, info = self._get_command_info(command)
        if name != None:
            handler = info[0]
            print(handler.__doc__ % Filename)
        else:
            print("ERROR: Unknown command %s" % command)

    def _run_test(self, args):
        """
SYNOPSIS
    %s test <name>

DESCRIPTION
    Run unit test named <name>. Use 'all' to run all unit tests. Use 'list'
    to list available unit tests.
        """
        unittest = UnitTest()
        unittest.test(args[0])

    #   Sameple code
    #
    def _greet_hello(self, args):
        """
SYNOPSIS
    %s hello <name>

DESCRIPTION
    Greet <name> with hello.
        """
        greet = Greetings()
        print(greet.hello(args[0]))

Filename = os.path.basename(__file__)
CLI = CLIHandler()

def main():
    args = CLI.get_opts_args()
    log("ARGS: %s" % args)
    log("OPTS: %s" % Options)
    if len(args) > 0:
        CLI.process_args(args)
    else:
        print("ERROR: Missing <command>")
        CLI.show_usage()

def log(msg, priority=1):
    if Options['verbose'] >= priority:
        print(msg)

if __name__ == "__main__":
    main()