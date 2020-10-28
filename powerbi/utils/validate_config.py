def checkconfig(config):
    """Returns a message to user for a missing configuration"""
    if config.AUTHENTICATION_MODE == "":
        return "Please specify one the two authentication modes"
    if (
        config.AUTHENTICATION_MODE.lower() == "serviceprincipal"
        and config.TENANT_ID == ""
    ):
        return "Tenant ID is not provided in the config file"
    elif config.REPORT_ID == "":
        return "Report ID is not provided"
    elif config.WORKSPACE_ID == "":
        return "Workspace ID is not provided in config file"
    elif config.CLIENT_ID == "":
        return "Client ID is not provided in config file"
    elif config.AUTHENTICATION_MODE.lower() == "masteruser":
        if config.POWER_BI_USER == "":
            return "Master account username is not provided in config file"
        elif config.POWER_BI_PASS == "":
            return "Master account password is not provided in config file"
    elif config.AUTHENTICATION_MODE.lower() == "serviceprincipal":
        if config.CLIENT_SECRET == "":
            return "Client secret is not provided in config file"
    elif config.SCOPE == "":
        return "Scope is not provided in the config file"
    elif config.AUTHORITY_URL == "":
        return "Authority URL is not provided in the config file"

    return None
