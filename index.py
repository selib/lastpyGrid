#!/usr/bin/env python3
print("Content-Type: text/html")
print()


print ("""
	html>
	<title>Interactive Page</title>
	<body>
	<form method=GET action="cgi-bin/nab.py">
		<P><B>Enter last.fm username:</B>
		<P><input type=text name=usr>
		<P><B>Enter time ranging back:</B>
		<P><input type=text name=tme>
		<P><B>Enter days looking back until: (needs to be the smaller number)</B>
		<P><input type=text name=timeto>
		<P><B>Display artists or albums (enter "ar" or "al")</B>
		<P><input type=text name=aroral>
		<P><input type=submit>
	</form>
	</body></html>
"""
)


