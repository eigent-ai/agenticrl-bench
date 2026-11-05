from data_processor import DataProcessor

def test_data_processor():
    dp = DataProcessor([1, 2, 3])
    assert dp.process() == [2, 4, 6]
