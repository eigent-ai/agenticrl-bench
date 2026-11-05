def is_positive(n):
	if n > 0:
		return True
	else:
		return False


def check_range(n, low, high):
	if n < low or n > high:
		return False
	return True
