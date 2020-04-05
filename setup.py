import wget, os

def download_files(files, directory):

	if os.path.exists(directory):
		for file in files.items():
			filename = file[0]
			url = file[1]
			print("\n\nDownloading from URL: " + url)
			path = os.path.join(directory,filename)
			try:
				wget.download(url, path)
				print("\nSaved in " + path)
			except KeyboardInterrupt as e:
				print("\n[!] Skipping...")
			except Exception as e:
				print("[X] " + str(e))
	else:
		print("\n[X] Folder " + directory + " does not exist...")


print("[*] Donwlading external files... Ctrl + C to skip current file download")


rules = {
	"hob064.rule": "https://raw.githubusercontent.com/praetorian-code/Hob0Rules/master/hob064.rule",
	"rockyou-30000.rule": "https://raw.githubusercontent.com/hashcat/hashcat/master/rules/rockyou-30000.rule",
	"T0XlC.rule": "https://raw.githubusercontent.com/hashcat/hashcat/master/rules/T0XlC.rule",
	"best64.rule": "https://raw.githubusercontent.com/hashcat/hashcat/master/rules/best64.rule",
	"d3ad0ne.rule": "https://raw.githubusercontent.com/hashcat/hashcat/master/rules/d3ad0ne.rule",
	"toggles-lm-ntlm.rule": "https://raw.githubusercontent.com/trustedsec/hate_crack/master/rules/toggles-lm-ntlm.rule",
	"OneRuleToRuleThemAll.rule": "https://raw.githubusercontent.com/NotSoSecure/password_cracking_rules/master/OneRuleToRuleThemAll.rule",
	"haku34K.rule": "https://raw.githubusercontent.com/kaonashi-passwords/Kaonashi/master/rules/haku34K.rule",
	"kamaji34K.rule": "https://raw.githubusercontent.com/kaonashi-passwords/Kaonashi/master/rules/kamaji34K.rule",
	"yubaba64.rule": "https://raw.githubusercontent.com/kaonashi-passwords/Kaonashi/master/rules/yubaba64.rule"

}

masks = {
	"kaonashi.hcmask": "https://raw.githubusercontent.com/kaonashi-passwords/Kaonashi/master/masks/kaonashi.hcmask",
	"2015-Top40-Time-Sort.hcmask": "https://blog.netspi.com/wp-content/uploads/2016/01/2015-Top40-Time-Sort.hcmask",
	"pathwell.hcmask": "https://raw.githubusercontent.com/trustedsec/hate_crack/master/masks/pathwell.hcmask",
	"rockyou-1-60.hcmask": "https://raw.githubusercontent.com/hashcat/hashcat/master/masks/rockyou-1-60.hcmask"
}

wordlists = {
	"google-10000-english.txt": "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt",
	"Password_Default_ProbWL.txt": "https://raw.githubusercontent.com/berzerk0/Probable-Wordlists/master/Dictionary-Style/Technical_and_Default/Password_Default_ProbWL.txt",
	"probable-v2-wpa-top4800.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/WiFi-WPA/probable-v2-wpa-top4800.txt",
	"rockyou.txt.bz2": "http://downloads.skullsecurity.org/passwords/rockyou.txt.bz2",
	"hashkiller.7z": "https://hashkiller.io/downloads/hashkiller-dict-2020-01-26.7z",
	"crackstation-human-only.txt.gz": "https://crackstation.net/files/crackstation-human-only.txt.gz"
}


base_dir = os.path.dirname(os.path.realpath(__file__))

download_files(rules, os.path.join(base_dir, "rules"))
download_files(masks, os.path.join(base_dir, "masks"))
download_files(wordlists, os.path.join(base_dir, "wordlists"))

print("\n\n\n\n[-->] TODO: extract rockyou.txt.bz2 --> bzip2 -d rockyou.txt.bz2")
print("\n[-->] TODO: extract hashkiller-dict-2020-01-26.7z --> 7za e hashkiller-dict-2020-01-26.7z")
print("\n[-->] TODO: extract crackstation-human-only.txt.gz --> realhuman_phill.txt")
print("\n[-->] TODO: download from mega or torrent Kaonashi14M --> https://github.com/kaonashi-passwords/Kaonashi/tree/master/wordlists and extract the wordlist: 7za e kaonashi14M.7z")