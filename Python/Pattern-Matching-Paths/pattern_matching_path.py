import sys


class Node:
    """
    An object representing a node in the tree/linked list structure
    """
    def __init__(self, data, children):
        self.data = data
        self.children = children
        self.is_leaf = False
        self.is_root = False
        self.path = []

    def __repr__(self):
        return repr("Node(" + self.data + ")")

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return self.data == other.data or other.data == "*"

    def get_path(self):
        return [p.data for p in self.path]


class Pattern:
    """
    An abstraction of a pattern, it contains the number of wildcards, the leftmost index of the wildcard
    and the original pattern as list from standard input
    """
    def __init__(self, leftmost, wildcards, pattern):
        self.leftmost = leftmost
        self.wildcards = wildcards
        self.pattern = pattern

    def __repr__(self):
        return repr("LeftMost: " + str(self.leftmost) + ", Wildcards: " + str(self.wildcards) + ", Pattern: " + str(
            self.pattern))


class CustomTrie:
    _map = {}

    def __init__(self):
        self._map = {}

    def make(self, paths):
        """
        Construct the trie tree, using dict as the underlining structure for holding each children from the root
        :param paths: the paths to explore
        :return: the tree
        """
        self._map = {}
        for path in paths:
            head = self._map.setdefault(path[0], Node(path[0], {}))
            # create head node, if only one item in path, then set as leaf
            if len(path[1:]) == 0:
                head.is_leaf = True
            elif not head.is_leaf:
                head.is_leaf = False

            # this is a root node
            head.is_root = True
            node = None

            # for each word in path, create a node if not already a child of the previous
            # then linked it with the previous as a child
            for word in path[1:]:
                node = head.children.get(word, None)
                if node is None:
                    # new node
                    node = Node(word, {})
                    # add as child to previous node
                    head.children.setdefault(word, node)
                    # set previous node as non leaf
                    if not head.is_leaf:
                        head.is_leaf = False

                    # update the path taken from root to current node
                    node.path.append(head)
                    tmp = list(head.path)
                    tmp.extend(node.path)
                    node.path = tmp

                # make this current node the head
                head = node

            # set current node as leaf
            if node is not None:
                node.is_leaf = True

        return self._map

    def get_tree_paths(self):
        """
        Iteratively traverses the tree and their children,
        Returns the all the linked path from root to each leaf node
        :return:
        """
        children = self.map
        tree_paths = []
        while 1:
            new_nodes = {}
            if len(children) == 0:
                break
            for word in children:
                node = children.get(word)
                # check if leaf node, if leaf node add the the tree path list
                if node.is_leaf:
                    node.path.append(node)
                    #print node,
                    #print node.path
                    tree_paths.append(node.path)

                # traverse the children of the node if any
                if len(node.children) > 0:
                    for child in node.children:
                        new_nodes[child] = node.children.get(child)

            children = new_nodes
        return tree_paths

    def find_pattern(self, paths=[], patterns=[]):
        """
        return, for each path,
        the pattern which best matches that path
        """
        best_list = {}
        for path in paths:
            matched_pattern = []
            for pattern in patterns:
                is_matched, leftmost, wildcards = self.is_pattern_matched(path, pattern)
                if is_matched:
                    matched_pattern.append(Pattern(leftmost, wildcards, pattern))

            #print 'matched pattern for path: ', path
            #print matched_pattern
            #print ''
            if len(matched_pattern) > 0:
                best = self.get_best_pattern(matched_pattern)
                best_list["".join(path[-1].get_path())] = best.pattern
            else:
                best_list["".join(path[-1].get_path())] = ["NO MATCH"]

        return best_list

    def is_pattern_matched(self, path=[], pattern=[]):
        """
        Returns true is pattern matches the path.  Also returns the number of wildcard and the leftmost wildcard
        for the pattern
        """
        leftmost = None
        wildcards = 0
        if len(path) != len(pattern):
            # 'path not valid: ', path
            is_matched = False
        else:
            # 'explore path: ', path
            is_matched = False
            for i, word in enumerate(pattern):
                if word == path[i].data or word == "*":
                    is_matched = True
                    if word is "*":
                        wildcards += 1
                        if leftmost is None:
                            leftmost = i

                else:
                    is_matched = False
                    break

        return is_matched, leftmost, wildcards

    def get_best_pattern(self, matched_pattern=[]):
        """
        Given a list of pattern, determines and return the best pattern.
        The best-matching pattern is the one which matches the path
        using the fewest wildcards.

        If there is a tie (that is, if two or more patterns with the same number
        of wildcards match a path), prefer the pattern whose leftmost wildcard
        appears in a field further to the right. If multiple patterns' leftmost
        wildcards appear in the same field position, apply this rule recursively
        to the remainder of the pattern.
        """
        best = matched_pattern[0]
        for pattern in matched_pattern[1:]:
            if pattern.wildcards < best.wildcards:
                best = pattern
            if pattern.wildcards == best.wildcards:
                if pattern.leftmost > best.leftmost:
                    best = pattern
        return best

    @property
    def map(self):
        return self._map


def main(pattern=[], paths=[]):
    """
    Given two lists: the first is a list of patterns, the second
    is a list of slash-separated paths. For each path, print
    the pattern which best matches that path.
    """

    # Use a form of trie tree structure to hold all nodes in the path
    # the children of each node is a key value dictionary, each node also has
    # a reference to their respective children
    trie = CustomTrie()
    trie.make(paths)

    # retrieve all link path from root to each leaf
    # the tree_path is a list of linked list containing all path from root to each leaf node
    tree_paths = trie.get_tree_paths()

    # find the best pattern that matches each path
    # best_pattern is a dictionary that holds the best pattern for each path, key is the joined items of a path
    best_pattern = trie.find_pattern(tree_paths, pattern)

    # sort the best pattern base on the sequence in paths
    best_pattern = [best_pattern["".join(p)] for p in paths]
    return best_pattern

# The program runs in quadratic time, O(n*m*k) in worst case, where n and m, is the number of path and patterns and k
# is a static value representing the longest pattern, therefore running is essentially Big-O(n*m).  The worst case 
# occurs when the longest pattern contains all wildcard.  Can it be improve? Perhaps.

# it should be runnable like this:
# python pattern_recognition.py < input_file.txt > output_file.txt
__author__ = 'Ejiro'
if __name__ == '__main__':
    # reads from standard input and prints to standard output
    infile = sys.stdin
    outfile = sys.stdout
    if len(sys.argv) > 1:
        infile = open(sys.argv[1])
        outfile = open(sys.argv[2], 'w')


    # parse the input file data
    index = 0
    n_patterns = 0
    n_paths = 0
    patterns_list = []
    path_list = []
    try:
        for line in infile:
            if index == 0:
                n_patterns = int(line)
            if index == n_patterns+1:
                n_paths = int(line)
            if 0 < index <= n_patterns:
                patterns_list.extend([line.strip().split(",")])
            if n_patterns+1 < index <= n_patterns+n_paths+1:
                path_list.extend([line.strip().strip("/").rstrip("/").split("/")])
            index += 1
    except ValueError:
        # invalid input
        print ""

    # execute and prints out to stdout
    results = main(patterns_list, path_list)
    for line in results:
        outfile.write(",".join(line)+"\n")

    # exit program
    sys.exit()