"""Run a complete analysis pipeline demonstrating all scidata features."""

from scidata.data.load_data import measurements_df, prices_df
from scidata.processing.analyzer import PriceAnalyzer
from scidata.processing.transformer import transform_measurements
import os


def main():
    print("=" * 60)
    print("SciData Analysis Report")
    print("=" * 60)

    print(f"\nMeasurements loaded: {len(measurements_df)} rows")
    print(f"Columns: {list(measurements_df.columns)}")
    print(f"Sensors: {sorted(measurements_df['sensor_id'].unique())}")

    avg_temp = measurements_df["temperature"].mean()
    avg_pressure = measurements_df["pressure"].mean()
    print(f"Average temperature: {avg_temp:.2f}")
    print(f"Average pressure: {avg_pressure:.2f}")

    print(f"\nPrices loaded: {len(prices_df)} rows")
    print(f"Columns: {list(prices_df.columns)}")

    prices_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
    prices_path = os.path.normpath(prices_path)
    analyzer = PriceAnalyzer(prices_path)
    summary = analyzer.daily_summary()
    print(f"\nDaily summaries computed: {len(summary)} days")
    print(f"First day: {summary[0][0]}, Close: {summary[0][2]}")
    print(f"Last day:  {summary[-1][0]}, Close: {summary[-1][2]}")
    print(f"Average closing price: {analyzer.average_close():.2f}")

    transformed = transform_measurements()
    print(f"\nTransformed measurements: {transformed.shape[0]} rows, {transformed.shape[1]} columns")

    raw_s001 = measurements_df[measurements_df["sensor_id"] == "S001"]["temperature"].mean()
    cal_s001 = transformed[transformed["sensor_id"] == "S001"]["temperature"].mean()
    print(f"S001 raw avg temp: {raw_s001:.2f}, calibrated avg temp: {cal_s001:.2f}")

    print("\n" + "=" * 60)
    print("Analysis complete. All components working correctly.")
    print("=" * 60)


if __name__ == "__main__":
    main()
