import os


def pred_del(filename):
	delfilename = "test.png"
	path = "/home/willy/Ubuntu-Sever-Code/web-server/web/uploads/"
	pathname = os.path.abspath(os.path.join(path, filename))
	os.remove(delfilename)
	if pathname.startswith(path):
		os.remove(pathname)