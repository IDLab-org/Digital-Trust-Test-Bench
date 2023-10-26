# from pyld import jsonld
# import json

def vc_profiler(vc):
    # expanded = jsonld.expand(vc)
    # print(json.dumps(expanded, indent=2))
    # flattened = jsonld.flatten(vc)
    # print(json.dumps(flattened, indent=2))
    basic = {
        "Context": vc.get("@context"),
        "Credential Type": vc.get("type"),
        "Issuer": vc.get("issuer"),
        "Issuance Date": vc.get("issuanceDate"),
        "Credential Subject": vc.get("credentialSubject"),
        "Proof": vc.get("proof"),
    }
    features = {
        "Credential Id": vc.get("id"),
        "Expiration Date": vc.get("expirationDate"),
        "Credential Schema": vc.get("credentialSchema"),
        "Refresh Service": vc.get("refreshService"),
        "Evidence": vc.get("evidence"),
        "Credential Status": vc.get("credentialStatus"),
        "Terms of Use": vc.get("termsOfUse"),
    }
    vc_profile = basic | features
    return vc_profile
