from typing import List, Optional, Tuple

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class TextClassifier:
    """
    The modeling class

    """

    def __init__(self, tokenizer_name_or_path: str, model_name_or_path: str, token: Optional[str]):
        """
        Apply model and get prediction
        Parameters
        ----------
        tokenizer_name_or_path: str
            tokenizer name or path .
        model_name_or_path: str
            model name or path.
        token: Optional[str]
            hugging-face pass
        Returns
        -------
        row: MelusineItem
            Updated row.
        """
        self.tokenizer_name_or_path = tokenizer_name_or_path
        self.model_name_or_path = model_name_or_path
        self.hf_token = token
        self.load_model()

    def load_model(self) -> None:
        """
        Apply model and get prediction
        Parameters
        ----------

        Returns
        -------
        None
        """
        if self.hf_token:
            self.tokenizer = AutoTokenizer.from_pretrained(
                pretrained_model_name_or_path=self.tokenizer_name_or_path, use_auth_token=self.hf_token
            )
            self.model = AutoModelForSequenceClassification.from_pretrained(
                pretrained_model_name_or_path=self.model_name_or_path, num_labels=2, use_auth_token=self.hf_token
            )
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=self.tokenizer_name_or_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                pretrained_model_name_or_path=self.model_name_or_path, num_labels=2
            )

    def predict(self, text) -> Tuple[List, List]:
        """
        Apply model and get prediction
        Parameters
        ----------
        text: str
            Email text
        Returns
        -------
        predictions, scores: Tuple[List, List]
            Model output post softmax appliance
        """

        inputs = self.tokenizer(text, padding=True, truncation=True, return_tensors="pt")
        # Forward pass through the model
        outputs = self.model(**inputs)
        # Extract logits
        self.logits = outputs.logits
        # Convert logits to probabilities using softmax
        probs = torch.nn.functional.softmax(self.logits, dim=-1)
        probs = probs.detach().cpu().numpy()
        # Convert predictions and scores to lists
        predictions = probs.argmax(axis=1).tolist()
        scores = probs.max(axis=1).tolist()
        return predictions, scores