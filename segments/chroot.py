def add_chroot_segment():
	try:
		import os
		ch1 = os.stat('/proc/1/root/.')
		ch2 = os.stat('/')
		if ch1.st_ino != ch2.st_ino:
			fin = open('/etc/hostname', 'r')
			lines = fin.readlines()
			fin.close()
			powerline.append(' %s ' % lines[0][:-1], 15, 4)
		else:
			return
	except OSError:
		return

add_chroot_segment()
