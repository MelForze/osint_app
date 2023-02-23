import subprocess


def ffuf(f_data):
    try:
        f_data = f_data.split(',')
        scope, port, rate, path_to_wordlist = f_data
        scope_h = scope.replace(".", "_")
        if port == '443':
            subprocess.check_output(
                ["ffuf", "-recursion", "-recursion-depth", "3", "-c", "-w", f"{path_to_wordlist}:FUZZ", "-u", f"https://{scope}/FUZZ", "-rate", f"{rate}", "-o", f"{scope_h}.html", "-of", "html", "&"])
        elif port == '80':
            subprocess.check_output(
                ["ffuf", "-recursion", "-recursion-depth", "3", "-c", "-w", f"{path_to_wordlist}:FUZZ", "-u", f"http://{scope}/FUZZ", "-rate", f"{rate}", "-o", f"{scope_h}.html", "-of", "html", "&"])
        else:
            subprocess.check_output(
                ["ffuf", "-recursion", "-recursion-depth", "3", "-c", "-w", f"{path_to_wordlist}:FUZZ", "-u", f"http://{scope}:{port}/FUZZ", "-rate", f"{rate}", "-o", f"{scope_h}.html", "-of", "html", "&"])
        print(f"{scope} already done!")
    except:
        print("ffuf broke or not installed")
