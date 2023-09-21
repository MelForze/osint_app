import subprocess
import os 


def gobuster(scope):
        modified_lines = []
        path_wordlist = f"{os.path.join(os.getcwd())}/subdomains-110000.txt"
        w_scope = scope.replace('.', '_')
        file_path = f"{os.path.join(os.getcwd())}/{w_scope}_gobuster.txt"
        result = subprocess.check_output(['gobuster','dns','-r','8.8.8.8', '-d', f'{scope}', '--wordlist',f'{path_wordlist}', '-o',f'{file_path}', '-i', '--wildcard'])
        input_file = file_path
        output_file = f'{w_scope}.txt'
        existing_output = set()
        # Читаем ранее записанные выходные строки из файла
        try:
                with open(output_file, "r") as f:
                        existing_output = set(f.read().splitlines())
        except FileNotFoundError:
                print("Файл выходных строк не найден. Создаем новый.")

        # Открываем файл для добавления новых выходных строк
        with open(output_file, "a") as f_output:
        # Читаем входные строки из файла
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
                                                                        # Добавляем новую выходную строку в файл и сохраняем во множестве существующих строк
                                                                        f_output.write(output_line + "\n")
                                                                        existing_output.add(output_line)
                                                except ValueError:
                                                        pass
        os.remove(file_path)
        print("Выходные строки успешно добавлены в файл.")

if __name__ == '__main__':
    os.system('clear')
    main = gobuster("deiteriy.com")