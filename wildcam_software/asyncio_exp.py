import asyncio
from asyncio import tasks
from datetime import datetime as DateTime
import time
from random import randint

async def async_function(task):
    print(f"[START {task}]")
    await asyncio.sleep(2)
    print(f"[END {task}]")


async def print_numbers(task):
    print(f"[START {task}]")
    for i in range(0, 10):
        print(f"{i} from [{task}]")
        await asyncio.sleep(0.5)
    print(f"[END {task}]")


async def print_timestamp(task, sleep_time):
    print(f'[START][{task}] AT {DateTime.now()}')
    await asyncio.sleep(sleep_time)
    print(f'[END][{task}] AT {DateTime.now()}')

    return f'{task}'


async def first_example():
    task_1 = asyncio.create_task(async_function("TASK 1"))
    task_2 = asyncio.create_task(print_numbers("TASK 2"))

    print("[AWAIT TASK 1]")
    await task_1
    print("[END AWAIT TASK 1]")

    print("[AWAIT TASK 2]")
    await task_2
    print("[END AWAIT TASK 2]")


async def second_example():
    task_1 = asyncio.create_task(print_numbers("TASK 1"))
    task_2 = asyncio.create_task(print_numbers("TASK 2"))
    await task_1
    await task_2
    

async def third_example():
    task_1 = asyncio.create_task(print_timestamp("TASK 1", 5))
    task_2 = asyncio.create_task(print_timestamp("TASK 2", 4))
    task_3 = asyncio.create_task(print_timestamp("TASK 3", 3))
    task_4 = asyncio.create_task(print_timestamp("TASK 4", 2))

    task_1_value = await task_1
    print(f"Do something with the value of {task_1_value}")
    await task_2
    await task_3
    await task_4


async def fourth_example():
    task_1 = asyncio.create_task(print_timestamp("TASK 1", randint(0, 5)))
    await asyncio.sleep(2)
    task_2 = asyncio.create_task(print_timestamp("TASK 2", randint(0, 5)))
    task_3 = asyncio.create_task(print_timestamp("TASK 3", randint(0, 5)))
    task_4 = asyncio.create_task(print_timestamp("TASK 4", randint(0, 5)))

    task_1_value = await task_1
    print(f"Do something with the value of {task_1_value}")
    await task_2
    await task_3
    await task_4


async def async_main():
    # FIRST EXAMPLE
    # task_1 and task_2 start at the same time
    # task_1 have to await for finshing the 2 seconds
    # 
    # task_2 is running at the same time and print out the numbers
    # task_1 is coming back because it finished
    # task_2 need more time
    # task_2 finished
    # await first_example()

    # SECOND EXAMPLE
    # task_1 and task_2 running at the same time
    # await second_example()

    # THIRD EXAMPLE
    #await third_example()

    # FOURTH EXAMPLE
    await fourth_example()


def main():
    print("[PROGRAMM START]")
    asyncio.run(async_main())
    print("[PROGRAM END]")


if __name__ == '__main__':
    main()


