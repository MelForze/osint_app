import ssl
import socket


def check_wildcard(scope):
    sub_scope = []
    unique_domain = []
    certificates = {}
    count = 0
    for domain in scope:
        parts = domain.split(".")
        if len(parts) > 2:
            second_part = ".".join(parts[1:])
            sub_scope.append(second_part)
        else:
            sub_scope.append(domain)
    for element in sub_scope:
        if element not in unique_domain:
            unique_domain.append(element)
    for f_domain in unique_domain:
        file_to_domain = f_domain.replace('.', '_')
        with open(f"{file_to_domain}.txt", "r") as f:
            for line in f:
                h_line = line.strip().split(',')
                hostname = h_line[0]
                context = ssl.create_default_context()
                try:
                    with socket.create_connection((hostname, 443), 1) as sock:
                        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                            cert = ssock.getpeercert()
                            serial_number = cert.get("serialNumber")
                            certificates[hostname] = serial_number
                except:
                    pass
    for domain in scope:
        wildcard = [key for key, value in certificates.items()
                    if value == certificates[domain] and key != domain]
        count += 1
        print(f"{count}) {domain}", "Wildcard domains", wildcard,
              "Certificate number: ", certificates[domain])
