
## Installation
Installation can be completed via `docker-compose`
```bash
docker compose up
```

If you want to do something, please, proceed into `docker container` with a terminal and do what you want :)
```bash
# use `docker ps` to find docker container name
docker exec -it <container-name> bash
```


## Description and Reasoning
The main purpose is to implement a queue with some limitations:
- priority
- resource availability

On top of queue limitations, one should be aware of `queue` characteristics too:
- append from the right
- pop from the left

Combining `queue` characteristics and imposed limitations, we have such requirements:
- append from the right
- pop from the left
- pop from the middle (due to resources availability)
- update the task by id (optional)

In order to meed the requirements, I had two main solutions in mind, but after some train of thoughts I opted for a `doubly linked list` (`DLL` for short) to store the tasks and a `dict` to store tasks according to their priority.

### Solution 1 (Chosen one)
This solution consists of two main data structures: `DLL` and `dict`.

`DLL` is a data structure, that stores the pointers to the previous and next elements in the list of every item. This type of binding results in:
- fast append from the left and right (TC: `O(1)`, SC: `O(1)`)
- fast pop from the left and right (TC: `O(1)`, SC: `O(1)`)
- fast pop from the middle by id (TC: `O(1)`, SC: `O(1)`)

Downsides of `DLL`:
- slow search by index
- a bit complicated code

`dict` is used for 5 priorities to store task `id`s in them. `python` `dict` characteristics:
- fast search (TC: `O(1)`, SC: `O(1)`)
- fast pop (TC: `O(1)`, SC: `O(1)`)
- fast insert (TC: `O(1)`, SC: `O(1)`)
- guaranteed sorted keys (in `python >= 3.5`)

Downsides of `DLL`:
- no insert from the left
- no insert in the middle

### Solution 2 (Not chosen one)
Use simple `dict`s to store the tasks in them, the key is the task `id` and value is the task itself. Having a single `dict` for every priority, we can ensure that all requirements are met



### Why Solution 1 over Solution 2
Even though `solution 2` satisfies all the requirements, I opted for the `solution 1` for a few reasons:
- `solution 1` has fast append from the left (make even greater priority)
- with a smart indexing (epoch time and task `id`, see `DLL.nodes`) one can make a fast rearrangement of items (e.g. change priority or move a task within the same priority)
- - the same cannot be achieved fast with the set of `dict`s, cause into order to rearrange the keys in `dict`, one has to recreate the `dict` totally


## Testing

Enter into the docker container as described in `Installation` section and test with
```bash
# simple test
pytest

# test with coverage report
pytest --cov --cov-report=html:test_coverage_report --cov-report=term
```
