import subprocess
import ipaddress
import os 

def gobuster(scope):
        path_wordlist = f"{os.path.join(os.getcwd())}/subdomains-110000.txt"
        w_scope = scope.replace('.', '_')
        file_path = f"{os.path.join(os.getcwd())}/{w_scope}_gobuster.txt"
        subprocess.check_output(['gobuster','dns','-r','8.8.8.8', '-d', f'{scope}', '--wordlist',f'{path_wordlist}','-t', '100', '-o', f'{file_path}', '-i', '--wildcard'])
        input_file = file_path
        output_file = f'{w_scope}.txt'
        existing_output = set()
        try:
                with open(output_file, "r") as f:
                        existing_output = set(f.read().splitlines())
        except FileNotFoundError:
                print("Файл выходных строк не найден. Создаем новый.")

        with open(output_file, "a") as f_output:
                with open(input_file, "r") as f_input:
                        for line in f_input:
                                if line.startswith("Found:"):
                                        parts = line.split("[")
                                        domain = parts[0].split(": ")[1].strip()
                                        ips = parts[1].replace("]", "").split(",")
                                        for ip in ips:
                                                ip = ip.strip()
                                                try:
                                                        if ipaddress.ip_address(ip).version == 4:
                                                                output_line = "{},{}".format(domain, ip)
                                                                if output_line not in existing_output:
                                                                        f_output.write(output_line + "\n")
                                                                        existing_output.add(output_line)
                                                except ValueError:
                                                        pass
        os.remove(file_path)