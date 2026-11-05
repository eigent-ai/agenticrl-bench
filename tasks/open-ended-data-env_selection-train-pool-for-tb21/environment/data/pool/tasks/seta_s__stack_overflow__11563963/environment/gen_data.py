#!/usr/bin/env python3
print("id,value,label")
for i in range(1, 501):
    if i % 50 == 0:
        value = 3.25
    elif i % 7 == 0:
        value = i * 0.25
    elif i % 3 == 0:
        value = -i * 0.125
    else:
        value = i * 1.5 + (i % 7) * 0.25
    print(f"{i},{value:.17g},item_{i:04d}")
