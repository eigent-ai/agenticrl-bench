from preprocessing.pipeline import run_pipeline

results = run_pipeline(
    train_path="data/train.csv",
    test_path="data/test.csv",
    output_path="output/results.json",
)
print("Pipeline complete. Results saved to output/results.json")
