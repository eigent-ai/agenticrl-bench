#include "tree.h"
#include <iostream>
#include <vector>
#include <string>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <datafile>" << std::endl;
        return 1;
    }

    std::vector<int> test_vec = {10, 20, 30, 40, 50};

    std::vector<Node*> nodes = parse_tree(argv[1]);
    if (nodes.empty()) {
        std::cerr << "Error: no nodes parsed" << std::endl;
        return 1;
    }

    Node* root = nodes[0];
    print_stats(root, nodes);

    for (auto* n : nodes) delete n;
    return 0;
}
