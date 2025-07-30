# Crypto Operational Loss Mitigation Simulator

## Table of Contents
1.  [Project Title and Description](#1-project-title-and-description)
2.  [Features](#2-features)
3.  [Getting Started](#3-getting-started)
    *   [Prerequisites](#prerequisites)
    *   [Installation](#installation)
4.  [Usage](#4-usage)
5.  [Project Structure](#5-project-structure)
6.  [Technology Stack](#6-technology-stack)
7.  [Contributing](#7-contributing)
8.  [License](#8-license)
9.  [Contact](#9-contact)

---

## 1. Project Title and Description

**QuLab: Crypto Operational Loss Mitigation Simulator**

This Streamlit application provides an interactive platform for simulating operational loss events within a hypothetical cryptocurrency exchange environment. Its primary objective is to demonstrate and analyze the financial impact of different insurance-like mitigation strategies, such as self-insurance funds or traditional excess-of-loss policies.

Users can adjust various parameters related to loss severity distributions and mitigation policy structures to observe real-time changes in simulated outcomes, cumulative losses, and financial summaries. This lab serves as a practical tool for understanding risk transfer mechanisms and their impact on an organization's retained risk.

---

## 2. Features

*   **Loss Event Simulation**: Simulate a customizable number of operational loss events.
*   **Flexible Severity Distributions**: Model loss severity using common statistical distributions:
    *   Lognormal Distribution
    *   Pareto Distribution
    *   Exponential Distribution
*   **Customizable Mitigation Policy**: Define an insurance-like policy with:
    *   Deductible: The initial amount of loss borne by the organization.
    *   Cover: The maximum amount the policy will pay out per event.
*   **Interactive Visualizations**:
    *   **Payout Function Plot**: Visualize how the deductible and cover affect the transferred and retained loss for individual events.
    *   **Cumulative Losses Trend**: Track the cumulative gross and retained losses over the simulated events, demonstrating risk reduction.
    *   **Gross vs. Transferred Loss Relationship**: Scatter plot showing the correlation between original gross loss and the amount paid out by the policy.
    *   **Aggregated Loss Comparison**: Bar chart summarizing total gross, transferred, and retained losses.
*   **Financial Summary**: Display key aggregated financial metrics (Total Gross Loss, Total Transferred Loss, Total Retained Loss).
*   **Educational Content**: A dedicated "Explanation" page detailing the concepts, formulae, and distributions used in the simulator.
*   **About Section**: Information about the lab project, contributors, and references.

---

## 3. Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

*   Python 3.7+ (Recommended: Python 3.9 or higher)
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/qu-lab-crypto-loss-simulator.git
    cd qu-lab-crypto-loss-simulator
    ```
    *(Replace `your-username/qu-lab-crypto-loss-simulator.git` with the actual repository URL)*

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required packages:**
    Create a `requirements.txt` file in your project root with the following content:
    ```
    streamlit>=1.20.0
    pandas>=1.4.0
    numpy>=1.22.0
    plotly>=5.0.0
    matplotlib>=3.5.0
    ```
    Then install them:
    ```bash
    pip install -r requirements.txt
    ```

---

## 4. Usage

To run the Streamlit application:

1.  **Ensure your virtual environment is activated** (if you created one).
2.  **Navigate to the project's root directory** (where `app.py` is located).
3.  **Run the Streamlit application** using the command:
    ```bash
    streamlit run app.py
    ```

This command will open the application in your default web browser (usually at `http://localhost:8501`).

**How to Use:**
*   **Navigation:** Use the sidebar `Navigation` select box to switch between the "Simulator", "Explanation", and "About" pages.
*   **Simulator Page:**
    *   Adjust `Simulation Parameters` in the sidebar to change the `Number of Events` and the `Loss Severity Distribution Type` along with its specific parameters (e.g., `Mean of Log`, `Std Dev of Log` for Lognormal).
    *   Modify `Mitigation Policy Parameters` by setting the `Deductible (d)` and `Cover (c)`.
    *   Observe how the changes in parameters instantly update the data table, descriptive statistics, and all the visualization plots and financial summaries.

---

## 5. Project Structure

The project is organized into modular files for clarity and maintainability:

```
qu-lab-crypto-loss-simulator/
├── app.py                      # Main Streamlit application entry point and navigation logic.
├── application_pages/          # Directory containing individual page modules.
│   ├── __init__.py             # Makes application_pages a Python package.
│   ├── page1.py                # Contains the core simulator logic, functions, and UI for the "Simulator" page.
│   ├── page2.py                # Defines the content for the "Explanation" page.
│   └── page3.py                # Defines the content for the "About" page.
├── requirements.txt            # Lists all Python dependencies for the project.
└── README.md                   # This README file.
```

---

## 6. Technology Stack

*   **Python**: The core programming language.
*   **Streamlit**: The open-source app framework used to build and deploy the web application.
*   **Pandas**: Used for data manipulation and analysis, especially for handling simulated loss dataframes.
*   **NumPy**: Essential for numerical operations, particularly for generating random numbers based on statistical distributions.
*   **Plotly**: Utilized for creating interactive and dynamic visualizations, such as the payout function.
*   **Matplotlib**: Used for generating static plots like cumulative loss trends and aggregated comparisons.

---

## 7. Contributing

Contributions are welcome! If you have suggestions for improvements, bug fixes, or new features, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

Please ensure your code adheres to good practices and includes appropriate tests if applicable.

---

## 8. License

This project is licensed under the MIT License - see the `LICENSE` file for details (if you plan to include one, otherwise remove this line).
*Note: If no explicit LICENSE file is provided, a standard open-source license like MIT is generally assumed for public projects of this nature.*

---


## License

## QuantUniversity License

© QuantUniversity 2025  
This notebook was created for **educational purposes only** and is **not intended for commercial use**.  

- You **may not copy, share, or redistribute** this notebook **without explicit permission** from QuantUniversity.  
- You **may not delete or modify this license cell** without authorization.  
- This notebook was generated using **QuCreate**, an AI-powered assistant.  
- Content generated by AI may contain **hallucinated or incorrect information**. Please **verify before using**.  

All rights reserved. For permissions or commercial licensing, contact: [info@qusandbox.com](mailto:info@qusandbox.com)
