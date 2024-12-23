from zeroconfig import Configer
import json

configer = Configer(enable_macros=True)
configer.load_sync('example.zc')

print(json.dumps(configer.to_dict(), indent=4, ensure_ascii=False))