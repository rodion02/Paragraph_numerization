from check import check_file

file_txt = "tests/test1.txt"
# file_txt = "text/error text 2.txt"
config_json = "472.json"
check_file(txt_path=file_txt, json_path=config_json, visualize=True)
