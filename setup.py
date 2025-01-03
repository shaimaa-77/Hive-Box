import sys
import toml
def get_app_version():
    try:
        with open("pyproject.toml","r",encoding="utf-8") as file:
            config=toml.load(file)
        app_version=config.get("tool",{}).get("poetry",{}).get("version","unknown version")
        return app_version
    except FileNotFoundError:
        return "pyproject.toml not found"
def print_app_version():
    app_version=get_app_version()
    print( f" {app_version}")
    sys.exit(0)

if __name__=="__main__":
    print_app_version()
        