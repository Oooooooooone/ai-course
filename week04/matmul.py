import torch, time

print("GPU 사용 가능:", torch.cuda.is_available())
print("GPU 이름:", torch.cuda.get_device_name(0))

size = 4000
a = torch.rand(size, size)
b = torch.rand(size, size)

start = time.time()
c = a @ b
cpu_time = time.time() - start
print("CPU:", round(cpu_time, 4), "초")

a_gpu = a.to("cuda")
b_gpu = b.to("cuda")
torch.cuda.synchronize()
start = time.time()
c_gpu = a_gpu @ b_gpu
torch.cuda.synchronize()
gpu_time = time.time() - start
print("GPU:", round(gpu_time, 4), "초")

print("GPU가 약", round(cpu_time / gpu_time), "배 빠름")