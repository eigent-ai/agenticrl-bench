#ifndef TREE_H
#define TREE_H

#include <vector>
#include <string>

struct Node {
    int id;
    std::string name;
    std::vector<int> values;
    std::vector<bool> active_flags;
    std::vector<Node*> children;
};

std::vector<Node*> parse_tree(const std::string& filename);
int local_sum(Node* node);
int aggregate(Node* node);
void print_stats(Node* root, std::vector<Node*>& all_nodes);

#endif
