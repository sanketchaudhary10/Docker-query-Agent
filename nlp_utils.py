# import spacy
# import re

# # Load the spaCy model
# nlp = spacy.load("en_core_web_sm")

# def parse_query(query):
#     """Parse the query to extract intent and relevant keywords."""
#     doc = nlp(query.lower())
#     intents = {
#         "pods": ["pods", "workload", "containers"],
#         "namespace": ["namespace", "default namespace"],
#         "deployments": ["deployments", "apps", "applications"],
#         "logs": ["logs", "events", "details"]
#     }

#     # Match intents based on query keywords
#     identified_intents = {
#         key: any(keyword in query for keyword in keywords)
#         for key, keywords in intents.items()
#     }

#     # Extract nouns and other important tokens for processing
#     extracted_keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]

#     # Return the detected intent and relevant tokens
#     return identified_intents, extracted_keywords



import spacy
import re

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def parse_query(query):
    query_cleaned = re.sub(r"[^\w\s\-_]", "", query.lower())
    doc = nlp(query_cleaned)

    intents = {
        "pods": ["pod", "pods", "workload", "container"],
        "namespace": ["namespace", "default"],
        "status": ["status", "state", "condition"],
        "deployments": ["deployment", "app", "application"],
        "logs": ["log", "event", "detail"]
    }

    # Detect intents
    identified_intents = {
        key: any(token.text in intents[key] for token in doc)
        for key in intents.keys()
    }

    # Extract Kubernetes-like names
    extracted_keywords = []
    pod_pattern = re.compile(r"[a-zA-Z0-9\-]+")  # Matches Kubernetes-like names
    for token in doc:
        if pod_pattern.match(token.text):
            extracted_keywords.append(token.text.strip())

    # Validate keywords for deployment names
    valid_keywords = [kw for kw in extracted_keywords if "-" in kw or kw.isalnum()]
    deployment_name = next((kw for kw in valid_keywords if "deployment" in kw.lower()), None)

    return identified_intents, valid_keywords, deployment_name

