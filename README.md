# Stock Analysis Workflow

This repository contains a GitHub Actions workflow for performing stock analysis on a daily basis. The workflow fetches stock data, calculates relevant metrics, and generates results that are automatically committed to the repository.

## Main Code

The main code responsible for the stock analysis is located in the following file:

- [Stock Analysis Script](main.py)

## Main Results

The results of the stock analysis are generated daily and can be found in the following file:

- [Results](results.txt)

## Log File

Detailed logs of the workflow execution are maintained in the following file:

- [Log File](log.txt)

## Framework Used

This project utilizes the following tools and frameworks:

- **Python**: The main programming language used for writing the stock analysis script.
- **yfinance**: A Python library to fetch historical market data from Yahoo Finance.
- **pandas**: A Python library used for data manipulation and analysis.
- **GitHub Actions**: For automating the daily execution of the stock analysis script.

## Workflow Details

The GitHub Actions workflow is defined in the following file:

- [.github/workflows/stock-analysis.yml](.github/workflows/stock-screener.yaml)

### Workflow Schedule

The workflow is scheduled to run every weekday (Monday to Friday) at 3:45 PM IST.

## How to Manually Trigger the Workflow

1. Go to the "Actions" tab in your repository on GitHub.
2. Select the "Run Stock Analysis" workflow.
3. Click on the "Run workflow" button.

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements or find any bugs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
