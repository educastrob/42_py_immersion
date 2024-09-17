import time
import sys

def    ft_progress(lst):
    total = len(lst)
    start = time.time()

    for i, item in enumerate(lst):
        elapsed_time = time.time() - start
        percent = (i + 1) / total
        if i + 1 > 0:
            eta = (elapsed_time / (i + 1)) * (total - (i + 1))
        else:
            eta = 0
		
        bar_length = 10
        filled_length = int(bar_length * percent)
        if filled_length > 0:
            bar = '=' * (filled_length - 1) + '>'
        else:
            bar = ' ' * bar_length
        
        bar = bar.ljust(bar_length)
		
        print(f"ETA: {eta:.2f}s [{percent * 100:.2f}%] [{bar}] {i + 1}/{total} | elapsed time {elapsed_time:.2f}s", end="\r")
        yield item
        
def	main():
	list = range(1000)
	ret = 0
	for elem in ft_progress(list):
		ret += (elem + 3) % 5
		time.sleep(0.01)
	print()
	print(ret)
     
if __name__ == "__main__":
	main()