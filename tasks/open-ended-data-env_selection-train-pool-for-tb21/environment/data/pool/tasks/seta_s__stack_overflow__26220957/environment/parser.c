#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libxml/parser.h>
#include <libxml/tree.h>

int parse_xml_file(const char *filename) {
    xmlDocPtr doc = xmlParseFile(filename);
    if (doc == NULL) {
        fprintf(stderr, "Failed to parse %s\n", filename);
        return -1;
    }

    xmlNodePtr root = xmlDocGetRootElement(doc);
    if (root == NULL) {
        fprintf(stderr, "Empty document\n");
        xmlFreeDoc(doc);
        return -1;
    }

    printf("Root element: %s\n", root->name);

    xmlFreeDoc(doc);
    xmlCleanupParser();
    return 0;
}

int count_xml_elements(const char *filename) {
    xmlDocPtr doc = xmlParseFile(filename);
    if (doc == NULL) {
        return -1;
    }

    xmlNodePtr root = xmlDocGetRootElement(doc);
    int count = 0;
    for (xmlNodePtr cur = root->children; cur; cur = cur->next) {
        if (cur->type == XML_ELEMENT_NODE) {
            count++;
        }
    }

    xmlFreeDoc(doc);
    return count;
}

const char* get_parser_version(void) {
    return "dataproc-parser-1.0";
}
