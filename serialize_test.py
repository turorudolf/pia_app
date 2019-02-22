import serialize
import datetime


#----------------------------------------------------------------------
if __name__ == "__main__":
	my_list = [i for i in range(10)]
	my_dict = {"bor":3, "time": datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")}
	my_string = "I'm a string!"
	pkl_path = "data/data.pkl"
	saved_list = serialize.load(pkl_path)
	if len(saved_list) > 0:
		serialize.save([saved_list, my_string], pkl_path)
	else:
		serialize.save(my_string, pkl_path)
	#serialize.save("", pkl_path)
	print saved_list
