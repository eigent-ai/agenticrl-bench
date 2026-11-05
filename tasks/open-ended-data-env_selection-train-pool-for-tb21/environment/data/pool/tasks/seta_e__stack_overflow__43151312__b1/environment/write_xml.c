#include <libxml/parser.h>
#include <libxml/tree.h>
#include <stdio.h>
#include <string.h>

#define FILE_NAME  "output.xml"
#define NX 4
#define NY 6

int main(void) {
    xmlDocPtr  doc;
    xmlNodePtr root, row_node, cell_node;
    char       buf[32];
    int        i, j;

    doc  = xmlNewDoc(BAD_CAST "1.0");
    root = xmlNewNode(NULL, BAD_CAST "matrix");
    xmlDocSetRootElement(doc, root);

    snprintf(buf, sizeof(buf), "%d", NX);
    xmlNewProp(root, BAD_CAST "rows", BAD_CAST buf);
    snprintf(buf, sizeof(buf), "%d", NY);
    xmlNewProp(root, BAD_CAST "cols", BAD_CAST buf);

    for (i = 0; i < NX; i++) {
        row_node = xmlNewChild(root, NULL, BAD_CAST "row", NULL);
        snprintf(buf, sizeof(buf), "%d", i);
        xmlNewProp(row_node, BAD_CAST "index", BAD_CAST buf);

        for (j = 0; j < NY; j++) {
            snprintf(buf, sizeof(buf), "%d", i * NY + j);
            cell_node = xmlNewChild(row_node, NULL, BAD_CAST "cell", BAD_CAST buf);
            snprintf(buf, sizeof(buf), "%d", j);
            xmlNewProp(cell_node, BAD_CAST "col", BAD_CAST buf);
        }
    }

    int ret = xmlSaveFormatFileEnc(FILE_NAME, doc, "UTF-8", 1);
    xmlFreeDoc(doc);
    xmlCleanupParser();

    return (ret > 0) ? 0 : 1;
}
