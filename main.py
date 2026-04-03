from signals import signal, computed, effect

a = signal[int](5)
print("=====signal 1 registered=====")
a.subscribe(lambda x: print(f"I am watching a, and it is {x}"))
doubled = computed[int](lambda: a.value * 2)
print("=====effect 1 registered=====")
effect(lambda: print(f"a is now {a.value} and doubled is now {doubled.value}"))
print("=====effect 2 registered=====")
effect(lambda: print(f"this only prints once: doubled: {doubled.value}"))
print("============a+=1============")
a.value += 1
print("============a+=1============")
a.value += 1
print("============a*=10===========")
a.value *= 10

