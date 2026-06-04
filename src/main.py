import argparse
from pathlib import Path

from netflow_forensics.analysis import run_forensic_analysis
from netflow_forensics.data_loader import load_flow_data
from netflow_forensics.reporting import save_findings_report
from netflow_forensics.visualization import save_visualizations


def parse_args():
    parser = argparse.ArgumentParser(description='Run NetFlow forensic analysis.')
    parser.add_argument('--input', '-i', required=True, help='Path to NetFlow CSV file.')
    parser.add_argument('--output', '-o', default='docs/forensic_findings.md', help='Path to save the findings report.')
    parser.add_argument('--plots', '-p', default='docs/plots', help='Directory to save generated plots.')
    parser.add_argument('--skip-plots', action='store_true', help='Skip generating visualizations.')
    return parser.parse_args()


def main():
    args = parse_args()

    csv_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = load_flow_data(csv_path)
    findings = run_forensic_analysis(df)
    save_findings_report(findings, output_path)

    if not args.skip_plots:
        save_visualizations(df, Path(args.plots))
        print(f'Visualizations saved to: {args.plots}')

    print(f'Forensic analysis finished. Report saved to: {output_path}')


if __name__ == '__main__':
    main()
