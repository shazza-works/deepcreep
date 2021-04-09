# deepcreep

**Deep creep is an interrnet radio station crawler.**	

## Help:
-	Seed url or list will be checked and all links gathered to find out what they are.
-	Any audio streams will be saved and if there is stream info data that will also be saved.
-	The SEP mark for data is as follows URL |?| DATA. On start there is a test url you can try,
-	results will depend on the quality of the given seed or seed file list.

## Format:
-	As there needs to be some sort of url quality checking the only
-	format that will be taken for a seed is a url in the format.
-	http:// your_mums.domain.her /
-	https:// your_mums.domain.her /
-	http:// your_mums.domain.her
-	If a link is encountered with no scheme then deepcreep will do it's best to rebuild the link.
-	http:// + your_mums.domain.her + /

## File:
-	One url per line please given as first argument to deepcreep.
-	./deepcreep input_file

## Colour;
-	Green = Url steam with info data.
-	Yellow = Url stream with no data.
-	Red = Server or Connection Error.
-	Magenta = Backup progress to restore session.
-	(Note: If you have changed term colour this may not show).

## Request:
-	GET / HTTP/1.1
-	Host: host:port
-	User-Agent: Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
-	Accept-Encoding: gzip, deflate
-	Accept: */*
-	Connection: keep-alive
-	From: pokin@yourmums.domain.com

### Shazza-Works Discord
Click: [<img src="https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white"/>](https://discord.gg/CZ3jWT8Hpy)

### Linux Type
Click:	[<img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black"/>](https://en.wikipedia.org/wiki/X86-64)

### Python3 Doc's
Click: [<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>](https://docs.python.org/3/index.html)

