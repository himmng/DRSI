import pandas as pd
import json
import requests
import os
import re
import time

class RSIMetadataBuilder:
    def __init__(self, api_key, model_name="openai/gpt-4o", kb_path="metadata_kb.json", max_retries=3, retry_delay=2):
        """
        Parameters
        ----------
        api_key : str
            API key
        model_name : str
            Model to use (e.g., "openai/gpt-4o")
        kb_path : str
            Path to knowledge base file (RSI memory)
        max_retries : int
            Number of retries for API call failures
        retry_delay : int
            Seconds to wait between retries
        """
        self.api_key = api_key
        self.model_name = model_name
        self.kb_path = kb_path
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.kb = self._load_kb()
    
    # ------------------ KB Management ------------------ #
    def _load_kb(self):
        if os.path.exists(self.kb_path):
            with open(self.kb_path, "r") as f:
                return json.load(f)
        return {}

    def _save_kb(self):
        with open(self.kb_path, "w") as f:
            json.dump(self.kb, f, indent=4)
    
    # ------------------ First Order Metadata ------------------ #
    def build_first_order_metadata(self, df: pd.DataFrame):
        metadata = {}
        for col in df.columns:
            metadata[col] = {
                "dtype": str(df[col].dtype),
                "missing_percent": df[col].isna().mean() * 100,
                "unique_values": df[col].nunique(),
                "sample_values": df[col].dropna().unique()[:5].tolist()
            }
        return metadata

    # ------------------ AI Call ------------------ #
    def _call_openrouter(self, prompt, url="https://openrouter.ai/api/v1/chat/completions"):
        # url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}]
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            except Exception as e:
                print(f"Attempt {attempt+1}/{self.max_retries}: {e}")
                time.sleep(self.retry_delay)
        # fallback if all retries fail
        print(f"All retries failed for prompt. Returning None.")
        return None

    # ------------------ Safe JSON Parsing ------------------ #
    @staticmethod
    def parse_json_safe(text):
        if not text:
            return None
        try:
            return json.loads(text)
        except:
            # extract JSON object from text
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    return None
            return None

    # ------------------ AI Metadata Augmentation ------------------ #
    def ai_augment_metadata(self, metadata):
        enriched_metadata = {}

        for col, info in metadata.items():
            # Check KB first
            if col in self.kb:
                print(f"[KB HIT] Using stored metadata for '{col}'")
                enriched_metadata[col] = {**info, **self.kb[col]}
                continue

            # Structured JSON prompt
            prompt = f"""
            infer the following as a valid JSON object **only** (no extra text):

            - semantic_type
            - possible_meaning
            - expected_format
            - potential_issues

            Example output:
            {{ 
            "semantic_type": "currency",
            "possible_meaning": "Total transaction amount",
            "expected_format": "float",
            "potential_issues": "Missing values or negative numbers"
            }}
            """
            ai_text = self._call_openrouter(prompt)
            enrichment = self.parse_json_safe(ai_text)

            # fallback stub if AI fails
            if enrichment is None:
                print(f"[AI Warning] Could not parse response for '{col}', using stub")
                enrichment = {
                    "semantic_type": "unknown",
                    "possible_meaning": f"Could not infer for {col}",
                    "expected_format": "unknown",
                    "potential_issues": "unknown"
                }

            enriched_metadata[col] = {**info, **enrichment}

            # Store in KB
            self.kb[col] = enrichment

        # Save KB after all columns
        self._save_kb()
        return enriched_metadata

    # ------------------ Feedback Integration ------------------ #
    def update_feedback(self, column_name, corrected_metadata):
        self.kb[column_name] = corrected_metadata
        self._save_kb()
        print(f"[Feedback Updated] KB updated for '{column_name}'.")

    # ------------------ Save Metadata ------------------ #
    def save_metadata(self, metadata, file_path="metadata.json"):
        with open(file_path, "w") as f:
            json.dump(metadata, f, indent=4)
        print(f"Metadata saved to {file_path}")
