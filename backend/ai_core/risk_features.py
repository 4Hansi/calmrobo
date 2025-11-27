# backend/ai_core/risk_features.py

def feature_list():
    """
    Canonical order of features used by the RF model.
    Keep this in sync with synthetic_data and training code.
    """
    return ["age", "income", "tolerance", "horizon_years", "volatility_pref"]


def ensure_feature_order(features_dict, expected_list=None):
    """
    Convert an input dict (possibly containing None) into a list of floats
    in the exact order expected by the model.
    Missing or null values => 0.0 default (model can handle).
    """
    order = expected_list or feature_list()
    out = []
    for k in order:
        v = features_dict.get(k, None)
        try:
            # handle strings like "30" too
            if v is None:
                out.append(0.0)
            else:
                out.append(float(v))
        except Exception:
            out.append(0.0)
    return out
