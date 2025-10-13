import pandas as pd
import json
import os
import uuid
from datetime import datetime
import numpy as np

class MetadataBuilder:
    """
    MetadataBuilder automatically generates and enhances metadata for datasets.
    """

    def __init__(self, source_path: str, save_dir: str = "./metadata"):
        self.source_path = source_path
        self.save_dir = save_dir
        self.dataset_name = os.path.splitext(os.path.basename(source_path))[0]
        self.df = None
        self.metadata = {}
        os.makedirs(save_dir, exist_ok=True)

    # -------------------------------------------------------------------------
    # (1) Function: Read data and build first-order metadata
    # -------------------------------------------------------------------------
    def build_first_order_metadata(self):
        """
        Reads the dataset and generates base metadata such as:
        - inferred schema (data types)
        - shape
        - null statistics
        - sample records
        """
        print(f"🔍 Reading dataset: {self.source_path}")
        self.df = pd.read_csv(self.source_path)

        inferred_schema = {
            col: str(self.df[col].dtype) for col in self.df.columns
        }

        null_stats = {
            col: float(self.df[col].isnull().mean()) for col in self.df.columns
        }

        self.metadata = {
            "dataset_id": str(uuid.uuid4()),
            "dataset_name": self.dataset_name,
            "source_path": self.source_path,
            "created_on": datetime.now().isoformat(),
            "record_count": len(self.df),
            "column_count": len(self.df.columns),
            "inferred_schema": inferred_schema,
            "null_statistics": null_stats,
            "quality_expectations": {}
        }

        print("✅ First-order metadata generated.")
        return self.metadata

    # -------------------------------------------------------------------------
    # (2) Function: AI-assisted metadata augmentation
    # -------------------------------------------------------------------------
    def ai_assisted_augmentation(self):
        """
        Uses heuristic + AI-inspired rules to infer:
        - potential primary keys
        - datetime columns
        - numerical/categorical types
        - completeness/uniqueness thresholds
        """
        print("🧠 Running AI-assisted metadata augmentation...")

        potential_keys = [
            col for col in self.df.columns
            if self.df[col].is_unique and not self.df[col].isnull().any()
        ]

        datetime_cols = [
            col for col in self.df.columns
            if pd.api.types.is_datetime64_any_dtype(self.df[col])
            or self._is_datetime_like(self.df[col])
        ]

        num_cols = [
            col for col in self.df.select_dtypes(include=[np.number]).columns
        ]
        cat_cols = [
            col for col in self.df.select_dtypes(include=["object", "category"]).columns
        ]

        # Simple heuristic-based expectations
        completeness_threshold = 0.98
        uniqueness_threshold = 1.0 if potential_keys else 0.95

        # Update metadata
        self.metadata["ai_augmented"] = {
            "potential_primary_keys": potential_keys,
            "datetime_columns": datetime_cols,
            "numerical_columns": num_cols,
            "categorical_columns": cat_cols,
            "suggested_quality_expectations": {
                "completeness_threshold": completeness_threshold,
                "uniqueness_threshold": uniqueness_threshold
            }
        }

        print("✨ Metadata augmented with AI-assisted inference.")
        return self.metadata

    # -------------------------------------------------------------------------
    # Helper function: Detect datetime-like strings
    # -------------------------------------------------------------------------
    def _is_datetime_like(self, series: pd.Series) -> bool:
        try:
            pd.to_datetime(series.dropna().sample(min(5, len(series))), errors="raise")
            return True
        except Exception:
            return False

    # -------------------------------------------------------------------------
    # Save the metadata to a JSON file
    # -------------------------------------------------------------------------
    def save_metadata(self):
        filename = f"{self.dataset_name}_metadata.json"
        file_path = os.path.join(self.save_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=4)
        print(f"💾 Metadata saved to {file_path}")
        return file_path
