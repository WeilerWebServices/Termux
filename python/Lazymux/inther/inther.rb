require "uri"
require "json"
require "net/http"
require "net/https"

#### YOUR_API_KEY
@shodan_API_KEY = "ENTER_YOUR_API_KEY_HERE"
@censys_ID = "ENTER_YOUR_CENSYS_ID_HERE"
@censys_PASS = "ENTER_YOUR_CENSYS_PASS_HERE"
@whatcms_API_KEY = "ENTER_YOUR_API_KEY_HERE"
####

# Banner
@banner = "Inther v0.1-dev (c) 2018 by DedSecTL/DTL - Make with full of \033[91m<3\033[0m"
@bannerInther = "  inther - information gathering using shodan search engine, censys and more

# INTHER
~ hackertarget is an online vulnerability scanners to test your security from the attackers perspective
~ shodan is a search engine that lets the user find specific types of computers
~ censys is a platform that helps information security practitioners discover, monitor, and analyze devices that are accessible from the internet
~ whatcms is an online cms detector which can currently detect the use of more than 330 different cms applications and services


Usage: ruby inther.rb [SERVICE] [ARG] TARGET...

SERVICE:
  --hack         access hackertarget API Services
  --shodan       access shodan API Services
  --censys       access censys API Services
  --whatcms      access whatcms API Services

ARGUMENTS:
[--hack]
  -w,--whois                 lookup of a domain or IP address to find the registered owner, netblock, asn and registration dates
  -t,--traceroute            uses multiple icmp pings to test the connectivity to each hop across the internet
  -n,--nping                 used to determine the connectivity and latency of Internet connected hosts
  -d,--dnslookup             view the standard DNS records for a domain
  -f,--findnsrec             use this hostname search to find all the forward DNS records (A records) for an organisation
  -r,--reversedns            discover the reverse DNS entries for an IP address, a range of IP addresses or a domain name
  -g,--geoip                 find the location of an IP address with this GeoIP lookup tool
  -i,--reviplookup           identify hostnames that have DNS (A) records associated with an IP address
  -h,--httpheaders           review the HTTP Headers from a web server with this quick check
  -p,--pagelinks             parse the html of a website and extract links from the page

[--shodan]
  -i,--ip-shodan             returns all services that have been found on the given host IP
  -p,--port-shodan           this method returns a list of port numbers that the crawlers are looking for
  -r,--proto-shodan          this method returns an object containing all the protocols that can be used when launching an internet scan
  -d,--id-shodan             check the progress of a previously submitted scan request
  -h,--honey-shodan          calculates a honeypot probability score ranging from 0 (not a honeypot) to 1.0 (is a honeypot)
  -m,--myip-shodan           get your current IP address as seen from the internet
  -n,--dnsresolve-shodan     look up the IP address for the provided list of hostnames
  -o,--dnsreverse-shodan     look up the hostnames that have been defined for the given list of IP addresses

[--censys]
  -v,--view-censys           returns the current structured data censys have on a specific host, website, or certificate

[--whatcms]
  -d,--detect-whatcms        detect content management systems
"
def hackertarget
	if ARGV[1] == "-w" or ARGV[1] == "--whois"
		puts @banner
		url = URI("https://api.hackertarget.com/whois/?q=#{ARGV[2]}")
		data = Net::HTTP.get(url)
		puts data
	elsif ARGV[1] == "-t" or ARGV[1] == "--traceroute"
		puts @banner
		url = URI("https://api.hackertarget.com/mtr/?q=#{ARGV[2]}")
		data = Net::HTTP.get(url)
		puts data
	elsif ARGV[1] == "-n" or ARGV[1] == "--nping"
		puts @banner
		url = URI("https://api.hackertarget.com/nping/?q=#{ARGV[2]}")
		data = Net::HTTP.get(url)
		puts data
	elsif ARGV[1] == "-d" or ARGV[1] == "--dnslookup"
		puts @banner
		url = URI("https://api.hackertarget.com/dnslookup/?q=#{ARGV[2]}")
		data = Net::HTTP.get(url)
		puts data
	elsif ARGV[1] == "-f" or ARGV[1] == "--findnsrec"
		puts @banner
		url = URI("https://api.hackertarget.com/hostsearch/?q=#{ARGV[2]}")
		data = Net::HTTP.get(url)
		puts data
	elsif ARGV[1] == "-r" or ARGV[1] == "--reversedns"
		puts @banner
		url = URI("https://api.hackertarget.com/reversedns/?q=#{ARGV[2]}")
		data = Net::HTTP.get(url)
		puts data
	elsif ARGV[1] == "-g" or ARGV[1] == "--geoip"
		puts @banner
		url = URI("https://api.hackertarget.com/geoip/?q=#{ARGV[2]}")
		data = Net::HTTP.get(url)
		puts data
	elsif ARGV[1] == "-i" or ARGV[1] == "--reviplookup"
		puts @banner
		url = URI("https://api.hackertarget.com/reverseiplookup/?q=#{ARGV[2]}")
		data = Net::HTTP.get(url)
		puts data
	elsif ARGV[1] == "-h" or ARGV[1] == "--httpheaders"
		puts @banner
		url = URI("https://api.hackertarget.com/httpheaders/?q=http://#{ARGV[2]}")
		data = Net::HTTP.get(url)
		puts data
	elsif ARGV[1] == "-p" or ARGV[1] == "--pagelinks"
		puts @banner
		url = URI("https://api.hackertarget.com/pagelinks/?q=#{ARGV[2]}")
		data = Net::HTTP.get(url)
		puts data
	else
		puts "inther: error: #{ARGV[1]} is not an argument"
	end
end

def shodan
	if ARGV[1] == "-i" or ARGV[1] == "--ip-shodan"
		puts @banner
		url = URI("https://api.shodan.io/shodan/host/#{ARGV[2]}?key=#{@shodan_API_KEY}")
		request = Net::HTTP.get_response(url)
		data = JSON.parse(request.body)
		puts "IP: #{data["ip_str"]}"
		if data["hostnames"] != nil
			puts "Hostnames: #{data["hostnames"]}"
		end
		puts "Open Ports: #{data["ports"]}"
		puts "Organization: #{data["org"]}"
		if data["asn"] != nil
			puts "ASN: #{data["asn"]}"
		end
		puts "ISP: #{data["isp"]}"
		puts "Latitude: #{data["latitude"]}"
		puts "Longitude: #{data["longitude"]}"
		if data["city"] != nil
			puts "City: #{data["city"]}"
		end
		puts "Country Name: #{data["country_name"]}"
		puts "Country Code: #{data["country_code"]}"
		if data["region_code"] != nil
			puts "Region Code: #{data["region_code"]}"
		end
		if data["postal_code"] != nil
			puts "Postal Code: #{data["postal_code"]}"
		end
		if data["dma_code"] != nil
			puts "DMA Code: #{data["dma_code"]}"
		end
		if data["vulns"] != nil
			puts "Vulns: #{data["vulns"]}"
		end
		puts "\n[+] inther: each port results"
		for n in data["data"]
			puts "--------# Port #{n["port"]} Results #--------"
			puts "Info: #{n["info"]}"
			puts "Hash: #{n["hash"]}"
			puts "Transport: #{n["transport"]}"
			puts "\n[+] Data: \n#{n["data"]}"
			if n.include?("http") == true
				puts "[+] HTTP Data Information"
				if n["http"]["title"] != nil
					puts "Title: #{n["http"]["title"]}"
				end
				if n["http"]["robots_hash"] != nil
					puts "Robots Hash: #{n["http"]["robots_hash"]}"
				end
				puts "Redirects: #{n["http"]["redirects"]}"
				if n["http"]["sitemap_hash"] != nil
					puts "Sitemap Hash: #{n["http"]["sitemap_hash"]}"
				end
				if n["http"]["robots"] != nil
					puts "Robots: #{n["http"]["robots"]}"
				end
				if n["http"]["sitemap"] != nil
					puts "Sitemap: #{n["http"]["sitemap"]}"
				end
				if n["http"]["components"] != nil
					puts "Components: #{n["http"]["components"]}"
				end
				if n["http"]["server"] != nil
					puts "Server: #{n["http"]["server"]}"
				end
				if n["http"]["html_hash"] != nil
					puts "HTML Hash: #{n["http"]["html_hash"]}"
				end
				puts #new line
			end
			if n.include?("ssh") == true
				puts "[+] SSH Data Information"
				if n["ssh"]["fingerprint"] != nil
					puts "Fingerprint: #{n["ssh"]["fingerprint"]}"
				end
				if n["ssh"]["mac"] != nil
					puts "Mac: #{n["ssh"]["mac"]}"
				end
				if n["ssh"]["cipher"] != nil
					puts "Cipher: #{n["ssh"]["cipher"]}"
				end
				if n["ssh"]["key"] != nil
					puts "Key: #{n["ssh"]["key"]}"
				end
				if n["ssh"]["type"] != nil
					puts "Type: #{n["ssh"]["type"]}"
				end
				puts #new line
			end
			if n.include?("ssl") == true
				puts "[+] SSL Data Information"
				puts "SSL Versions: #{n["ssl"]["versions"]}"
				if n["ssl"]["serial"] != nil
					puts "Serial: #{n["ssl"]["serial"]}"
				end
				if n["ssl"]["cipher"] != nil
					puts "Cipher: #{n["ssl"]["cipher"]}"
				end
				puts #new line
			end
		end
	elsif ARGV[1] == "-p" or ARGV[1] == "--port-shodan"
		puts @banner
		url = URI("https://api.shodan.io/shodan/ports?key=#{@shodan_API_KEY}")
		request = Net::HTTP.get_response(url)
		puts "Ports: #{request.body}"
	elsif ARGV[1] == "-r" or ARGV[1] == "--proto-shodan"
		puts @banner
		url = URI("https://api.shodan.io/shodan/protocols?key=#{@shodan_API_KEY}")
		request = Net::HTTP.get_response(url)
		data = JSON.parse(request.body)
		puts "Riak: #{data["riak"]}"
		puts "Ethernetip-udp: #{data["ethernetip-udp"]}"
		puts "Kerberos: #{data["kerberos"]}"
		puts "HTTP: #{data["http"]}"
		puts "MongoDB: #{data["mongodb"]}"
		puts "PCAnywhere-Status: #{data["pcanywhere-status"]}"
		puts "Telnet: #{data["telnet"]}"
		puts "Nodata-tcp: #{data["nodata-tcp"]}"
		puts "PCWorx: #{data["pcworx"]}"
		puts "Modbus: #{data["modbus"]}"
	elsif ARGV[1] == "-d" or ARGV[1] == "--id-shodan"
		puts @banner
		url = URI("https://api.shodan.io/shodan/scan/#{ARGV[2]}?key=#{@shodan_API_KEY}")
		request = Net::HTTP.get_response(url)
		data = JSON.parse(request.body)
		puts "ID: #{data["id"]}"
		puts "Count: #{data["count"]}"
		puts "Status: #{data["status"]}"
	elsif ARGV[1] == "-h" or ARGV[1] == "--honey-shodan"
		puts @banner
		url = URI("https://api.shodan.io/labs/honeyscore/#{ARGV[2]}?key=#{@shodan_API_KEY}")
		request = Net::HTTP.get_response(url)
		if Integer(request.body) != 0
			puts "Honeypot: True"
		else
			puts "Honeypot: False"
		end
	elsif ARGV[1] == "-m" or ARGV[1] == "--myip-shodan"
		puts @banner
		url = URI("https://api.shodan.io/tools/myip?key=#{@shodan_API_KEY}")
		request = Net::HTTP.get_response(url)
		puts "MY_IP: #{request.body}"
	elsif ARGV[1] == "-n" or ARGV[1] == "--dnsresolve-shodan"
		puts @banner
		url = URI("https://api.shodan.io/dns/resolve?hostnames=#{ARGV[2]}&key=#{@shodan_API_KEY}")
		request = Net::HTTP.get_response(url)
		data = JSON.parse(request.body)
		hostnames = ARGV[2].split(",")
		hostnames.each do |n|
			puts "#{n.upcase}: #{data["n"]}"
		end
	elsif ARGV[1] == "-o" or ARGV[1] == "--dnsreverse-shodan"
		puts @banner
		url = URI("https://api.shodan.io/dns/reverse?ips=#{ARGV[2]}&key=#{@shodan_API_KEY}")
		request = Net::HTTP.get_response(url)
		data = JSON.parse(request.body)
		ips = ARGV[2].split(",")
		ips.each do |n|
			puts "#{n}: #{data["+n+"]}"
		end
	else
		puts "inther: error: #{ARGV[1]} is not an argument"
	end
end

def basicAuth(url)
	uri = URI(url)
	Net::HTTP.start(uri.host, uri.port,
		:use_ssl => uri.scheme == 'https', 
		:verify_mode => OpenSSL::SSL::VERIFY_NONE) do |http|
		
		request = Net::HTTP::Get.new uri.request_uri
		request.basic_auth "#{@censys_ID}", "#{@censys_PASS}"
		
		response = http.request request # Net::HTTPResponse object
		
		return response.body
	end
end
	
def censys
	if ARGV[1] == "-v" or ARGV[1] == "--view-censys"
		puts @banner
		response = basicAuth("https://www.censys.io/api/v1/view/ipv4/#{ARGV[2]}")
		data = JSON.parse(response)
		File.write("#{ARGV[2]}.json", response)
		puts "----- BASIC INFORMATION -----"
		if data["metadata"] != nil
			puts "OS: #{data["metadata"]["os_description"]}"
		end
		puts "Network: #{data["autonomous_system"]["description"]}"
		via = []
		data["autonomous_system"]["path"].each do |n|
			via << "AS#{n}"
		end
		puts "Routing: #{data["autonomous_system"]["routed_prefix"]} via #{via.join(' ')}"
		puts "Protocols: #{data["protocols"].join('')}"
		puts "\n80/HTTP"
		puts "GET /"
		puts "Server: #{data["80"]["http"]["get"]["metadata"]["description"]}"
		puts "Status Line: #{data["80"]["http"]["get"]["status_line"]}"
		puts "Page Title: #{data["80"]["http"]["get"]["title"]}"
		if data["80"]["http"]["get"]["metadata"]["description"] != 'cloudflare nginx'
			if data["443"] != nil
				puts "\n443/HTTPS"
				puts "Version: #{data["443"]["https"]["tls"]["version"]}"
				puts "Cipher Suite: #{data["443"]["https"]["tls"]["cipher_suite"]["name"]}"
				puts "Trusted: #{data["443"]["https"]["tls"]["validation"]["browser_trusted"]}"
				puts "Heartbleed Enabled: #{data["443"]["https"]["heartbleed"]["heartbeat_enabled"]}"
				puts "\nCryptographic Configuration"
				puts "Export DHE: #{data["443"]["https"]["dhe_export"]["support"]}"
				puts "Export RSA: #{data["443"]["https"]["rsa_export"]["support"]}"
				puts "DHE Support: #{data["443"]["https"]["dhe_export"]["support"]}"
			end
		end
		if data["22"] != nil
			puts "\n22/SSH"
			puts "Server: #{data["22"]["ssh"]["v2"]["metadata"]["description"]}"
			puts "Banner: #{data["22"]["ssh"]["v2"]["banner"]["raw"]}"
			puts "\nHost Key"
			puts "Algorithm: #{data["22"]["ssh"]["v2"]["server_host_key"]["key_algorithm"]}"
			puts "Fingerprint: #{data["22"]["ssh"]["v2"]["server_host_key"]["fingerprint_sha256"]}"
			puts "\nNegotiated Algorithm"
			puts "Key Exchange: #{data["22"]["ssh"]["v2"]["selected"]["kex_algorithm"]}"
			puts "Symmetric Cipher: #{data["22"]["ssh"]["v2"]["selected"]["client_to_server"]["cipher"]}"
			puts "MAC: #{data["22"]["ssh"]["v2"]["selected"]["client_to_server"]["mac"]}"
		end
		puts "\nGeographic Location"
		puts "City: #{data["location"]["city"]}"
		puts "Province: #{data["location"]["province"]}"
		puts "Country: #{data["location"]["country"]} (#{data["location"]["country_code"]})"
		puts "Lat/Long: #{data["location"]["latitude"]}, #{data["location"]["longitude"]}"
		puts "Timezone: #{data["location"]["timezone"]}"
		puts "\nFull data: #{ARGV[2]}.json"
	else
		puts "inther: error: #{ARGV[1]} is not an argument"
	end
end

def whatcms
	if ARGV[1] == "-d" or ARGV[1] == "--detect-whatcms"
		puts @banner
		request = Net::HTTP.get_response(URI("https://whatcms.org/APIEndpoint/Detect?key=#{@whatcms_API_KEY}&url=#{ARGV[2]}"))
		data = JSON.parse(request.body)
		if data["result"]["msg"] != "Success"
			puts data["result"]["msg"]
		else
			puts "Confidence: #{data["result"]["confidence"]}"
			puts "Code: #{data["result"]["code"]}"
			puts "Name: #{data["result"]["name"]}"
			puts "CMS URL: #{data["result"]["cms_url"]}"
			puts "Version: #{data["result"]["version"]}"
			puts "MSG: #{data["result"]["msg"]}"
			puts "ID: #{data["result"]["id"]}"
			puts "=======\nRequest web: #{data["request_web"]}"
		end
	else
		puts "inther: error: #{ARGV[1]} is not an argument"
	end
end

def inther
	if ARGV[0] == "--hack"
		hackertarget
	elsif ARGV[0] == "--shodan"
		shodan
	elsif ARGV[0] == "--censys"
		censys
	elsif ARGV[0] == "--whatcms"
		whatcms
	end
end

if __FILE__ == $0
	begin
		if ARGV.length < 2
			puts @bannerInther
		else
			inther
		end
	rescue SocketError
		puts "inther: error: check your internet connection"
	rescue Net::OpenTimeout
		puts "inther: error: check your internet connection"
	end
end