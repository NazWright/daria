# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Set the path to the file you'd like to load
file_path = "creditcard.csv"

def load_transaction_data():
    df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        "mlg-ulb/creditcardfraud",
        file_path,
    )
    print("Fraud Transaction Dataset Analysis:", df.info())

    print("Fraud Class Distribution (Percentage):", df['Class'].value_counts(normalize=True) * 100)

    print("Fraud Class Distribution (Counts):", df['Class'].value_counts())

    return df
