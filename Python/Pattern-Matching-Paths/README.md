Pattern-Matching Paths
======================

Problem Description
-------------------

There are two lists: the first is a list of patterns, the second
is a list of slash-separated paths. For each path, print
the pattern which best matches that path. ("Best" is defined more
rigorously below, under "Output Format".)

A pattern is a comma-separated sequence of non-empty fields. For a
pattern to match a path, every field in the pattern must exactly match
the corresponding field in the path. (Corollary: to match, a pattern and
a path must contain the same number of fields.) For example: the pattern
`x,y` can only match the path `x/y`. Note, however, that leading and
trailing slashes in paths should be ignored, thus `x/y` and `/x/y/` are
equivalent.

Patterns can also contain a special field consisting of a *single
asterisk*, which is a wildcard and can match any string in the path.

For example, the pattern `A,*,B,*,C` consists of five fields: three
strings and two wildcards. It will successfully match the paths
`A/foo/B/bar/C` and `A/123/B/456/C`, but not `A/B/C`,
`A/foo/bar/B/baz/C`, or `foo/B/bar/C`.


Input Format
------------

The first line contains an integer, N, specifying the number of
patterns. The following N lines contain one pattern per line. You may
assume every pattern is unique. The next line contains a second integer,
M, specifying the number of paths. The following M lines contain one
path per line. Only ASCII characters will appear in the input.

Output Format
-------------

For each path encountered in the input, print the *best-matching
pattern*. The best-matching pattern is the one which matches the path
using the fewest wildcards.

If there is a tie (that is, if two or more patterns with the same number
of wildcards match a path), prefer the pattern whose leftmost wildcard
appears in a field further to the right. If multiple patterns' leftmost
wildcards appear in the same field position, apply this rule recursively
to the remainder of the pattern.

For example: given the patterns `*,*,c` and `*,b,*`, and the path
`/a/b/c/`, the best-matching pattern would be `*,b,*`.

If no pattern matches the path, print `NO MATCH`.

How to execute
-----------------------

The script is runnable from a command line, it
reads from standard input and prints to standard output. 

python python pattern_matching_path.py < input_file.txt > output_file.txt


Example Input
-------------

    6
    *,b,*
    a,*,*
    *,*,c
    foo,bar,baz
    w,x,*,*
    *,x,y,z
    5
    /w/x/y/z/
    a/b/c
    foo/
    foo/bar/
    foo/bar/baz/

Example Output
--------------

    *,x,y,z
    a,*,*
    NO MATCH
    NO MATCH
    foo,bar,baz