import argparse
import time
import multiprocessing
import subfinder as subfinder
import gobuster as gobuster
import ffuf as ffuf
import wildcard as wildcard
from headers_check import check_headers

parser = argparse.ArgumentParser()
parser.add_argument("-s", "-scope", type=str,
                    help="Domains in scoope:", required=True)
parser.add_argument("-sub", '-subfinder', type=str,
                    help="Search neighboring domains", required=False, default="no")
parser.add_argument("-f", "-ffuf", type=str, help="switch on ffuf ",
                    required=False, default="no")
parser.add_argument("-p", "-port", type=int, help="port ffuf",
                    required=False, default=443)
parser.add_argument("-r", "-rate", type=int, help="rate for  ffuf",
                    required=False, default=150)
parser.add_argument("-w", "-worlists", type=str,
                    help="Path to wordlists for ffuf")

if __name__ == '__main__':
    start_prog = time.time()
    f_data = []
    args = parser.parse_args()
    sub_scope = []
    unique_domain = []
    number_domain = 0
    scope = args.s.split(",")
    print("Domains in scope:")
    print('\n'.join(scope), '\n')
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
    if args.sub != 'no':
        with multiprocessing.Pool(multiprocessing.cpu_count()) as process:
            process.map(subfinder.subfinder, unique_domain)
        with multiprocessing.Pool(multiprocessing.cpu_count()) as process:
            process.map(gobuster.gobuster, unique_domain)
        print("Subfinder finished", '\n')
        print("Wildcard check start!")
        wildcard.check_wildcard(scope)
        print()
        for domain in scope:
            number_domain += 1
            print(f"{number_domain}) Domain - {domain}")
            headers = domain+","+str(args.p)
            check_headers(headers)
    if args.f != 'no':
        if args.w != '':
            for domain in scope:
                f_data.append(domain+","+str(args.p)+"," +
                              str(args.r)+","+str(args.w))
                print(f_data)
                with multiprocessing.Pool(multiprocessing.cpu_count()) as process:
                    process.map(ffuf.ffuf, f_data)
                print("ffuf finished: ")  # , '%.2f' % end, " seconds", '\n')
    end_prog = time.time() - start_prog
    print("Program finished: ", '%.2f' % end_prog, " seconds", '\n')
