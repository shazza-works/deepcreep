#!/usr/bin/python3
# Da Shazza-Works Yo
#
import sys, os
import time
import re
import pickle
import requests
from termcolor import cprint
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup



uline = "\x1b[4m"
reset = "\x1b[0m"

cprint("\n\n\t"+uline+"Ｗｅｌｃｏｍｅ ｔｏ Ｄｅｅｐ Ｃｒｅｅｐ"+reset, 'green')
cprint("\nThe internet radio stream hunter.\n", 'yellow')

def show_help():
	help = """Help:
	Seed url or list will be checked and all links gathered to find out what they are.
	Any audio streams will be saved and if there is stream info data that will also be saved.
	The SEP mark for data is as follows URL |?| DATA. On start there is a test url you can try,
	results will depend on the quality of the given seed or seed file list.

	Format:
	\tAs there needs to be some sort of url quality checking the only
	\tformat that will be taken for a seed is a url in the format.
	\t\thttp:// your_mums.domain.her /
	\t\thttps:// your_mums.domain.her /
	\t\thttp:// your_mums.domain.her
	\tIf a link is encountered with no scheme then deepcreep will do it's best to rebuild the link.
	\t\thttp:// + your_mums.domain.her + /

	File:
	\tOne url per line please given as first argument to deepcreep.
	\t\t./deepcreep input_file

	Colour;
	\tGreen = Url steam with info data.
	\tYellow = Url stream with no data.
	\tRed = Server or Connection Error.
	\tMagenta = Backup progress to restore session.
	\t\t(Note: If you have changed term colour this may not show).

	Credits:
	\tShazza-Works - https://github.com/shazza-works
	\t\t\t\t\t\t\t\t(like fuck he dose !)\n"""
	try:
		user_input = sys.argv[1]
		if user_input == '--help':
			cprint(help, 'yellow')
			sys.exit()
	except IndexError:
		pass

show_help()

cprint("TEST> http://www.radiofeeds.co.uk/mp3.asp\n", 'blue')

def get_backup():
	try:
		cprint("[*] DOING RESTORE NOW.", 'magenta')
		f = open('deepcreep.bk', 'rb')
		checked = pickle.load(f)
		to_creep =  pickle.load(f)
		music = pickle.load(f)
		cprint(f"Visited Sites Loaded ({len(checked)})", 'green')
		cprint(f"To Visit Sites Loaded ({len(to_creep)})", 'green')
		cprint(f"Found Music Sites Loaded ({len(music)})", 'green')
		f.close()
		return checked, to_creep, music
	except FileNotFoundError:
		checked, to_creep, music = [], [], []		
		cprint("[!] NO RESTORE FOUND!", 'red')
		cprint("[*] Moving on.")
		return checked, to_creep, music

checked, to_creep, music =  get_backup()

def read_input():
	try:
		file_input = sys.argv[1]
		if os.path.isfile(file_input):
			fd = open(file_input, 'r')
			for x in fd.readlines():
				to_creep.append(x)
		else:
			cprint("[!] File given dose not seem to be a file!")
			return
	except IndexError:
		pass

read_input()


def is_valid(url):
	parsed = urlparse(url)
	return bool(parsed.netloc) and bool(parsed.scheme)

def seed():
	try:
		while len(to_creep) == 0:
			i = input("Seed>")
			if is_valid(i):
				to_creep.append(i)
				return
			else:
				cprint("BAD URL TRY AGAIN PLEASE!", 'red')
				cprint(f"\nTry; {sys.argv[0]} --help for more info.", 'blue')
		else:
			return
	except KeyboardInterrupt:
		print("\nseed exit")
		sys.exit(1)

seed()

def make_backup():
	cprint("[*] MAKING BACKUP NOW", 'magenta')
	f = open('deepcreep.bk', 'wb')
	pickle.dump(checked, f)
	pickle.dump(to_creep, f)
	pickle.dump(music, f)
	f.close()

def add_creep(url):
	if url not in checked:
		cprint(f"[*] New url Added> {url}", 'blue')

def save(data):
	save = open("url_hitlog.txt", 'a')
	save.write(data+'\n')
	save.close()

headers = {
	'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
	'From': 'pokin@yourmums.domain.com'
}

def get_header(url):
	try:
		header = requests.head(url, timeout=2, headers=headers).headers
		return header
	except:
		pass
	try:
		header = requests.get(url, timeout=2, headers=headers).headers
		return header
	except:
		pass

def add_music(url, data=None):
	if url not in music:
		if not data == None:
			music.append(url)
			save( url + '|?|' + str(data) )
			cprint(f"[*] Stream [+info]({len(music)})> {url}", 'green')
		else:
			music.append(url)
			save(url)
			cprint(f"[*] Stream ({len(music)})> {url}", 'yellow')
		make_backup()
	else:
		pass

def get_page(link):
	page = requests.get(link, headers=headers, timeout=2).content
	return page

def get_type(url):
	head = get_header(url)
	if head is None and url not in checked:
		checked.append(url)
		return
	elif re.findall('audio/', str(head)):
		if re.findall('icy-', str(head)):
			data = dict(head)
			add_music(url, data)
			checked.append(url)
		else:
			data = None
			add_music(url, data)
			checked.append(url)
	elif re.findall('text/html', str(head)):
		add_creep(url)

def do_scoop(url):
	try:
		if not url in checked:
			page = get_page(url)
			soup = BeautifulSoup(page, "html.parser")
			try:
				for a_tag in soup.findAll("a"):
					href = a_tag.attrs.get("href")
					if href == "" or href is None:
						continue
					href = href.partition('?')[0]
					if re.findall('www.', href) and not re.findall('://', href):
						href = 'http://'+href
					if re.findall('://', href):
						href = href.replace(' ', '%20')
					if is_valid(href) and href not in to_creep:
						get_type(href)
						checked.append(href)
			except KeyboardInterrupt:
				print ("\nscoop exit")
				sys.exit(1)
	except:
		pass

def main():
	try:
		while to_creep:
			print ("LEN>", len(to_creep))
			link = to_creep.pop(0)
			do_scoop(link)
			checked.append(link)
		cprint("\nAll Jobs Are Done Thanks For Using Me...\n", 'green')
		sys.exit(0)
	except KeyboardInterrupt:
		print("\nmain exit")
		sys.exit(1)

main()