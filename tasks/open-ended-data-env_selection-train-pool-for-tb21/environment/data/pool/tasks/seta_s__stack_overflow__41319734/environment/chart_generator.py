from collections import defaultdict
import pygal
import os

measurement_1 = defaultdict(None, [
    ("component1", [11.83, 11.35, 0.55]),
    ("component2", [2.19, 2.42, 0.96]),
    ("component3", [1.98, 2.17, 0.17]),
])

measurement_2 = defaultdict(None, [
    ("component1", [34940.57, 35260.41, 370.45]),
    ("component2", [1360.67, 1369.58, 2.69]),
    ("component3", [13355.60, 14790.81, 55.63]),
])

x_labels = ['2016-12-01', '2016-12-02', '2016-12-03']


def draw(measurement_1, measurement_2, x_labels):
    graph = pygal.Line()
    graph.x_labels = x_labels

    for key, value in measurement_1.iteritems():
        if "component1":
            graph.add(key, value, stroke_style={
                'width': 5,
                'dasharray': '3, 6',
                'linecap': 'round',
                'linejoin': 'round',
            })
        else:
            graph.add(key, value)

    for key, value in measurement_2.iteritems():
        graph.add(key, value, secondary=True)

    return graph.render_data_uri()


if __name__ == '__main__':
    draw(measurement_1, measurement_2, x_labels)
