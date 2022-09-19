#coding=utf-8
from unittest import result
from tasks import add

result = add.delay(4, 4)
print("Is taks ready: %s" % result.ready())

run_result = result.get(timeout=1)
print('sssss')
result.get(propagate=False)
print('task result: %s' % run_result)