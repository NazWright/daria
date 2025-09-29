"""daredev_fraud package

This package is intentionally small. We provide a compatibility shim so notebooks and examples
that import `load_fraud_dataset` continue to work even though the loader function is named
`load_transaction_data` in `data_ingestion.loader`.

Notes:
- KaggleHub requires extras for pandas datasets: `pip install kagglehub[pandas-datasets]`
"""
        
from .data_ingestion.loader import load_transaction_data as load_fraud_dataset

__all__ = ["load_fraud_dataset"]
