import sys
import socket
import dns.resolver

def lookup_dns(domain):
    record_types = ['A', 'AAAA', 'MX', 'CNAME', 'TXT', 'SOA']
    results = {}
    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype, raise_on_no_answer=False)
            results[rtype] = [str(rdata) for rdata in answers]
        except dns.resolver.NoAnswer:
            results[rtype] = []
        except dns.resolver.NXDOMAIN:
            results[rtype] = ['No such domain']
        except Exception as e:
            results[rtype] = [f'Error: {e}']
    return results

def print_results(domain, results):
    print(f"Lookup results for: {domain}\n")
    for rtype, records in results.items():
        print(f"{rtype} Records:")
        if records:
            for rec in records:
                print(f"  {rec}")
        else:
            print("  No records found.")
        print()

def main():
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = input("Enter a domain name: ").strip()
    if not domain:
        print("No domain provided.")
        return
    try:
        # Check
        socket.gethostbyname(domain)
    except Exception:
        print("Invalid domain or unable to resolve.")
        return
    results = lookup_dns(domain)
    print_results(domain, results)

if __name__ == "__main__":
    main()
