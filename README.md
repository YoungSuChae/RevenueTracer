# RevenueTracer

RevenueTracer is a Python-based application for managing stores, departments, items, users, and their associated data. It includes features such as user account management, revenue forecasting, and interactive analysis tools.

## Features

- **User Account Management**: Create accounts, log in, and manage user information.
- **Store Management**: Add, search, and delete store data.
- **Department Management**: Manage department details including addition, search, and deletion.
- **Item Management**: Add, search, and delete items.
- **Revenue Analysis and Forecasting**: Visualize and predict revenue trends using machine learning models.
- **Interactive GUI**: Built with PyQt6 for a rich user interface.

## Prerequisites

Before running the project, ensure the following are installed on your system:

- Python 3.8 or higher

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/RevenueTracer.git
   cd RevenueTracer
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

The project requires the following Python packages:

- PyQt6: `pip install PyQt6`
- pandas: `pip install pandas`
- matplotlib: `pip install matplotlib`
- scikit-learn: `pip install scikit-learn`
- numpy: `pip install numpy`

Ensure that the following CSV files are included in the root folder:

- `ItemList.csv`
- `Store.csv`
- `userInfo.csv`
- `department.csv`

These files store data for items, stores, users, and departments, respectively.

## Running the Project

1. Run the application:

   ```bash
   python Main.py
   ```

2. Follow the instructions in the GUI for account management, revenue analysis, and more.

## File Structure

- `Main.py`: Entry point for the application.
- `SaleInterface.py`: GUI logic for the main sales interface.
- `LoginCreatePage.py`: GUI logic for login and account creation.
- `User.py`: Handles user-related functionalities.
- `Store.py`: Manages store-related operations.
- `Department.py`: Handles department data.
- `Item.py`: Manages item-related functionalities.
- `model.py`: Machine learning model for revenue forecasting.

## Features Overview

### Login and Account Creation

Use the login interface to create a user account or log in to access features.

### Store Management

Add, search, and delete stores using the Store tab.

### Revenue Forecasting

The application uses a linear regression model to predict future revenues and display trends.

### Interactive GUI

Navigate through various tabs for departments, items, and sales analysis.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Feel free to submit issues or pull requests for improvements and bug fixes.
