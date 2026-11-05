class TransformStep:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, data):
        return self.fn(data)


class Pipeline:
    def __init__(self):
        self.transforms = []

    def add_transform(self, transform):
        step = TransformStep(transform)
        self.transforms.append(step)

    def run(self, data):
        result = data
        for step in self.transforms:
            result = step(result)
        return result
