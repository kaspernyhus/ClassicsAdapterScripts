####
#  Calculate the correct dma parameters for the i2s driver
####
from math import floor, ceil


sample_rate = 48000  # Hz
bit_width = 16        # bit
channels = 2
polling_cycle = 10    # ms  //  max time of i2s_read polling cycle


# dma_frame_num should be as big as possible while the DMA buffer size won’t exceed its maximum value 4092
max_dma_buffer_size = 4092
dma_frame_num = floor(max_dma_buffer_size / (channels * (bit_width / 8 )))
dma_buffer_size = dma_frame_num * channels * (bit_width / 8 )
interrupt_interval = (dma_frame_num / sample_rate) * 1000
dma_desc_num = ceil(polling_cycle/interrupt_interval)

# user provided buffer to i2s_read must be bigger than
user_buffer = dma_desc_num * dma_buffer_size


print("-------------------------------------")
print(" ESP32 I2S DMA BUFFER SETTINGS")
print("-------------------------------------")
print("dma_desc_num (dma_buf_count):", dma_desc_num)
print("dma_frame_num (dma_buf_len):", dma_frame_num)
print("-----------------")
print("dma_buffer_size:", dma_buffer_size)
print("interrupt interval:", round(interrupt_interval, 3), "ms")
print("user buffer must be at least", int(user_buffer), "bytes")
print("-------------------------------------")


# ---------------------------------- #

dma_desc_num = 8
dma_frame_num = 480


dma_buffer_size = dma_frame_num * channels * (bit_width / 8)
interrupt_interval = (dma_frame_num / sample_rate) * 1000

print("dma_buffer_size", dma_buffer_size)
print("interrupt_interval:", interrupt_interval)