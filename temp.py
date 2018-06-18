import threading
#
# length = 8723
# int_end = int(length/1000+1)
# for ii in range(int_end):
#     start = ii*1000
#     end = (ii+1)*1000-1
#
#     if end > length:
#         end = length
#
#     print(start, '-', end, '-', end - start)


def start_thread(start, end, factor):
    index_length = int((end - start)/factor + 1)
    thread_array = []
    for index in range(index_length):
        index_start = index * factor
        index_end = (index + 1) * factor

        if end > index_end:
            index_end = end
        if factor > 10:
            thread_array[index] += [threading.Thread(target=start_thread, args=(index_start, index_end, factor/10))]
        else:
            thread_array[index] += [threading.Thread(target=clean_sheet, args=(index_start, index_end))]

        thread_array[index].start()

    for index in range(len(thread_array)):
        thread_array[index].join()
