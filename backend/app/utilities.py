

def vc_profiler(vc):
    profile = {}
    features = ["basic", "schema", "refresh", "evidence", "status", "tou", "ldp", "jwt", "zkp"]
    features.remove("basic")
    if vc.get("@context"):
        profile["Context"] = []
        for context in vc["@context"]:
            if type(context) == str:
                profile["Context"].append(context)
    if vc.get("issuer"):
        if type(vc["issuer"]) == dict:
            profile["Issuer"] = vc["issuer"]["id"]
        elif type(vc["issuer"]) == str:
            profile["Issuer"] = vc["issuer"]
    if vc.get("type"):
        profile["Type"] = vc["type"]
    if vc.get("credentialStatus"):
        features.remove("status")
        profile["Status"] = vc["credentialStatus"]["type"]
    if vc.get("credentialSchema"):
        features.remove("schema")
        profile["Schema"] = vc["credentialSchema"]["type"]
    if vc.get("refreshService"):
        features.remove("refresh")
    if vc.get("termsOfUse"):
        features.remove("tou")
    if vc.get("evidence"):
        features.remove("evidence")
    if vc.get("proof"):
        if type(vc["proof"]) == dict:
            profile["Proof"] = [vc["proof"]["type"]]
        elif type(vc["proof"]) == list:
            profile["Proof"] = [proof["type"] for proof in vc["proof"]]
    # if vars(test_suite_input)["proof_type"]:
    #     features.remove(vars(test_suite_input)["proof_type"])
    return profile, features