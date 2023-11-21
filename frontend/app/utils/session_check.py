class Session_check:
    def check_online(session):
        """Checks if the current session includes a valid online authenticated user
        and ensures more session settings are present in the session.
        Modifies the input/output session parameter by adding some defaults if not present
        (language, invitation, ...)
        returns true if the user is online, false if user not authenticated
        """
        # print(f"SESSION: {session}")
        if "online" not in session or not session["online"]:
            session["invitation"] = "https://xyz"
            return False
        if (
            "language" not in session
            or not session["language"]
            or session["language"] not in ["en", "fr"]
        ):
            session["language"] = "en"
        return True
