from zeroconfig import Configer

configer = Configer()
configer.load_sync('example.zeroconfig')

config = configer.to_dict()
print(config['multiline_string'])